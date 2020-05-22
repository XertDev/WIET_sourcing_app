import abc
from typing import List, Any


class AbstractDataProvider(abc.ABC):
	@abc.abstractmethod
	def get_page_rows(self, page_num: int, size) -> List[Any]:
		pass

	@abc.abstractmethod
	def get_columns(self) -> List[str]:
		pass

	@abc.abstractmethod
	def get_row_count(self) -> int:
		pass


class DummyProvider(AbstractDataProvider):
	def get_page_rows(self, page_num: int, size) -> List[tuple]:
		return [("row"+str(i), (i, 2*i)) for i in range(page_num, page_num + size)]

	def get_columns(self) -> List[str]:
		return ["col", "2xcol"]

	def get_row_count(self) -> int:
		return 1000
