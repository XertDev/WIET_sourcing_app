from typing import List, Any

from kivy.app import App

from WIET_sourcing_app.models.question_set_info import QuestionSetInfo
from WIET_sourcing_app.widgets.data_table.data_provider import AbstractDataProvider


class QuestionSetListProvider(AbstractDataProvider):
	async def get_page_rows(self, page_num: int, size: int, query: str) -> List[Any]:
		app = App.get_running_app()
		raw_rows: List[QuestionSetInfo] = await app.question_set_service.query_question_sets(query)
		return [(row.id, (row.name, row.question_count)) for row in raw_rows]

	def get_columns(self) -> List[str]:
		return ["Nazwa        ", "Liczba pytań"]

	async def get_row_count(self) -> int:
		app = App.get_running_app()
		return await app.question_set_service.query_question_set_count()
