from project.bl.utils import BaseBL


class CategoryBL(BaseBL):
    pass


class VacancyBL(BaseBL):

    def get_visible(self):
        return (
            self.model.query
            .filter(self.model.hide == False)
            .all()  # NOQA
        )


class CityBL(BaseBL):
    pass
