from project.lib.media.validators import allowed_file

def allowed_extension(form, file):
    return allowed_file(file.filename)