#Author: Jhoel Perez
#Date: 10/10/2022 
#Objective: Fetch info from last fm api to obtain dataset for data analysis
#Notes: 

#Dependencies 
from dotenv import load_dotenv
from os import getcwd, environ, path
from time import sleep, time
import pandas as pd 
import requests, json


if __name__ == "__main__":
    #load environment variables 
    env_file = f"{getcwd()}\API_key.env"

    if path.exists(env_file):
        #load environment variables 
        load_dotenv(env_file)

        API_key = environ.get("API_key")
        API_secret = str(environ.get("API_Shared_secret"))

        #single api request 
        def last_fm_api(header,payload):
            end_point = 'https://ws.audioscrobbler.com/2.0/'

            response = requests.get(end_point,headers=header,params=payload)

            #raise exception if request invalid 
            response.raise_for_status()

            #convert json to text 
            obj = response.json()
            # text = json.dumps(obj, sort_keys=True, indent=4)
            # data= json.loads(text)

            result = obj
            # result = data['artists'][attribute]

            # if it's not a cached result, sleep
            if not getattr(response, 'from_cache', False):
                sleep(0.25)

            return result, response.status_code

        #api paging requests
        def last_fm_api_paging(max_pages,headers,payload):
            results = [] 
            page =1


            while page <= max_pages:
                #assign page number to payload 
                payload['page']:page

                print(f"Requesting page {page}/{max_pages}")

                #make request with page info 
                data, status = last_fm_api(headers,payload)

                #if request invalid stop loop 
                if status != 200:
                    break

                #append request 
                results.append(data)

                page += 1

                #delay request for cache request API limit 
                # sleep(0.25)

            return results

        #API request 
        header ={
            'user-agent': 'Dataquest'
        }

        payload = {
            'api_key': API_key,
            'method': 'chart.gettopartists',
            'format': 'json'
        }

        #api request time elapsed 
        time_start = time()

        #get max num of pages 
        pages, status = last_fm_api(header, payload)
        max_pages = int(pages['artists']['@attr']['totalPages'])

        print(f"total pages: {max_pages}")

        #make cached requests 
        all_data = last_fm_api_paging(max_pages,header, payload)
        # all_data = last_fm_api_paging(max_pages,header, payload,'artists')

        #convert data to Data Frame 
        frames = [pd.DataFrame(r['artists']['artist']) for r in all_data]

        #combine all request into one frame
        artists = pd.concat(frames)
        
        #save dataframe to csv 
        artists.to_csv(f'{getcwd()}\Chart_artists_Lastfm.csv')

        #time elapsed total 
        print(f"{time()-time_start}")

    else: 
        print("invalid environment file...")