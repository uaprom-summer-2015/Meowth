from project.bl.utils import BaseBL


class PageBL(BaseBL):

    def get_page_by_id(self, id):
        page_model = self.model
        page = page_model.query.get(id)
        return page if page else None

    def get_page_by_url(self, url):
        page_model = self.model
        page = page_model.query.filter(page_model.url == url).first()
        return page if page else None

    def save(self):
        pass  # For now


class PageBlockBL(BaseBL):

    def get_block_by_id(self, id):
        block_model = self.model
        block = block_model.query.get(id)
        return block if block else None

    def save(self):
        pass  # For now
