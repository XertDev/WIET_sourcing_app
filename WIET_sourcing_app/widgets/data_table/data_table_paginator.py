from math import ceil

from rx.subjects import BehaviorSubject


class DataTablePaginator:

	_page = BehaviorSubject(0)
	_page_size = BehaviorSubject(10)
	_item_count = BehaviorSubject(0)

	@property
	def page(self) -> BehaviorSubject:
		return self._page

	@property
	def page_size(self) -> BehaviorSubject:
		return self._page_size

	@property
	def item_count(self) -> BehaviorSubject:
		return self._item_count

	def set_page(self, page: int) -> None:
		if page < 0:
			raise IndexError("Page number must be bigger or equal than 0")
		pages_count = ceil(self.item_count.value/self.page_size.value)
		if page >= pages_count:
			raise IndexError("Page does not exist")
		self._page.on_next(page)

	def set_page_size(self, page_size: int) -> None:
		if page_size <= 0:
			raise ValueError("Page size must be bigger than 0")
		self._page_size.on_next(page_size)

	def set_item_count(self, item_count: int) -> None:
		if item_count < 0:
			raise ValueError("Item count must be bigger than 0")
		self._item_count.on_next(item_count)

	def next_page(self):
		self._page.on_next(self._page.value+1)

	def prev_page(self):
		self._page.on_next(self._page.value-1)
