import rx
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from WIET_sourcing_app.widgets.data_table.data_table_paginator import DataTablePaginator
from WIET_sourcing_app.widgets.drop_down.drop_down_menu import WIETDropdownMenu

Builder.load_string("""
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
		on_release: root._paginator.prev_page()
	
	MDIconButton:
		id: forward_button
		icon: "chevron-right"
		user_font_size: "20sp"
		pos_hint: {"center_y": .5}
		on_release: root._paginator.next_page()

""")


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
		else:
			self.ids.forward_button.disabled = False

		if start == 0:
			self.ids.back_button.disabled = True
		else:
			self.ids.back_button.disabled = False

		self.ids.label_items_per_page.text = f"{start}-{end} of {items_count}"

	def update_page_size_label(self, page_size: int):
		self.ids.item_per_page.text = str(page_size)

	def create_pagination_menu(self, interval):
		items = [
			{
				"text": f"{i}"
			} for i in [5, 10, 20, 50]
		]
		self._pagination_menu = WIETDropdownMenu(
			caller=self.ids.item_per_page,
			items=items,
			position="auto",
			max_height="140dp",
			callback=self.set_page_size,
			use_icon_item=False,
			width_mult=1
		)

	def set_page_size(self, instance_menu_item):
		item_page_count = int(instance_menu_item.text)
		self._paginator.set_page_size(item_page_count)

	def __del__(self):
		self._page_obs.dispose()
		self._range_obs.dispose()
