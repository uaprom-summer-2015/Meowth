from unittest.mock import Mock
from flask import url_for
from project.admin.utils import EntryList
from project.admin.views import SECTIONS, mainpage
from project.tests.utils import ProjectTestCase


expected_sections = dict([
    ('Пользователи', '/admin/users/'),
    ('Вакансии', '/admin/vacancies/'),
    ('Категории', '/admin/categories/'),
    ('Города', '/admin/cities/'),
    ('Блоки страниц', '/admin/blocks/'),
    ('Страницы', '/admin/pages/'),
    ('Элементы страниц', '/admin/pagechunks/'),
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
        # self.response = self.client.get("/admin/")

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed("admin/main.html")

    def test_view_generates_correct_context(self):
        self.assert_context("sections", expected_sections.items())


class SectionsTest(ProjectTestCase):
    def test_all_endpoints_can_be_resolved(self):
        for name in expected_sections:
            self.assertEqual(
                expected_sections[name],
                url_for("admin."+SECTIONS[name])
            )
