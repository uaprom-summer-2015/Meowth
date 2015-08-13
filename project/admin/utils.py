from flask import url_for, render_template, abort, request, current_app
from flask.views import MethodView, View
from project.models import UploadedImage
from werkzeug.utils import redirect


class EntryDetail(MethodView):
    """
        /entities/ GET → list of all entities
        /entity/<id> GET → get entity
        /entity/<id> POST → update entity
        /entity/ GET → create new entity
    """

    create_form = None
    update_form = None
    model = None
    template = None
    success_url = None

    def __init__(self, *, create_form, update_form=None, model,
                 success_url, template="admin/entry.html"):
        self.create_form = create_form
        self.update_form = update_form or create_form
        self.model = model
        self.template = template
        self.success_url = success_url

    def _clean_data(self, data):

        _data = {k: v for k, v in data.items() if k in self.model.__dict__}

        return _data

    def get(self, entry_id):
        entry = None
        if entry_id is None:
            # Add a new entry
            entry_form = self.create_form()
        else:
            # Update an old entry
            entry = self.model.bl.get(entry_id)

            if entry is None:
                abort(404)
            entry_form = self.update_form(obj=entry)

        return self.render_response(
            entry_form=entry_form,
            entry=entry)

    def post(self, entry_id):
        if entry_id is None:
            # Add a new entry
            form = self.create_form()
            if form.validate_on_submit():
                self.model.bl.create(form.data)
                return redirect(url_for("admin." + self.success_url))
        else:
            # Update an old entry
            instance = self.model.bl.get(entry_id)
            form = self.update_form(obj=instance)
            if form.validate_on_submit():
                instance.bl.update(form.data)
                return redirect(url_for("admin." + self.success_url))

        return self.render_response(entry_form=form)

    def render_response(self, **kwargs):
        return render_template(self.template, **kwargs)


class EntryList(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        return render_template(
            self.template,
            entries=self.model.query.all(),
        )


class VacancyList(EntryList):
    def dispatch_request(self):
        return render_template(
            self.template
        )


class GalleryImageDetail(EntryDetail):

    def get(self, entry_id):
        entry = None
        if entry_id is None:
            # Add a new entry
            clazz = self.create_form(config=current_app.config)
            entry_form = clazz()
        else:
            # Update an old entry
            entry = self.model.bl.get(entry_id)
            if entry is None:
                abort(404)
            entry_form = self.update_form(obj=entry)

        return self.render_response(
            entry_form=entry_form,
            entry=entry
        )

    def post(self, entry_id):
        if entry_id is None:
            # Add a new entry
            clazz = self.create_form(config=current_app.config)
            form = clazz()
            if form.validate_on_submit():
                image = request.files['image']
                self.model.bl.save_image(
                    image=image,
                    img_category=UploadedImage.IMG_CATEGORY.gallery,
                    title=form.data['title'],
                    description=form.data['description'],
                )
                return redirect(url_for("admin." + self.success_url))

        else:
            # Update an old entry
            instance = self.model.bl.get(entry_id)
            form = self.update_form(obj=instance)
            if form.validate_on_submit():
                if 'delete' in form.data:
                    instance.bl.delete()
                else:
                    instance.bl.update(form.data)
                return redirect(url_for("admin." + self.success_url))

        return self.render_response(entry_form=form)

    def render_response(self, **kwargs):
        return render_template(self.template, **kwargs)
