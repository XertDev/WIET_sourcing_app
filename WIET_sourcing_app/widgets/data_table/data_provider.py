import abc
from typing import List, Any


class AbstractDataProvider(abc.ABC):
	@abc.abstractmethod
	async def get_page_rows(self, page_num: int, size, query: str) -> List[Any]:
		pass

	@abc.abstractmethod
	def get_columns(self) -> List[str]:
		pass

	@abc.abstractmethod
	async def get_row_count(self) -> int:
		pass


class DummyProvider(AbstractDataProvider):
	async def get_page_rows(self, page_num: int, size: int, query: str) -> List[tuple]:
		return [("row"+str(i), (i, 2*i)) for i in range(page_num, page_num + size)]

	def get_columns(self) -> List[str]:
		return ["col", "2xcol"]

	async def get_row_count(self) -> int:
		return 1000
