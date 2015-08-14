from flask import session
from project.bl.utils import BaseBL


class CategoryBL(BaseBL):
    pass


class VacancyBL(BaseBL):
    def visit(self):
        self.model.visits += 1
        self.save()

    def update(self, data):
        self.update_user()
        super().update(data)

    def update_user(self):
        self.model.user_id = session['user_id']


class CityBL(BaseBL):
    pass
