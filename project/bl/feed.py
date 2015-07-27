from project.bl.utils import BaseBL


class CategoryBL(BaseBL):
    pass


class VacancyBL(BaseBL):

    def get_visible(self):
        vacancies = self.model.query\
            .filter(self.model.hide == False)\
            .all()  # NOQA
        return vacancies


class CityBL(BaseBL):
    pass
