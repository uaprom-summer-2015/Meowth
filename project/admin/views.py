from flask import render_template, url_for, session, redirect

from project.admin.forms import VacancyForm, CategoryForm, CityForm, \
    PageChunkForm, MailTemplateForm
from project.blueprints import admin_app
from project.pages.forms import PageBlockForm, PageForm
from project.pages.utils import PageDetail
from project.admin.utils import EntryDetail, EntryList
from project.auth.forms import RegisterForm
from project.models import Vacancy, Category, City, User, PageBlock, Page, \
    PageChunk, MailTemplate

SECTIONS = {}  # list_name: list_endpoint


@admin_app.before_request
def check_user_logged_in():
    if 'user_id' in session:
        return

    return redirect(url_for("auth.login"))


def register_section(*, section_name, list_endpoint,
                     list_route, detail_route,
                     list_view, detail_view):
    admin_app.add_url_rule(list_route, view_func=list_view)

    admin_app.add_url_rule(
        detail_route + "<int:entry_id>/",
        view_func=detail_view,
    )

    admin_app.add_url_rule(
        detail_route,
        defaults={'entry_id': None},
        view_func=detail_view,
    )

    SECTIONS[section_name] = list_endpoint


# Vacancies
vacancy_list = EntryList.as_view(
    name='vacancy_list',
    model=Vacancy,
    template="admin/vacancies.html",
)

vacancy_detail = EntryDetail.as_view(
    name='vacancy_detail',
    create_form=VacancyForm,
    model=Vacancy,
    template="admin/vacancy.html",
    success_url="vacancy_list",
)

register_section(
    section_name="Вакансии",
    list_route="/vacancies/",
    detail_route="/vacancy/",
    list_view=vacancy_list,
    detail_view=vacancy_detail,
    list_endpoint="vacancy_list",
)


# Categories
category_list = EntryList.as_view(
    name="category_list",
    model=Category,
    template="admin/categories.html",
)

category_detail = EntryDetail.as_view(
    name='category_detail',
    create_form=CategoryForm,
    model=Category,
    success_url="category_list",
)

register_section(
    section_name="Категории",
    list_route="/categories/",
    detail_route="/category/",
    list_view=category_list,
    detail_view=category_detail,
    list_endpoint="category_list",
)


# Cities
city_list = EntryList.as_view(
    name="city_list",
    model=City,
    template="admin/cities.html",
)
city_view = EntryDetail.as_view(
    name='city_detail',
    create_form=CityForm,
    model=City,
    success_url="city_list",
)

register_section(
    section_name="Города",
    list_route="/cities/",
    detail_route="/city/",
    list_view=city_list,
    detail_view=city_view,
    list_endpoint="city_list",
)


# Users
user_list = EntryList.as_view(
    name="user_list",
    model=User,
    template="admin/users.html",
)

user_detail = EntryDetail.as_view(
    name='user_detail',
    create_form=RegisterForm,
    model=User,
    success_url="user_list",
)

register_section(
    section_name="Пользователи",
    list_route="/users/",
    detail_route="/user/",
    list_view=user_list,
    detail_view=user_detail,
    list_endpoint="user_list",
)


# PageBlocks
pageblock_list = EntryList.as_view(
    name='pageblock_list',
    model=PageBlock,
    template="admin/pageblocks.html",
)

pageblock_view = EntryDetail.as_view(
    name='pageblock_detail',
    create_form=PageBlockForm,
    template='admin/pageblock.html',
    model=PageBlock,
    success_url="pageblock_list",
)

register_section(
    section_name="Блоки страниц",
    list_route="/blocks/",
    detail_route="/block/",
    list_view=pageblock_list,
    detail_view=pageblock_view,
    list_endpoint="pageblock_list",
)


# Pages
page_list = EntryList.as_view(
    name="page_list",
    model=Page,
    template="admin/pages.html",
)

page_view = PageDetail.as_view(
    name='page_detail',
    create_form=PageForm,
    model=Page,
    success_url="page_list",
)

register_section(
    section_name="Страницы",
    list_route="/pages/",
    detail_route="/page/",
    list_view=page_list,
    detail_view=page_view,
    list_endpoint="page_list",
)

# Page chunks
pagechunk_list = EntryList.as_view(
    name="pagechunk_list",
    model=PageChunk,
    template="admin/pagechunks.html",
)

pagechunk_detail = EntryDetail.as_view(
    name='pagechunk_detail',
    create_form=PageChunkForm,
    model=PageChunk,
    template="admin/pagechunk.html",
    success_url="pagechunk_list",
)

register_section(
    section_name="Элементы страниц",
    list_route="/pagechunks/",
    detail_route="/pagechunk/",
    list_view=pagechunk_list,
    detail_view=pagechunk_detail,
    list_endpoint="pagechunk_list",
)


# Mail Templates
mail_templates_list = EntryList.as_view(
    name="mail_templates_list",
    model=MailTemplate,
    template="admin/mailtemplates.html",
)

mail_template_detail = EntryDetail.as_view(
    name='mail_template_detail',
    create_form=MailTemplateForm,
    model=MailTemplate,
    template="admin/mailtemplate.html",
    success_url="mail_templates_list",
)

register_section(
    section_name="Шаблоны писем",
    list_route="/mail_templates/",
    detail_route="/mail_template/",
    list_view=mail_templates_list,
    detail_view=mail_template_detail,
    list_endpoint="mail_templates_list",
)


@admin_app.route("/")
def mainpage():
    sections = {}
    for name, endpoint in SECTIONS.items():
        sections[name] = url_for("admin." + endpoint)

    return render_template(
        "admin/main.html",
        sections=sections.items(),
    )


# noinspection PyUnusedLocal
@admin_app.errorhandler(403)
def handle_forbidden(error):
    return render_template('admin/403.html'), 403
