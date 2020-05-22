import abc
from typing import List, Any, NamedTuple


class AbstractDataProvider(abc.ABC):
	@abc.abstractmethod
	def get_page_rows(self, page_num: int, size) -> List[Any]:
		pass

	@abc.abstractmethod
	def get_columns(self):
		pass


class DummyProvider(AbstractDataProvider):
	def get_page_rows(self, page_num: int, size) -> List[NamedTuple]:
		return []

	def get_columns(self) -> List[str]:
		return 	["col"]
