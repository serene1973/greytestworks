import requests

class APIDriver:
    _session = requests.Session()  # Using session to maintain headers and base URL

    def __init__(self, base_uri, headers=None):
        self.base_uri = base_uri
        self.headers = headers or {}
        self.query_params = {}

        # Set headers at session level
        self._session.headers.update(self.headers)

    def set_query_params(self, query_params):
        """Sets query parameters for the API request."""
        self.query_params = query_params
        return self

    def request_builder(self, method="GET", endpoint=""):
        """Builds and sends an API request."""
        url = f"{self.base_uri}/{endpoint}"
        
        response = self._session.request(method, url, params=self.query_params)

        return response



class ApiCalls:
    def __init__(self, base_uri, api_key):
        self.base_uri = base_uri
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "ZSESSIONID": api_key
        }

    def get_user_info(self, first_name, last_name):
        """Fetch user details based on first and last name."""
        query = f"((FirstName = {first_name}) AND (LastName = {last_name}))"
        query_params = {"query": query}

        api_driver = APIDriver(self.base_uri, self.headers)
        response = api_driver.set_query_params(query_params).request_builder()

        if response.status_code == 200:
            try:
                ref_user = response.json()["Query Result"]["Results"][0]["_ref"]
                return ref_user
            except (IndexError, KeyError):
                return "User not found"
        else:
            return f"API Error: {response.status_code}, {response.text}"


base_url = "https://api.example.com"
api_key = "your_api_key_here"

api = ApiCalls(base_url, api_key)
user_ref = api.get_user_info("John", "Doe")
print(user_ref)


