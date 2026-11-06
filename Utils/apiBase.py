class APIUtils:

    def __init__(self, api_context):
        self.api = api_context

    def authenticate(self, endpoint, credentials):
        response = self.api.post(endpoint, data=credentials)

        if not response.ok:
            raise RuntimeError(
                f"Authentication failed: {response.status}"
            )

        return response