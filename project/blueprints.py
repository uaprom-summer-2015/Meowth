from flask import Blueprint


def _factory(bp_name, url_prefix):
    import_name = 'project.{}.views'.format(bp_name)
    template_folder = 'templates'
    blueprint = Blueprint(
        bp_name,
        import_name,
        template_folder=template_folder,
        url_prefix=url_prefix,
    )
    return blueprint

pages_app = _factory("pages", '')
admin_app = _factory("admin", '/admin')
auth_app = _factory("auth", '/auth')
feed_app = _factory("feed", '/vacancies')

all_blueprints = (pages_app, admin_app, auth_app, feed_app,)
