from .auth import UserBL
from .feed import CategoryBL, CityBL, VacancyBL
from .pages import PageBL, PageBlockBL, PageChunkBL
from .utils import registry

__all__ = ["UserBL", "CategoryBL", "CityBL", "VacancyBL", "PageBL",
           "PageBlockBL", "PageChunkBL"]


def init_resource_registry():
    registry['bl.category'] = lambda category: CategoryBL(category)
    registry['bl.vacancy'] = lambda vacancy: VacancyBL(vacancy)
    registry['bl.city'] = lambda city: CityBL(city)
    registry['bl.user'] = lambda user: UserBL(user)
    registry['bl.pagechunk'] = lambda pagechunk: PageChunkBL(pagechunk)
    registry['bl.pageblock'] = lambda pageblock: PageBlockBL(pageblock)
    registry['bl.page'] = lambda page: PageBL(page)
