import json
from unittest.mock import Mock
from flask import url_for
from project.admin.utils import EntryList
from project.admin.views import vacancy_detail
from project.admin.views import SECTIONS
from project.models import PageBlock, Page, Vacancy
from project.tests.utils import ProjectTestCase
from werkzeug.exceptions import NotFound


SU_ONLY_SECTIONS = ['Пользователи']

expected_sections = dict([
    ('Пользователи', '/admin/users/'),
    ('Вакансии', '/admin/vacancies/'),
    ('Категории', '/admin/categories/'),
    ('Города', '/admin/cities/'),
    ('Блоки страниц', '/admin/blocks/'),
    ('Страницы', '/admin/pages/'),
    ('Элементы страниц', '/admin/pagechunks/'),
    ('Шаблоны писем', '/admin/mail_templates/'),
    ('Галерея', '/admin/gallery_images/'),
])


class EntryListTests(ProjectTestCase):

    render_templates = False
    template = "test.html"  # who cares what template we use?
    model = Mock()

    def setUp(self):
        self.view = EntryList.as_view(
            name="whatever",
            model=self.model,
            template=self.template,
        )
        self.view()

    def test_view_uses_correct_template(self):
        self.assert_template_used(self.template)

    def test_view_uses_all_model_objects(self):
        self.model.query.all.assert_called_once_with()


class EntryDetailTest(ProjectTestCase):
    pass


class SectionsTest(ProjectTestCase):
    def test_all_endpoints_can_be_resolved(self):
        for name in expected_sections:
            self.assertEqual(
                expected_sections[name],
                url_for("admin." + SECTIONS[name].ep)
            )


class VacancyAdminDeletionTest(ProjectTestCase):
    def test_deleted_raises_404(self):
        pk = Vacancy.query.filter(Vacancy.condition_is_deleted).first().id
        self.assertRaises(NotFound, vacancy_detail, pk)


class PermissionsTest(ProjectTestCase):
    def test_userlist_returns_403(self):
        self.log_in('dipperpines')
        resp = self.client.get(url_for('admin.user_list'))
        self.assert403(resp)

    def test_userlist_returns_200_superuser(self):
        self.log_in('cthulhu')
        resp = self.client.get(url_for('admin.user_list'))
        self.assert200(resp)

    def test_userdetail_returns_403(self):
        self.log_in('dipperpines')
        resp = self.client.get(url_for('admin.user_detail', entry_id=1))
        self.assert403(resp)

    def test_userdetail_returns_200_superuser(self):
        self.log_in('cthulhu')
        resp = self.client.get(url_for('admin.user_detail', entry_id=1))
        self.assert200(resp)

    def test_correct_sections_staff(self):
        expected = dict([(k, v) for k, v in expected_sections.items()
                         if k not in SU_ONLY_SECTIONS])
        self.log_in('dipperpines')
        self.client.get(url_for('admin.mainpage'))
        self.assert_context("sections", expected.items())

    def test_correct_sections_superuser(self):
        self.log_in('cthulhu')
        self.client.get(url_for('admin.mainpage'))
        self.assert_context("sections", expected_sections.items())

    def test_view_uses_correct_template(self):
        self.log_in('cthulhu')
        self.client.get(url_for('admin.mainpage'))
        self.assertTemplateUsed("admin/main.html")


class VacancyAuxilliarTest(ProjectTestCase):
    def test_avail_block_view_returns_correct_value(self):
        self.log_in()
        pageblocks = [{"label": str(block), "value": str(block.id)}
                      for block in PageBlock.query.all()]
        url = url_for('admin.available_blocks')
        response = self.client.get(url, follow_redirects=True)
        expected = bytes(
            json.dumps({"blocks": pageblocks}, sort_keys=True),
            encoding='utf8',
        )
        self.assertEqual(expected, response.data)

    def test_chosen_block_view_returns_correct_value(self):
        self.log_in()
        for page in Page.query.all():
            blocks = [str(block.id) for block in page.blocks]
            url = url_for('admin.block_list', entry_id=page.id)
            response = self.client.get(url, follow_redirects=True)
            expected = bytes(
                json.dumps({"entries": blocks}, sort_keys=True),
                encoding='utf8',
            )
            self.assertEqual(expected, response.data)
