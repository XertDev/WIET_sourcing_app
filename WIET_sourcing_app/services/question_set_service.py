from typing import List

from aiogqlc import GraphQLClient
from kivy.storage import AbstractStore

from WIET_sourcing_app.models.question_set_info import QuestionSetInfo
from WIET_sourcing_app.models.question import QuestionInfo

ALL_QUESTION_SETS = """
query AllQuestionSets{
	allQuestionSets{
		edges{
			node{
				id
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

QUESTION_SET_COUNT = """
query TotalQuestionCount{
	allQuestionSets{
		totalCount
	}
}"""
QUERY_SET_QUESTIONS = """
{
	questionSet(id:"%s"){
	    questions{
      		edges{
        		node{
        		    id
          			question{
          			    __typename
          			}
          	    }    
            }
        }
    }
}"""


class QuestionSetService:
	_client: GraphQLClient
	_store: AbstractStore

	def __init__(self, client: GraphQLClient, store: AbstractStore) -> None:
		self._client = client
		self._store = store

	async def query_question_set_count(self) -> int:
		try:
			result = await self._client.execute(QUESTION_SET_COUNT)
		except ValueError:
			print("Failed to query question set count")
			return 0

		result = await result.json()

		if "errors" in result:
			print("Failed to query question set count")
			return 0

		result = result["data"]["allQuestionSets"]

		return result["totalCount"]

	async def query_question_sets(self) -> List[QuestionSetInfo]:
		try:
			result = await self._client.execute(ALL_QUESTION_SETS)
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
				node["id"],
				node["name"],
				node["details"],
				node["closeDate"],
				node["questionCount"],
			))
		return sets

	async def get_set_questions(self, set_id) -> List[QuestionInfo]:
		try:
			result = await self._client.execute(QUERY_SET_QUESTIONS % set_id)
		except ValueError:
			print("Failed to query set questions")
			return []

		result = await result.json()

		if "errors" in result:
			print("Failed to query set questions")
			return []

		result = result["data"]["questionSet"]["questions"]
		questions = []
		for edge in result["edges"]:
			node = edge["node"]
			questions.append(QuestionInfo(
				node["id"],
				node["question"]["__typename"]
			))
		return questions

