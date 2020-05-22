from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, DictProperty
from kivy.uix.scrollview import ScrollView

from WIET_sourcing_app.widgets.data_table.data_table_cell_header import DataTableCellHeader

Builder.load_string("""
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
"""
)


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
				self.ids.first_cell.width = self.column_minimum[i]

		self.ids.header.cols_minimum = self.column_minimum
