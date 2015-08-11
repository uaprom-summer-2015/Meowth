from project.bl.utils import BaseBL


class PageChunkBL(BaseBL):
    pass


class PageBL(BaseBL):

    def get(self, _type):
        return self.model.query.filter(self.model.type == _type).one()


class PageBlockBL(BaseBL):
    pass  # There is no PageBlock specific logic here
