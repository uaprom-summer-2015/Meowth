from cloudinary.utils import cloudinary_url
from flask import url_for, current_app


class ImageHandler:
    _handler = None

    def init_app(self, app):
        self._handler = {
            "flask": self._get_from_flask,
            "cloudinary": self._get_from_cloudinary
        }[app.config["STATIC_SERVER"]]

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def get_image_url(self, path):
        return self._handler(path)

    def _get_from_flask(self, path):
        return current_app.config["SERVER_NAME"] + url_for("get_file",
                                                           path=path)

    def _get_from_cloudinary(self, path):
        return cloudinary_url(path)
