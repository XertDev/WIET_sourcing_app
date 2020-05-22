#Based on https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/uix/datatables.py
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView


from WIET_sourcing_app.widgets.data_table.data_provider import DummyProvider, AbstractDataProvider
from WIET_sourcing_app.widgets.data_table.data_table_header import DataTableHeader
from WIET_sourcing_app.widgets.data_table.data_table_pagination import DataTablePagination
from WIET_sourcing_app.widgets.data_table.data_table_paginator import DataTablePaginator

Builder.load_string(
	"""
<DataTable>
	orientation: "vertical"
	canvas:
		Color:
			rgba: rgba (1, 1, 1, 1)
		RoundedRectangle:
			pos: self.pos
			size: self.size
	"""
)


class DataTableView(RecycleView):
	def __init__(self,  **kwargs):
		super(DataTableView, self).__init__(**kwargs)


class DataTable(BoxLayout):
	_table_view: DataTableView
	_header: DataTableHeader
	_pagination: DataTablePagination
	paginator: DataTablePaginator
	data_provider: AbstractDataProvider = DummyProvider()

	def __init__(self, **kwargs):
		super(DataTable, self).__init__(**kwargs)
		self._table_view = DataTableView()
		self._header = DataTableHeader(["No."] + self.data_provider.get_columns())

		self.paginator = DataTablePaginator()
		self._pagination = DataTablePagination(self.paginator)

		self.add_widget(self._header)
		self.add_widget(self._table_view)
		self.add_widget(self._pagination)

