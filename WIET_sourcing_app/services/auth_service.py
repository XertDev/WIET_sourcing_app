from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

SIGN_IN_MUTATION = gql("""
mutation SignIn($email: String!, $password: String!){
	signIn(email: $email, password: $password)
	{
	success
	token
	}
}
""")

SIGN_UP_MUTATION = gql("""
mutation SignUp($name: String!, $email: String!, $password: String!){
	signUp(name: $name, email: $email, password: $password)
	{
		success
	}
}
""")

BACKEND_URL = 'https://wiet-sourcing.herokuapp.com/graphql'

class AuthService:
	def __init__(self) -> None:
		self._transport = RequestsHTTPTransport(
			url=BACKEND_URL,
			use_json=True
		)

		self._client = Client(
			transport=self._transport,
			fetch_schema_from_transport=True
		)

	def sign_in(self, email: str, password: str) -> bool:
		payload = {"email": email, "password": password}
		try:
			result = self._client.execute(SIGN_IN_MUTATION, payload)
		except Exception as e:
			print(e)
			return False

		if "signIn" not in result:
			return False

		if not result["signIn"]["success"]:
			print("Failed to login")
			return False

		self._transport = RequestsHTTPTransport(
			url=BACKEND_URL,
			use_json=True,
			headers={
				"Authorization": "Bearer " + result["signIn"]["token"]
			}
		)
		self._client = Client(
			transport=self._transport,
			fetch_schema_from_transport=True
		)
		return True

	def sign_up(self, name: str, email: str, password: str) -> bool:
		payload = {"name": name, "email": email, "password": password}
		try:
			result = self._client.execute(SIGN_UP_MUTATION, payload)
		except Exception as e:
			print(e)
			return False

		return "signUp" in result and result["signUp"]["success"]
