from flask import url_for, abort
from werkzeug.utils import redirect

from project.admin.utils import EntryDetail
from project.models import PageBlock


class PageDetail(EntryDetail):
    def get(self, entry_id):
        if entry_id is None:
            # Restrict creating new pages
            abort(403)

        # Update an old entry
        entry = self.model.bl.get(entry_id)

        if entry is None:
            abort(404)
        entry_form = self.update_form(obj=entry)

        pageblocks = [block.title for block in PageBlock.query.all()]

        for block in entry_form.blocks:
            block.choices = pageblocks

        return self.render_response(
            entry_form=entry_form,
            entry=entry)

    def post(self, entry_id):
        if entry_id is None:
            # Restrict creating new pages
            abort(403)

        # Update an old entry
        form = self.update_form()
        if form.validate_on_submit():
            instance = self.model.bl.get(entry_id)
            instance.bl.update(form.data)
            return redirect(url_for("admin." + self.success_url))

        return self.render_response(entry_form=form)
