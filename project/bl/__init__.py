from .auth import UserBL, TokenBL
from .feed import CategoryBL, CityBL, VacancyBL
from .pages import PageBL, PageBlockBL, PageChunkBL
from .mail import MailTemplateBL
from .utils import registry
from .uploads import UploadedImageBL

__all__ = ["UserBL", "CategoryBL", "CityBL", "VacancyBL", "PageBL",
           "PageBlockBL", "PageChunkBL", 'TokenBL', "UploadedImageBL", ]


def init_resource_registry():
    registry['bl.category'] = lambda category: CategoryBL(category)
    registry['bl.vacancy'] = lambda vacancy: VacancyBL(vacancy)
    registry['bl.city'] = lambda city: CityBL(city)
    registry['bl.user'] = lambda user: UserBL(user)
    registry['bl.pagechunk'] = lambda pagechunk: PageChunkBL(pagechunk)
    registry['bl.pageblock'] = lambda pageblock: PageBlockBL(pageblock)
    registry['bl.page'] = lambda page: PageBL(page)
    registry['bl.token'] = lambda token: TokenBL(token)
    registry['bl.mailtemplate'] = lambda template: MailTemplateBL(template)
    registry['bl.uploadedimage'] = lambda template: UploadedImageBL(template)
