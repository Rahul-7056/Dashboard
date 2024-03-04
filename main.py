import os
import base64
import streamlit as st
from config.dbConfig import db_config
from requests import post,get

client_id = os.environ['clientid']
client_secret = os.environ['clientsecret']

def get_token():
  auth_string = client_id + ":" + client_secret
  auth_bytes = auth_string.encode("utf-8")
  auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
  url = "https://accounts.spotify.com/api/token"
  headers = {
    "authorization": "Basic " + auth_base64,
    "content-type": "application/x-www-form-urlencoded"
  }
  data = {"grant_type":"client_credentials"}
  result = post(url, headers=headers, data=data)
  json_result = result.json()
  # output: access_token
  # {
  # "access_token":"BQC6mMNB5EdGtmgDkUOUVDXgGIQpXdOC6s4qLsJ8h9zQqE5EUCoNr49mHZbfSgLGrSb56wpdTn4zE7CyoAi348DPv29BhtuqKdYEg37D-ZbYrGhZTxE"
  # "token_type":"Bearer"
  # "expires_in":3600
  # }
  return json_result['access_token']

def get_auth_header(token):
  return {'Authorization': 'Bearer ' + token}

def search_for_artist(token,artist_name):
  url = "https://api.spotify.com/v1/search"
  headers = get_auth_header(token)
  query = f"?q={artist_name}&type=artist&limit=1"
  query_url = url + query
  result = get(query_url, headers=headers)
  json_result = result.json()
  items = json_result["artists"]["items"]
  if len(items)==0:
    st.write("no artist found")
    return None
  else:
    artist_id = items[0]["id"]
    return artist_id

def get_songs_by_artist(token,artist_id):
  url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
  headers = get_auth_header(token)
  result = get(url, headers=headers)
  final=result.json()['tracks']
  st.write(final)

def get_artist_info(token,artist_id):
  url=f"https://api.spotify.com/v1/artists/{artist_id}"
  headers = get_auth_header(token)
  result = get(url, headers=headers)
  final=result.json()
  # st.write(final)
  
token = get_token()
artist_id=search_for_artist(token, "lata mangeshkar")
get_songs_by_artist(token,artist_id)
get_artist_info(token,artist_id)
st.title("Streamlit on Replit")
text = db_config()

st.write(text)
st.write(artist_id)

