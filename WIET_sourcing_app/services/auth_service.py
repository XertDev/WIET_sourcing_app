from aiogqlc import GraphQLClient

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

BACKEND_URL = 'http://wiet-sourcing.herokuapp.com/graphql'


class AuthService:
	_client: GraphQLClient

	def __init__(self) -> None:
		self._client = GraphQLClient(BACKEND_URL)

	async def sign_in(self, email: str, password: str) -> bool:
		payload = {"email": email, "password": password}
		try:
			result = await self._client.execute(SIGN_IN_MUTATION, payload)
		except Exception as e:
			print(e)
			return False
		result = await result.json()

		if "errors" in result:
			return False
		result = result["data"]

		auth = 'Bearer {}'.format(result["signIn"]["token"])

		self._client.headers["Authorization"] = auth

		return True

	async def sign_up(self, name: str, email: str, password: str) -> bool:
		payload = {"name": name, "email": email, "password": password}
		try:
			result = await self._client.execute(SIGN_UP_MUTATION, payload)
		except Exception as e:
			print(e)
			return False

		result = await result.json()
		if "errors" in result:
			return False

		return True
