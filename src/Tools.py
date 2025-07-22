import requests
from typing import List
import os
from config import Config

def GoogleSearch(query : str, search_api_key : str, cse_id : str) :
    endpoint_url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={cse_id}&q={query}"
    response = requests.get(endpoint_url)
    return response.json()["items"]


def Search(query : str) -> List[dict]:
    """
    Searches the query over internet and returns back the result.

    Arguments:
        query(str): query is what to be searched over the internet.

    Results:
        returns a json object consisting of url and content.
    """
    search_api_key = Config.SEARCHAPI_API_KEY
    cse_id         = Config.CSE_ID
    result = GoogleSearch(query,search_api_key, cse_id)
    response = []
    for res in result:
        link = res["link"]
        response.append(
            {
                'url':link,
                 'content': res['snippet']
            }
            )
    return response

class DeepResearch:
    pass