import requests
import os   
from dotenv import load_dotenv

load_dotenv()
CAT_API_KEY= os.getenv('CAT_API_KEY')

def getCatPicture():
    params={
        "limit":2,
        "has_breeds":1,
    }
    headers = {
        "x-api-key": CAT_API_KEY
    }
    r = requests.get("https://api.thecatapi.com/v1/images/search", params= params, headers=headers)
    data = r.json()[0]
    response={}
    response["breed"]=data["breeds"][0]["name"]
    response["description"]=data["breeds"][0]["description"]
    response["imageURL"]=data["url"]
    return response