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


class AuthService:
	def __init__(self) -> None:
		self._transport = RequestsHTTPTransport(
			url='https://wiet-sourcing.herokuapp.com/graphql',
			use_json=True
		)

		self._client = Client(
			transport=self._transport,
			fetch_schema_from_transport=True
		)

	def sign_in(self, email: str, password: str) -> bool:
		payload = {"email": email, "password": password}
		print(payload)
		result = {}
		try:
			result = self._client.execute(SIGN_IN_MUTATION, payload)
		except Exception as e:
			print(e)

		if "signIn" not in result:
			return False

		if not result["signIn"]["success"]:
			print("Failed to login")
			# todo: error handling
			return False

		print(result["signIn"]["token"])
		return False
