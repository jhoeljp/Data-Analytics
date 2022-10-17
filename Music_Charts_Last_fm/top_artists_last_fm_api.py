#Author: Jhoel Perez
#Date: 10/10/2022 
#Objective: Fetch info from last fm api to obtain dataset for data analysis
#Notes: 

#Dependencies 
from dotenv import load_dotenv
from os import getcwd, environ, path
from time import sleep, time
import pandas as pd 
import requests

#single api request 
def last_fm_api(header,payload):
    end_point = 'https://ws.audioscrobbler.com/2.0/'

    #perform request to host 
    response = None
    try:
        response = requests.get(end_point,headers=header,params=payload)
    except:
        return None,404

    #convert json to text
    obj = response.json()
    
    # text = json.dumps(obj, sort_keys=True, indent=4)
    # data= json.loads(text)

    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        #delay request for cache request API limit 
        sleep(0.25)

    return obj, response.status_code

#api paging requests
def last_fm_api_paging(max_pages,headers,payload):
    results = [] 
    page = payload['page']

    while page <= max_pages:
        #assign page number to payload 
        payload['page'] = page

        #make request with page info 
        try:
            data, status = last_fm_api(headers,payload)
        except:
            #if error occurs save fetched data
            return results

        #if request invalid stop loop 
        if status != 200:
            print(f"somethig went wrong: Status {status}")
            break
        
        # print(f"Requesting page {page}/{max_pages}")
        print(f"{page}/{max_pages}")

        #append request 
        results.append(data)

        page += 1

    return results

if __name__ == "__main__":
    #load environment variables 
    env_file = f"{getcwd()}\API_key.env"

    if path.exists(env_file):
        #load environment variables 
        load_dotenv(env_file)

        API_key = environ.get("API_key")
        API_secret = str(environ.get("API_Shared_secret"))

        #API request 
        header ={
            'user-agent': 'Dataquest'
        }

        payload = {
            'api_key': API_key,
            'method': 'chart.gettopartists',
            'format': 'json',
            'page': 1
        } 

        all_data = []
        time_start = time()

        try:
            #get max num of pages 
            pages, status = last_fm_api(header, payload)

            max_pages = int(pages['artists']['@attr']['totalPages'])
            # max_pages = 10000

            print(f"total pages: {max_pages}")

            #make cached requests 
            
            all_data = last_fm_api_paging(max_pages,header, payload)

        except ConnectionError as ex:
            print(f"Oops Error establishing connection!")

        except Exception as ex: 
            print(f"Oops error has occured! {ex}")

        finally:
            if all_data != []:

                #convert data to Data Frame 
                frames = [pd.DataFrame(r['artists']['artist']) for r in all_data]

                #combine all request into one frame
                artists = pd.concat(frames)
                
                #save dataframe to csv 
                artists.to_csv(f'{getcwd()}\Chart_artists_Lastfm.csv')

            else:
                print("No Records retrieved! ")

            time_f = (time()-time_start)/60
            print(f"Time elapsed {round(time_f,2)} minutes! ")

    else: 
        print("invalid environment file...")