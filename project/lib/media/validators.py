from flask import current_app as app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def allowed_image(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1] in
        app.config['IMG_EXTENSIONS']
    )
