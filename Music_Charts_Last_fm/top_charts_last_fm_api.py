#Author: Jhoel Perez
#Date: 10/10/2022 
#Objective: Fetch info from last fm api to obtain dataset for data analysis
#Notes: 

#Dependencies 
from xdrlib import ConversionError
from dotenv import load_dotenv
from os import getcwd, environ, path
from time import sleep, time
import pandas as pd 
import requests

#single api request 
def last_fm_api(header,payload,key,sub_key):
    end_point = 'https://ws.audioscrobbler.com/2.0/'

    #perform request to host 
    response = None
    try:
        response = requests.get(end_point,headers=header,params=payload)
    except:
        return None,404

    #convert json to text
    obj = response.json()

    #empty response 
    if obj[key][sub_key] == []:
        print(f"\nEmpty records have been found at page {payload['page']}")
        return None,404

    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        #delay request for cache request API limit 
        sleep(0.25)

    return obj, response.status_code

#api paging requests
def last_fm_api_paging(max_pages,headers,payload, key, sub_key):
    results = [] 
    page = payload['page']

    while page <= max_pages:
        #assign page number to payload 
        payload['page'] = page

        #make request with page info 
        try:
            data, status = last_fm_api(headers,payload, key, sub_key)
        except:
            #if error occurs save fetched data
            return results

        #if request invalid stop loop 
        if status != 200:
            print(f"Somethig went wrong: Status {status}")
            break
        
        #Requesting current page number 
        print(f"{page}/{max_pages}")

        #append request 
        results.append(data)

        page += 1

    return results

def chose_top_chart_category():
    #display option to user 
    #LAST FM top chart available methods 
    '''
    ['tracks']['track']  'chart.gettoptracks'
    ['artists']['artist'] 'chart.gettopartists'
    ['tags']['tag'] 'chart.gettoptags'
    '''
    choice = 0
    method, key, sub_key, file_title= '','','',''

    while choice == 0:

        #display choice menu
        print("\n")
        print("Last FM API".center(30,'*'))
        print(f"1) Get Top Tracks\n2) Get Top Artists\n3) Get Top Tags\n\n")
        tmp_input = input("Choose option 1, 2 or 3 : ")

        try: 

            choice = int(tmp_input)

            if choice == 1: 
                method = 'chart.gettoptracks'
                key = 'tracks'
                sub_key = 'track'
                file_title = 'Chart_tracks_Lastfm.csv'

            elif choice == 2: 
                method = 'chart.gettopartists'
                key = 'artists'
                sub_key = 'artist'
                file_title = 'Chart_artists_Lastfm.csv'

            elif choice == 3: 
                method = 'chart.gettoptags'
                key = 'tags'
                sub_key = 'tag'
                file_title = 'Chart_tags_Lastfm.csv'

            else: 
                raise ConversionError("Invalid option!")

        #error for options out of bounds 
        except:

            print("Invalid input, only valid options are 1, 2, or 3 ")
            sleep(2)
            choice = 0 

    return method,key, sub_key, file_title


if __name__ == "__main__":

    #let user select info Chart
    method, key, sub_key,file_dump = chose_top_chart_category()

    #load environment variables 
    env_file = f"{getcwd()}\API_key.env"

    if path.exists(env_file):
        #load environment variables 
        load_dotenv(env_file)

        API_key = environ.get("API_key")
        API_secret = str(environ.get("API_Shared_secret"))

        #API request info
        header ={
            'user-agent': 'Dataquest'
        }

        payload = {
            'api_key': API_key,
            'method': method,
            'format': 'json',
            'page': 1
        } 

        all_data = []

        #start timer for metrics
        time_start = time()

        try:
            #get max num of pages 
            pages, status = last_fm_api(header, payload, key, sub_key)

            #get number of pages available
            max_pages = int(pages[key]['@attr']['totalPages'])

            print(f"total pages: {max_pages}")

            #make cached requests 
            print(f"Requesting {method} from Last FM API ...\n")
            all_data = last_fm_api_paging(max_pages,header, payload, key, sub_key)

        except ConnectionError as ex:
            print(f"Oops Error establishing connection!")

        except Exception as ex: 
            print(f"Oops error has occured! {ex}")

        finally:
            if all_data != []:

                #convert data to Data Frame 
                frames = [pd.DataFrame(r[key][sub_key]) for r in all_data]

                #combine all request into one frame
                artists = pd.concat(frames)
                
                #save dataframe to csv 
                artists.to_csv(f'{getcwd()}\{file_dump}')

                print(f"Records have been saved to file {file_dump} on this directory {getcwd()}")

            else:
                print("No Records retrieved! ")

            #calculate requests time elapsed in minutes
            time_f = (time()-time_start)/60
            print(f"Time elapsed {round(time_f,2)} minutes! ")

    else: 
        print("invalid environment file...")