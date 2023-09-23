
import requests 

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

def request_artist(token):
    url = "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb"

    header = {"Authorization" : f"Bearer  {token}"}

    artists = requests.get(url=url,
                                headers=header,
                                )
    
    print(artists.json())

if __name__ == '__main__':

    api_token = get_token()
    request_artist(api_token)
    # print(api_token)

