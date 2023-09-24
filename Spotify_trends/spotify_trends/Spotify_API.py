import requests 
import pprint
'''
feature playlist = https://developer.spotify.com/documentation/web-api/reference/get-featured-playlists
playlist = https://developer.spotify.com/documentation/web-api/reference/get-playlist
'''
client_id = ""
client_secret = ""

def get_token():
    token = "" 

    url = "https://accounts.spotify.com/api/token"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    body = { "grant_type": 'client_credentials',
            'client_id':f'{client_id}',
            'client_secret':f'{client_secret}'}

    try:

        get_token = requests.post(url=url,
                                headers=headers,
                                data=body
                                )
        
        get_token.raise_for_status()

        response = get_token.json()

        token = response['access_token']
        token_type = response['token_type']
        expires_in = response['expires_in']

        print(f"{token_type} expires in {expires_in} seconds")
        return token
    
    #TODO: change to HTTPError exception
    except Exception as e: 
        print("not 200 response")

def request_playlist(header, playlist_id):
    
    # playlist_id = "0sdmbRcjAGi0nmLTjn87lV?si"

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    playlist = requests.get(url=url,
                            headers=header,
                            )
    response = playlist.json()
    print(response['name'])
    print(response['followers']['total'])
    # print(response['tracks']['items'])

def request_featured_playlists(header,country_code):

    limit = 4
    # country_code = "SA"

    url = f"https://api.spotify.com/v1/browse/featured-playlists?limit={limit}&country={country_code}"
    playlists = requests.get(url=url,
                            headers=header,
                            )
    
    response = playlists.json()

    playlists_id = []

    for song in response['playlists']['items']:
        # print(song['name'])
        # print(song['id'])
        # print(song['href'])
        # print('-'*20)
        playlists_id.append(song['id'])

    return playlists_id


if __name__ == '__main__':

    api_token = get_token()
    header = {"Authorization" : f"Bearer  {api_token}"}


    # request_playlist(api_token, header)
    country_code = ['SA']

    for country in country_code:
        playlist_id = request_featured_playlists(header, country)
        # print(f"SA {playlist_id}")

    request_playlist(header,playlist_id[0])

