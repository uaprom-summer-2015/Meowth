from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask.views import MethodView
from project.admin.forms import VacancyForm, CategoryForm
from project.admin import logic as bl

admin_app = Blueprint('admin', __name__)



# /entities/ GET → list of all entities
# /entity/<id> GET → get entity
# /entity/<id> POST → update entity
# /entity/ GET → create new entity

# class AdminBase:
#     class EntryList(MethodView):
#         def get(self):
#             return render_template(self._template_path,
#                                    entries=self._get_list())
#
#         def __init__(self, get_list, template_path):
#             self._get_list = get_list
#             self._template_path = template_path

class EntryDetail(MethodView):

    form = None
    # model = None
    template = None
    get_entry = None
    create_entry = None
    update_entry = None
    success_endpoint = None

    def __init__(self, form, get_entry, create_entry, update_entry,
                 success_endpoint, template="admin/entry.html"):
        self.form = form
        # self.model = model
        self.template = template
        self.get_entry = get_entry
        self.create_entry = create_entry
        self.update_entry = update_entry
        self.success_endpoint = success_endpoint

    def get(self, entry_id):
        if entry_id is None:
            # Add a new entry
            entry_form = self.form()
        else:
            # Update an old entry
            entry = self.get_entry(entry_id)

            if entry is None:
                abort(404)
            entry_form = self.form(obj=entry)
        return self.render_response(entry_form=entry_form)

    def post(self, entry_id):
        if entry_id is None:
            # Add a new entry
            form = self.form()
            if form.validate():
                self.create_entry(form.data)
                return redirect(url_for("admin."+self._redirect_endpoint))
        else:
            # Update an old entry
            form = self.form(request.form)
            if form.validate():
                self.update_entry(entry_id, form.data)
                return redirect(url_for("admin."+self._redirect_endpoint))

        return self.render_response(entry_form=form)

    def render_response(self, **kwargs):
        return render_template(self.template, **kwargs)

        # def __init__(self, get_entry, create_entry, update_entry,
        #              entry_template, entry_form, redirect_endpoint):
        #     self._get_entry = get_entry
        #     self._create_entry = create_entry
        #     self._update_entry = update_entry
        #     self._entry_template = entry_template
        #     self._entry_form = entry_form
        #     self._redirect_endpoint = redirect_endpoint

    # def __init__(self, app,
    #              list_endpoint, detail_endpoint,
    #              list_route, detail_route,
    #              get_list, get_entry, create_entry, update_entry,
    #              list_template, entry_template, entry_form
    #              ):
    #     self.entryList = self.EntryList(get_list, list_template)
    #     self.entryDetail = self.EntryDetail(get_entry, create_entry,
    #                                         update_entry, entry_template,
    #                                         entry_form, detail_endpoint)
    #
    #     list_view = self.entryList.as_view(list_endpoint)
    #     detail_view = self.EntryList.as_view(detail_endpoint)
    #

        # self.get_list = get_list
        # self.get_entry = get_entry
        # self.create_entry = create_entry
        # self.update_entry = update_entry
        # self.list_template = list_template
        # self.entry_template = entry_template
# app.add_url_rule(list_route, view_func=list_view)

vacancy_view = EntryDetail.as_view(
        name='vacancy_detail',
        form=VacancyForm,
        get_entry=bl.get_vacancy,
        update_entry=bl.update_vacancy,
        create_entry=bl.create_vacancy,
        template="admin/vacancy.html"
    )

admin_app.add_url_rule(
    "/vacancy/<int:entry_id>/",
    defaults={'entry_id': None},
    view_func=vacancy_view
)
admin_app.add_url_rule(
    "/vacancy/",
    defaults={'entry_id': None},
    view_func=vacancy_view
)

category_view = EntryDetail.as_view(
        name='category_detail',
        form=CategoryForm,
        get_entry=bl.get_category,
        update_entry=bl.update_category,
        create_entry=bl.create_category,
    )

admin_app.add_url_rule(
    "/category/<int:entry_id>/",
    view_func=category_view
)
admin_app.add_url_rule(
    "/category/",
    defaults={'entry_id': None},
    view_func=category_view
)


@admin_app.route("/vacancies")
def vacancy_list():
    return render_template("admin/vacancies.html",
                           vacancies=bl.get_vacancies())


# @admin_app.route("/vacancies/new", methods=['GET', 'POST'])
# def vacancy_new():
#     if request.method == 'GET':
#         form = VacancyForm()
#
#     elif request.method == 'POST':
#         form = VacancyForm(request.form)
#         if form.validate():
#             bl.create_vacancy(form.data)
#             return redirect(url_for("admin.vacancy_list"))
#
#     return render_template(
#         "admin/vacancy.html",
#         vacancy_form=form
#     )
#
#
# @admin_app.route('/vacancies/<int:vacancy_id>',
#                  methods=['GET', 'POST'])
# def vacancy_detail(vacancy_id):
#     if request.method == 'GET':
#         vacancy = bl.get_vacancy(vacancy_id)
#         form = VacancyForm(obj=vacancy)
#
#     elif request.method == 'POST':
#         form = VacancyForm(request.form)
#         if form.validate():
#             bl.update_vacancy(vacancy_id, form.data)
#             return redirect(url_for("admin.vacancy_list"))
#
#     return render_template(
#         "admin/vacancy.html",
#         vacancy_form=form,
#     )


@admin_app.route("/categories")
def category_list():
    return render_template("admin/categories.html",
                           categories=bl.get_categories())


# @admin_app.route("/categories/new", methods=['GET', 'POST'])
# def category_new():
#     if request.method == 'GET':
#         form = CategoryForm()
#
#     elif request.method == 'POST':
#         form = CategoryForm(request.form)
#         if form.validate():
#             bl.create_category(form.data)
#             return redirect(url_for("admin.category_list"))
#
#     return render_template(
#         "admin/entry.html",
#         category_form=form
#     )
#
#
# @admin_app.route('/categories/<int:category_id>',
#                  methods=['GET', 'POST'])
# def category_detail(category_id):
#     if request.method == 'GET':
#         category = bl.get_category(category_id)
#         form = CategoryForm(obj=category)
#
#     elif request.method == 'POST':
#         form = CategoryForm(request.form)
#         if form.validate():
#             bl.update_category(category_id, form.data)
#             return redirect(url_for("admin.category_list"))
#
#     return render_template(
#         "admin/entry.html",
#         category_form=form,
#     )
