from project.bl.utils import BaseBL


class PageChunkBL(BaseBL):
    pass


class PageBL(BaseBL):

    def get_page_by_url(self, url):
        page_model = self.model
        page = page_model.query.filter(page_model.url == url).first()
        return page if page else None


class PageBlockBL(BaseBL):
    pass  # There is no PageBlock specific logic here
