#Based on https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/uix/datatables.py
import abc
from typing import List, Any, NamedTuple

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ListProperty, StringProperty, DictProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.tooltip import MDTooltip

from WIET_sourcing_app.widgets.data_provider import DummyProvider, AbstractDataProvider

Builder.load_string(
	"""
<DataTableCellHeader>
	orientation: "vertical"
	size_hint_y: None
	height: self.minimum_height
	spacing: "4dp"
	tooltip_text: root.text
	
	MDLabel:
		text: " " + root.text
		size_hint_y: None
		height: self.texture_size[1]
		bold: True
	
	MDSeparator:
		id: separator

<DataTableHeader>
	bar_width: 0
	do_scroll: False
	size_hint: 1, None
	height: header.height
	canvas:
		Color:
			rgba: rgba (1, 1, 1, 1)
		RoundedRectangle:
			pos: self.pos
			size: self.size
	
	MDGridLayout:
		id: header
		rows: 1
		adaptive_size: True
		padding: 0, "8dp", 0, 0
		
		MDBoxLayout:
			orientation: "vertical"
			
			MDBoxLayout:
				id: box
				padding: "8dp", "8dp", "4dp", 0
				spacing: "16dp"
				
				DataTableCellHeader:
					id: first_cell

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


class DataTableCellHeader(MDTooltip, BoxLayout):
	text = StringProperty()


class DataTableHeader(ScrollView):
	column_headings = ListProperty()
	column_minimum = DictProperty()

	def __init__(self, headings, **kwargs):
		super().__init__(**kwargs)
		self.column_headings = headings
		self.ids.header.cols = len(self.column_headings)
		for i, heading in enumerate(self.column_headings):
			self.column_minimum[i] = len(heading) * dp(20)
			if i:
				self.ids.header.add_widget(
					DataTableCellHeader(
						text=heading,
						width=self.column_minimum[i]
					)
				)
			else:
				self.ids.first_cell.text = heading
				self.ids.first_cell.ids.separator.height = 0
				self.ids.first_cell.width = self.column_minimum[i]

		self.ids.header.cols_minimum = self.column_minimum

class DataTableView(RecycleView):
	def __init__(self,  **kwargs):
		super(DataTableView, self).__init__(**kwargs)


class DataTable(BoxLayout):
	_table_view: DataTableView
	_header: DataTableHeader

	data_provider: AbstractDataProvider = DummyProvider()

	def __init__(self, **kwargs):
		super(DataTable, self).__init__(**kwargs)
		self._table_view = DataTableView()
		self._header = DataTableHeader(["No."] + self.data_provider.get_columns())
		self.add_widget(self._header)
		self.add_widget(self._table_view)


