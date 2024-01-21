import requests
import os   
from dotenv import load_dotenv
import random

load_dotenv()
CAT_API_KEY= os.getenv('CAT_API_KEY')

breedIds=['abys', 'aege', 'abob', 'acur', 'asho', 'awir', 'amau', 'amis', 'bali', 'bamb', 'beng', 'birm', 'bomb', 'bslo', 'bsho', 'bure', 'buri', 'cspa', 'ctif', 'char', 'chau', 'chee', 'csho', 'crex', 'cymr', 'cypr', 'drex', 'dons', 'lihu', 'emau', 'ebur', 'esho', 'hbro', 'hima', 'jbob', 'java', 'khao', 'kora', 'kuri', 'lape', 'mcoo', 'mala', 'manx', 'munc', 'nebe', 'norw', 'ocic', 'orie', 'pers', 'pixi', 'raga', 'ragd', 'rblu', 'sava', 'sfol', 'srex', 'siam', 'sibe', 'sing', 'snow', 'soma', 'sphy', 'tonk', 'toyg', 'tang', 'tvan', 'ycho']

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

def processData(data):
    response=[]
    for cat in data:
        catData={}
        catData["breed"]=cat["breeds"][0]["name"]
        catData["description"]=cat["breeds"][0]["description"]
        catData["imageURL"]=cat["url"]
        response.append(catData)
    return response

def getCatPictureAdv(quantity,diff_breeds=False):
    params={
        "limit":quantity,
        "has_breeds":1,
    }
    headers = {
        "x-api-key": CAT_API_KEY
    }
    if diff_breeds:
        chosenBreeds=[]
        while len(chosenBreeds)!= quantity+1:
            randomNum=breedIds[random.randint(0,len(breedIds)-1)]
            if randomNum not in chosenBreeds:
                chosenBreeds.append(randomNum)
        params["limit"]=1
        response=[]
        for breed in chosenBreeds:
            params["breed_ids"]= breed
            r = requests.get("https://api.thecatapi.com/v1/images/search", params= params, headers=headers)
            data = r.json()
            response.append(processData(data))
            
    else:
        params["breed_ids"]= breedIds[random.randint(0,len(breedIds)-1)]
        r = requests.get("https://api.thecatapi.com/v1/images/search", params= params, headers=headers)
        data = r.json()
        response=processData(data)
    return response

def getCatBreeds():
    r = requests.get("https://api.thecatapi.com/v1/breeds")
    data = r.json()
    breedId=[]
    for breed in data:
        breedId.append(breed["id"])
    return breedId

if __name__=="__main__":
   response= getCatPicture(3,False)
   #response= getCatBreeds()
   print(response)