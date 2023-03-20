from typing import Optional

from project.dao.main import DirectorsDAO
from project.exceptions import ItemNotFound
from project.models import Director


class DirectorsService:
    def __init__(self, dao: DirectorsDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Director:
        if director := self.dao.get_by_id(pk):
            return director
        raise ItemNotFound(f'Director with pk={pk} does not exists.')

    def get_all(self, page: Optional[int] = None) -> list[Director]:
        return self.dao.get_all(page=page)
