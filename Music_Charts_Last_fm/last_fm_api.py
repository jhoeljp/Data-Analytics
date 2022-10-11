#Author: Jhoel Perez
#Date: 10/10/2022 
#Objective: Fetch info from last fm api to obtain dataset for data analysis
#Notes: 

#Dependencies 
from dotenv import load_dotenv
from os import getcwd, environ, path
import requests, json, pprint

if __name__ == "__main__":
    print("t")

#load environment variables 
env_file = f"{getcwd()}\API_key.env"

if path.exists(env_file):
    load_dotenv(env_file)

    API_key = environ.get("API_key")
    API_secret = str(environ.get("API_Shared_secret"))

    #single api request 
    def last_fm_api(header,payload,attribute):
        end_point = 'https://ws.audioscrobbler.com/2.0/'

        response = requests.get(end_point,headers=header,params=payload)
        # print(response.status_code)
        response.raise_for_status()

        obj = response.json()
        text = json.dumps(obj, sort_keys=True, indent=4)
        data= json.loads(text)

        result = data['artists'][attribute]

        return result

    #api paging requests
    def last_fm_api_paging(max_page,headers,payload,att):
        results = [] 
        page =1


        while page < max_page:
            payload['page':page]
            data = last_fm_api(headers,payload,att)
            results.append(data)
            page += 1

    #API request 
    header ={
        'user-agent': 'Dataquest'
    }

    payload = {
        'api_key': API_key,
        'method': 'chart.gettopartists',
        'format': 'json'
    }

    #get max num of pages 
    pages = last_fm_api(header, payload,'@attr')
    max_pages = pages['totalPages']

    print(f"total pages: {max_pages}")

    # last_fm_api_paging(header, payload,'artists')

else: 
    print("invalid environment file...")
# for x in top_artists_data:
#     print(x['name'])