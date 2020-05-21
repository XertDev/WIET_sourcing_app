from typing import List

from aiogqlc import GraphQLClient
from kivy.storage import AbstractStore

from WIET_sourcing_app.models.question_set_info import QuestionSetInfo

USER_INFO = """
query AllQuestionSets{
	allQuestionSets{
		edges{
			node{
				name
				details
				closeDate
				questionCount
				id
			}
		}
	}
}
"""


class QuestionSetService:
	_client: GraphQLClient
	_store: AbstractStore

	def __init__(self, client: GraphQLClient, store: AbstractStore) -> None:
		self._client = client
		self._store = store

	async def query_question_sets(self) -> List[QuestionSetInfo]:
		try:
			result = await self._client.execute(USER_INFO)
		except ValueError:
			print("Failed to query question sets")
			return []

		result = await result.json()

		if "errors" in result:
			print("Failed to query question sets")
			return []

		result = result["data"]["allQuestionSets"]
		sets = []
		for edge in result["edges"]:
			node = edge["node"]
			sets.append(QuestionSetInfo(
				node["name"],
				node["details"],
				node["closeDate"],
				node["questionCount"],
				node["id"]
			))
		return sets
