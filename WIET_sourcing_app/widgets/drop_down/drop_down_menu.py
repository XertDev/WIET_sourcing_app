from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu, MDMenuItemIcon, RightContent, MDMenuItem

from WIET_sourcing_app.widgets.drop_down.menu_item import WIETMenuItem


class WIETDropdownMenu(MDDropdownMenu):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def create_menu_items(self):
		"""Creates menu items."""

		if self.use_icon_item:
			item_cls = MDMenuItemIcon
		else:
			item_cls = WIETMenuItem

		for data in self.items:
			item = item_cls(
				text=data.get("text", ""),
				icon=data.get("icon", ""),
				divider=data.get("divider", "Full"),
			)
			if self.callback:
				item.bind(on_release=self.callback)
			right_content_cls = data.get("right_content_cls", None)
			# Set right content.
			if isinstance(right_content_cls, RightContent):
				item.ids._right_container.width = right_content_cls.width + dp(
					20
				)
				item.ids._right_container.padding = ("10dp", 0, 0, 0)
				item.add_widget(right_content_cls)
			else:
				if "_right_container" in item.ids:
					item.ids._right_container.width = 0
			self.menu.ids.box.add_widget(item)
