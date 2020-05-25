from datetime import datetime, timedelta
from typing import Optional

from aiogqlc import GraphQLClient
from kivy.storage import AbstractStore

SIGN_IN_MUTATION = """
mutation SignIn($email: String!, $password: String!){
	signIn(email: $email, password: $password)
	{
		token
	}
}
"""

SIGN_UP_MUTATION = """
mutation SignUp($name: String!, $email: String!, $password: String!){
	signUp(name: $name, email: $email, password: $password)
	{
		userProfile
		{
			id
		}
	}
}
"""

REFRESH_TOKEN = """
mutation RefreshToken{
	refreshSignIn{
		token
	}
}
"""

BACKEND_URL = 'http://wiet-sourcing.herokuapp.com/graphql'

AUTH_TOKEN_KEY = "AUTH_TOKEN"


class AuthService:
	_client: GraphQLClient
	_store: AbstractStore

	def __init__(self, store: AbstractStore) -> None:
		self._client = GraphQLClient(BACKEND_URL)
		self._store = store

	async def sign_in(self, email: str, password: str) -> bool:
		payload = {"email": email, "password": password}
		try:
			result = await self._client.execute(SIGN_IN_MUTATION, payload)
		except ValueError as e:
			print(e)
			return False
		result = await result.json()

		if "errors" in result:
			return False
		result = result["data"]

		auth = 'Bearer {}'.format(result["signIn"]["token"])

		self._client.headers["Authorization"] = auth
		self._store.put(
			AUTH_TOKEN_KEY,
			value=auth
		)

		return True

	async def sign_up(self, name: str, email: str, password: str) -> bool:
		payload = {"name": name, "email": email, "password": password}
		try:
			result = await self._client.execute(SIGN_UP_MUTATION, payload)
		except ValueError:
			return False

		result = await result.json()
		if "errors" in result:
			return False

		return True

	async def refresh_token(self) -> Optional[str]:
		try:
			result = await self._client.execute(REFRESH_TOKEN)
		except ValueError:
			return None

		result = await result.json()
		if "errors" in result:
			return None
		result = result["data"]

		return 'Bearer {}'.format(result["refreshSignIn"]["token"])

	async def load_auth_token_from_store(self) -> bool:
		if not self._store.exists(AUTH_TOKEN_KEY):
			return False

		auth = self._store.get(AUTH_TOKEN_KEY)["value"]
		self._client.headers["Authorization"] = auth

		token = await self.refresh_token()
		if not token:
			self._store.delete(AUTH_TOKEN_KEY)
			return False

		self._client.headers["Authorization"] = token

		self._store.put(
			AUTH_TOKEN_KEY,
			value=token
		)

		return True

	def sign_out(self):
		self._store.delete(AUTH_TOKEN_KEY)
		if self._client.headers['Authorization'] is not None:
			del self._client.headers["Authorization"]

	@property
	def client(self) -> GraphQLClient:
		return self._client

