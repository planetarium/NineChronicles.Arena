import requests


def execute_gql(url: str, query: str):
    resp = requests.post(url, json={"query": query})
    if resp.status_code != 200:
        raise Exception(f"Request failed with status code: {resp.status_code}")
    resp = resp.json()
    if "errors" in resp:
        raise Exception(f"GQL Failed: {resp['errors']}")
    return resp["data"]
