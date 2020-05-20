from aiogqlc import GraphQLClient
from kivy.storage import AbstractStore

from WIET_sourcing_app.models.user_profile import UserProfile

USER_INFO = """
query userInfo{
	me{
		name
		wietPoints
	}
}
"""


class UserService:
	_client: GraphQLClient
	_store: AbstractStore
	_user_info: UserProfile

	def __init__(self, client: GraphQLClient, store: AbstractStore) -> None:
		self._client = client
		self._store = store
		self._user_info = UserProfile("", 0)

	@property
	def user_info(self):
		return self._user_info

	async def update_reload_user_info(self):
		try:
			result = await self._client.execute(USER_INFO)
		except ValueError:
			print("Failed to update user info")
			return

		result = await result.json()

		if "errors" in result:
			print("Failed to update user info")
			return

		result = result["data"]["me"]
		self._user_info = UserProfile(result["name"], result["wietPoints"])
