#Based on https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/uix/datatables.py
from typing import List, Dict

import rx
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, DictProperty, ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView


from WIET_sourcing_app.widgets.data_table.data_provider import DummyProvider, AbstractDataProvider
from WIET_sourcing_app.widgets.data_table.data_table_header import DataTableHeader
from WIET_sourcing_app.widgets.data_table.data_table_pagination import DataTablePagination
from WIET_sourcing_app.widgets.data_table.data_table_paginator import DataTablePaginator
from WIET_sourcing_app.widgets.data_table.data_table_row import DataTableRow

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
			
<DataTableView>
	orientation: "vertical"
	spacing: 40
	padding:10, 10
	space_x: self.size[0]/3
	effect_cls: "ScrollEffect"
	scroll_type: ['bars']
	
	DataTableRecycleLayout:
		id: table_layout
		orientation: "vertical"
		cols: root._cols
		default_size: None, dp(30)
		default_size_hint: 1, None
		size_hint: None, None
		cols_minimum: root._cols_minimum
		height: self.minimum_height
		width: self.minimum_width
	"""
)


class DataTableRecycleLayout(
	FocusBehavior, RecycleGridLayout
):
	pass


class DataTableView(RecycleView):
	_paginator: DataTablePaginator
	_data_provider: AbstractDataProvider
	_cols = NumericProperty()
	_cols_minimum = DictProperty()
	_parent = ObjectProperty()

	def __init__(
			self,
			paginator: DataTablePaginator,
			data_provider: AbstractDataProvider,
			cols_minimum: Dict,
			parent,
			**kwargs
	):
		super(DataTableView, self).__init__(**kwargs)
		self._paginator = paginator
		self._data_provider = data_provider
		self._cols = len(cols_minimum)
		self._cols_minimum = cols_minimum
		self.viewclass = DataTableRow
		self._parent = parent

		rx.Observable.combine_latest(
			self._paginator.page,
			self._paginator.page_size,
			lambda x, y: (x, y)
		).subscribe(self.update_data)

	def update_data(self, page_info):
		data = []
		start_element = page_info[0] * page_info[1]
		for i, row_data in enumerate(self._data_provider.get_page_rows(*page_info)):
			row_index = start_element + i
			data.append(
				{
					"text": str(row_index),
					"Index": row_index,
					"table": self
				}
			)

			for cell_data in row_data:
				data.append(
					{
						"text": str(cell_data),
						"Index": row_index,
						"table": self
					}
				)

		self.data = data


class DataTable(BoxLayout):
	_table_view: DataTableView
	_header: DataTableHeader
	_pagination: DataTablePagination
	paginator: DataTablePaginator
	data_provider: AbstractDataProvider = DummyProvider()

	def __init__(self, **kwargs):
		super(DataTable, self).__init__(**kwargs)
		self.register_event_type("on_row_press")
		self.paginator = DataTablePaginator()
		self._header = DataTableHeader(["No."] + self.data_provider.get_columns())
		self._table_view = DataTableView(self.paginator, self.data_provider, self._header.column_minimum, self)
		self._pagination = DataTablePagination(self.paginator)
		self.paginator.set_item_count(self.data_provider.get_row_count())

		self.add_widget(self._header)
		self.add_widget(self._table_view)
		self.add_widget(self._pagination)

	def on_row_press(self, *args):
		"""Called when a table row is clicked."""
		print(args[0].Index)

