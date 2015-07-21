from project.bl.utils import BaseBL


class PageBL(BaseBL):

    def get_page_by_url(self, url):
        page_model = self.model
        page = page_model.query.filter(page_model.url == url).first()
        return page if page else None

    def save(self):
        pass  # For now

    def update(self, data):
        model = self.model
        # Possible crutch ahead:
        while len(model.blocks):
            model._blocks.pop().soft_delete()
        for key, value in data.items():
            if key != 'blocks':
                setattr(model, key, value)
        for block in data['blocks']:
            model.blocks.append(block)
        model.save()
        return model


class PageBlockBL(BaseBL):

    def save(self):
        pass  # For now

    def update(self, data):
        pass  # For now
