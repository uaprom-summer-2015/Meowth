from flask import render_template, url_for, jsonify

from project.admin import forms
from project.blueprints import admin_app
from project.lib.admin import get_actual_vacancies_list
from project.models import PageBlock, Page
from project.pages.admin import PageDetail
from project.pages.forms import PageBlockForm, PageForm
from project.admin.utils import (
    EntryDetail, EntryList, VacancyList, GalleryImageDetail
)
from project.auth.forms import RegisterForm
from project.auth.decorators import login_required
from project import models
from project.lib.auth import get_user_from_session

from collections import namedtuple

Endpoint = namedtuple('Endpoint', ['ep', 'su_only'])
SECTIONS = {}  # list_name: list_endpoint


def register_section(*, section_name, list_endpoint,
                     list_route, detail_route,
                     list_view, detail_view, su_only=False):
    list_view = login_required(su_only=su_only)(list_view)
    detail_view = login_required(su_only=su_only)(detail_view)

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

    SECTIONS[section_name] = Endpoint(list_endpoint, su_only)


# Vacancies
vacancy_list = VacancyList.as_view(
    name='vacancy_list',
    model=models.Vacancy,
    template="admin/vacancies.html",
)

vacancy_detail = EntryDetail.as_view(
    name='vacancy_detail',
    create_form=forms.VacancyForm,
    model=models.Vacancy,
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


@admin_app.route('/vacancies/list/')
@login_required()
def json_vacancies():
    vacancies_list = get_actual_vacancies_list()
    return jsonify(
        vacancies=vacancies_list,
    )

# Categories
category_list = EntryList.as_view(
    name="category_list",
    model=models.Category,
    template="admin/categories.html",
)

category_detail = EntryDetail.as_view(
    name='category_detail',
    create_form=forms.CategoryForm,
    model=models.Category,
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
    model=models.City,
    template="admin/cities.html",
)
city_view = EntryDetail.as_view(
    name='city_detail',
    create_form=forms.CityForm,
    model=models.City,
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
    model=models.User,
    template="admin/users.html",
)

user_detail = EntryDetail.as_view(
    name='user_detail',
    create_form=RegisterForm,
    model=models.User,
    success_url="user_list",
)

register_section(
    section_name="Пользователи",
    list_route="/users/",
    detail_route="/user/",
    list_view=user_list,
    detail_view=user_detail,
    list_endpoint="user_list",
    su_only=True,
)


# PageBlocks
pageblock_list = EntryList.as_view(
    name='pageblock_list',
    model=models.PageBlock,
    template="admin/pageblocks.html",
)

pageblock_view = EntryDetail.as_view(
    name='pageblock_detail',
    create_form=PageBlockForm,
    template='admin/pageblock.html',
    model=models.PageBlock,
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
    model=models.Page,
    template="admin/pages.html",
)

page_view = PageDetail.as_view(
    name='page_detail',
    create_form=PageForm,
    model=models.Page,
    success_url="page_list",
    template="admin/page.html",
)

register_section(
    section_name="Страницы",
    list_route="/pages/",
    detail_route="/page/",
    list_view=page_list,
    detail_view=page_view,
    list_endpoint="page_list",
)


@admin_app.route("/page/<int:entry_id>/block_list/")
@login_required()
def block_list(entry_id):
    page = Page.query.get(entry_id)
    ids = [str(block.id) for block in page.blocks]
    return jsonify(entries=ids)


@admin_app.route("/pages/available_blocks/")
@login_required()
def available_blocks():
    blocks = [{"value": str(block.id), "label": str(block)}
              for block in PageBlock.query.all()]
    return jsonify(blocks=blocks)


# Page chunks
pagechunk_list = EntryList.as_view(
    name="pagechunk_list",
    model=models.PageChunk,
    template="admin/pagechunks.html",
)

pagechunk_detail = EntryDetail.as_view(
    name='pagechunk_detail',
    create_form=forms.PageChunkForm,
    model=models.PageChunk,
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
    model=models.MailTemplate,
    template="admin/mailtemplates.html",
)

mail_template_detail = EntryDetail.as_view(
    name='mail_template_detail',
    create_form=forms.MailTemplateForm,
    model=models.MailTemplate,
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

# Gallery Images
images_list = EntryList.as_view(
    name='images_list',
    model=models.UploadedImage,
    template="admin/images.html",
)

image_detail = GalleryImageDetail.as_view(
    name='image_detail',
    create_form=forms.image_upload_form_factory,
    model=models.UploadedImage,
    success_url='images_list',
    template='admin/image.html',
)

register_section(
    section_name="Изображения",
    list_route="/images/",
    detail_route="/image/",
    list_view=images_list,
    detail_view=image_detail,
    list_endpoint="images_list",
)


@admin_app.route("/")
@login_required()
def mainpage():
    sections = {}
    u = get_user_from_session()
    for name, endpoint in SECTIONS.items():
        if not endpoint.su_only or u.is_superuser():
            sections[name] = url_for("admin." + endpoint.ep)
    return render_template(
        "admin/main.html",
        sections=sections.items(),
    )


# noinspection PyUnusedLocal
@admin_app.errorhandler(403)
def handle_forbidden(error):
    return render_template('admin/errors/403.html'), 403
