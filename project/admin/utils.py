from flask import url_for, render_template, abort
from flask.views import MethodView, View
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
        # FIXME: This is Base view.
        # WTF removing confirmation field (user registration)
        # from form.data is doing here?
        _data = data
        _data.pop('confirmation', None)
        return _data

    def get(self, entry_id):
        if entry_id is None:
            # Add a new entry
            entry_form = self.create_form()
        else:
            # Update an old entry
            entry = self.model.bl.get(entry_id)

            if entry is None:
                abort(404)
            entry_form = self.update_form(obj=entry)

        return self.render_response(entry_form=entry_form)

    def post(self, entry_id):
        if entry_id is None:
            # Add a new entry
            form = self.create_form()
            if form.validate_on_submit():
                self.model.bl.create(form.data)
                return redirect(url_for("admin."+self.success_url))
        else:
            # Update an old entry
            form = self.update_form()
            if form.validate_on_submit():
                # FIXME: WTF is this here?
                if hasattr(self.update_form, 'user_instance'):
                    delattr(self.update_form, 'user_instance')
                model = self.model.bl.get(entry_id)
                model.bl.update(self._clean_data(form.data))
                return redirect(url_for("admin."+self.success_url))

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
