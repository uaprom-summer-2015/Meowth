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

    def visit(self):
        self.model.visits += 1
        self.model.save()


class CityBL(BaseBL):
    pass
