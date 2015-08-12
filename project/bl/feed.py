from flask import session
from project.bl.utils import BaseBL
from sqlalchemy.sql.expression import false


class CategoryBL(BaseBL):
    pass


class VacancyBL(BaseBL):
    def get_visible(self):
        return (
            self.model.query
            .filter(self.model.hide == false(),
                    self.model.deleted == false())
            .all()
        )

    def get_actual(self):
        return (
            self.model.query
            .filter(self.model.deleted == false())
            .all()
        )

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
