import requests

class APIDriver:
    def __init__(self, base_url, headers=None):
        self.session = requests.Session()  # Maintains session for efficiency
        self.session.headers.update(headers or {})  # Set headers
        self.base_url = base_url

    def request(self, method, endpoint, params=None):
        """Generic method to make API requests."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, params=params)
        return response



class ApiCalls:
    def __init__(self, base_url, api_key):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "ZSESSIONID": api_key
        }
        self.api_driver = APIDriver(base_url, headers)

    def get_user_info(self, first_name, last_name):
        """Fetch user reference based on first and last name."""
        query = f"((FirstName = {first_name}) AND (LastName = {last_name}))"
        response = self.api_driver.request("GET", "", params={"query": query})

        try:
            return response.json()["Query Result"]["Results"][0]["_ref"]
        except (IndexError, KeyError):
            return "User not found"



from concurrent.futures import ThreadPoolExecutor

def fetch_user(api, first_name, last_name):
    return api.get_user_info(first_name, last_name)

base_url = "https://api.example.com"
api_key = "your_api_key_here"
api = ApiCalls(base_url, api_key)

# User details to fetch in parallel
user_list = [("John", "Doe"), ("Alice", "Smith"), ("Bob", "Brown")]

# Execute API calls in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(lambda user: fetch_user(api, *user), user_list)

print(list(results))
