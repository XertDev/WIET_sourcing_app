from typing import List

from aiogqlc import GraphQLClient
from kivy.storage import AbstractStore

from WIET_sourcing_app.models.question_set_info import QuestionSetInfo
from WIET_sourcing_app.models.question import QuestionInfo

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

QUERY_SET_QUESTIONS = """
{
	questionSet(id:"%s"){
	    questions{
      		edges{
        		node{
          			question{
              			__typename
            		}
          	    }    
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
			node = edge["node"]["question"]
			questions.append(QuestionInfo(
				node["__typename"],
			))
		return questions
