from project.admin.utils import EntryDetail
from flask import url_for, abort
from werkzeug.utils import redirect


class PageDetail(EntryDetail):

    def get(self, entry_id):
        if entry_id is None:
            # Forbidden
            abort(403)
        else:
            # Update an old entry
            entry = self.model.bl.get(entry_id)

            if entry is None:
                abort(404)
            entry_form = self.update_form(obj=entry)

            keys = [k for k in entry_form.data if k.startswith('block_')]
            keys.sort()
            upd = dict(zip(keys, entry.blocks))
            _data = entry_form.data.copy()
            _data.update(upd)
            entry_form.process(**_data)
            del _data

        return self.render_response(entry_form=entry_form)

    def post(self, entry_id):
        def prepare_data(data):
            """ Convert data to normal form """
            _data = data.copy()
            keys = [k for k in _data if k.startswith('block_')]
            keys.sort()
            _data['blocks'] = []
            for k in keys:
                if _data[k] and _data[k] not in _data['blocks']:
                    _data['blocks'].append(_data[k])
                _data.pop(k, None)
            return _data

        if entry_id is None:
            # Forbidden
            abort(403)
        else:
            # Update an old entry
            instance = self.model.bl.get(entry_id)
            form = self.update_form(obj=instance)
            if form.validate_on_submit():
                instance.bl.update(prepare_data(form.data))
                return redirect(url_for("admin."+self.success_url))

        return self.render_response(entry_form=form)
