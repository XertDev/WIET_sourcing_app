from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.theming import ThemableBehavior

Builder.load_string("""
<DataTableRow>
	orientation: "vertical"

	MDBoxLayout:
		id: box
		padding: "8dp", "8dp", 0, "8dp"
		spacing: "16dp"
		height: index_label.texture_size[1]
		
		MDLabel:
			id: index_label
			size_hint_y: None
			text: root.text
			height: self.texture_size[1]
	MDSeparator:
"""	)


class DataTableRow(ThemableBehavior, RecycleDataViewBehavior, ButtonBehavior, BoxLayout):
	text = StringProperty()
	index = None
	table = ObjectProperty()

	def refresh_view_attrs(self, table_data, index, data):
		self.index = index
		return super().refresh_view_attrs(table_data, index, data)

	def on_touch_down(self, touch):
		if super().on_touch_down(touch):
			if self.table._parent:
				self.table._parent.dispatch("on_row_press", self)
			return True

