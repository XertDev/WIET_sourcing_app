from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tooltip import MDTooltip

Builder.load_string("""
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
""")


class DataTableCellHeader(MDTooltip, BoxLayout):
	text = StringProperty()
