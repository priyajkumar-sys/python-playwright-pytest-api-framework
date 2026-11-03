class APIUtils:

    def __init__(self, api_context):
        self.api = api_context

    def authenticate(self, credentials):
        response = self.api.post("/auth", data=credentials)

        if response.status != 200:
            raise RuntimeError("Authentication request failed")

        data = response.json()

        if "token" not in data:
            raise RuntimeError("Authentication token missing")

        return {"Cookie": f"token={data['token']}"}