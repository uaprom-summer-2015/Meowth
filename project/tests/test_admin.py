import json
from unittest.mock import Mock
from flask import url_for
from project.admin.utils import EntryList
from project.admin.views import SECTIONS, mainpage
from project.models import PageBlock, Page
from project.tests.utils import ProjectTestCase


expected_sections = dict([
    ('Пользователи', '/admin/users/'),
    ('Вакансии', '/admin/vacancies/'),
    ('Категории', '/admin/categories/'),
    ('Города', '/admin/cities/'),
    ('Блоки страниц', '/admin/blocks/'),
    ('Страницы', '/admin/pages/'),
    ('Элементы страниц', '/admin/pagechunks/'),
    ('Шаблоны писем', '/admin/mail_templates/'),
    ('Галлерея', '/admin/gallery_images/'),
])


class EntryListTests(ProjectTestCase):

    render_templates = False
    template = "404.html"  # who cares what template we use?
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


class MainPageTest(ProjectTestCase):
    render_templates = False

    def setUp(self):
        self.view = mainpage
        self.view()

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed("admin/main.html")

    def test_view_generates_correct_context(self):
        self.assert_context("sections", expected_sections.items())


class SectionsTest(ProjectTestCase):
    def test_all_endpoints_can_be_resolved(self):
        for name in expected_sections:
            self.assertEqual(
                expected_sections[name],
                url_for("admin." + SECTIONS[name])
            )


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
