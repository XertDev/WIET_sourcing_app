from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem

Builder.load_string("""
<WIETMenuItem>
	_txt_top_pad: "8dp"
	_txt_bot_pad: "16dp"
	on_release: root.parent.parent.parent.parent.dispatch("on_dismiss")

""")


class WIETMenuItem(OneLineListItem):
	icon = StringProperty()

