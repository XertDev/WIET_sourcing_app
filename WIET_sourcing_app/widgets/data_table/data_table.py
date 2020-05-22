#Based on https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/uix/datatables.py
import rx
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tooltip import MDTooltip

from WIET_sourcing_app.widgets.data_table.data_provider import DummyProvider, AbstractDataProvider
from WIET_sourcing_app.widgets.data_table.data_table_paginator import DataTablePaginator

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

<DataTablePagination>
	adaptive_height: True
	spacing: "8dp"
	
	Widget:
	
	MDLabel:
		text: "Rows per page"
		size_hint: None, 1
		width: self.texture_size[0]
		text_size: None, None
		font_style: "Caption"
		
	MDDropDownItem:
		id: item_per_page
		pos_hint: {"center_y": .5}
		font_size: "14sp"
		on_release: root._pagination_menu.open()
	
	MDLabel:
		id: label_items_per_page
		size_hint: None, 1
		text_size: None, None
		font_style: "Caption"
	
	MDIconButton:
		id: back_button
		icon: "chevron-left"
		user_font_size: "20sp"
		pos_hint: {"center_y": .5}
		disabled: True
	
	MDIconButton:
		id: forward_button
		icon: "chevron-right"
		user_font_size: "20sp"
		pos_hint: {"center_y": .5}

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


class DataTablePagination(ThemableBehavior, MDBoxLayout):
	_paginator: DataTablePaginator
	_pagination_menu: MDDropdownMenu

	def __init__(self, paginator: DataTablePaginator, **kwargs):
		super().__init__(**kwargs)
		self._paginator = paginator
		self._page_obs = self._paginator.page_size.subscribe(self.update_page_size_label)
		self._range_obs = rx.Observable.combine_latest(
			self._paginator.page,
			self._paginator.page_size,
			self._paginator.item_count,
			lambda a, b, c: (a, b, c)
		).subscribe(self.update_page_range)

		Clock.schedule_once(self.create_pagination_menu, 0.5)

	def update_page_range(self, start_count):
		start = start_count[0] * start_count[1]
		items_count = start_count[2]
		end = min(start + start_count[1], items_count)
		if end == items_count:
			self.ids.forward_button.disabled = True
		self.ids.label_items_per_page.text = f"{start}-{end} of {items_count}"

	def update_page_size_label(self, page_size: int):
		self.ids.item_per_page.text = str(page_size)

	def create_pagination_menu(self, interval):
		items = [
			{"text": f"{i}"} for i in [5, 10, 20, 50]
		]
		self._pagination_menu = MDDropdownMenu(
			caller=self.ids.item_per_page,
			items=items,
			use_icon_item=False,
			position="auto",
			max_height="140dp",
			width_mult=2
		)

	def __del__(self):
		self._page_obs.dispose()
		self._range_obs.dispose()


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

