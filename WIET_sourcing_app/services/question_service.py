from typing import List

from aiogqlc import GraphQLClient
from kivy.storage import AbstractStore

from WIET_sourcing_app.models.question import QuestionInfo

QUERY_QUESTION = """
{
  question(id:"%s"){
    question{
      __typename,
      ...on %s
    }
  }
}
"""


class QuestionService:
    _client: GraphQLClient
    _store: AbstractStore

    def __init__(self, client: GraphQLClient, store: AbstractStore) -> None:
        self._client = client
        self._store = store

    async def get_question_union(self, que_id, on_query):
        try:
            result = await self._client.execute(QUERY_QUESTION % (que_id, on_query))
        except ValueError:
            print("Failed to query set questions")
            return None

        result = await result.json()

        if "errors" in result:
            print("Failed to query set questions")
            return None

        result = result["data"]["question"]["question"]
        return result
