import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("Spotify credential not found in .env file")
    
    client_credentials_manager = SpotifyClientCredentials(
        cliend_id=client_id,
        client_secret=client_secret
    )

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
