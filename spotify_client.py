#!.venv/bin/python
import spotipy
from configparser import ConfigParser
from spotipy.oauth2 import SpotifyOAuth

DISCOVER_WEEKLY_ID = '37i9dQZEVXcJBxdUAjiLxu'

# Create a SpotifyOAuth object
class SpotifyClient:

    def __init__(self, client_id, client_secret, redirect_uri):
        sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-library-read playlist-read-private")
        # Authenticate and create a Spotify client
        self.sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Function to retrieve user's playlists
    def get_user_playlists(self):
        playlists = self.sp.current_user_playlists()
        return playlists['items']

    # Function to retrieve tracks from a specific playlist
    def get_playlist_tracks(self, playlist_id):
        tracks = self.sp.playlist_tracks(playlist_id, limit=50, offset=0)
        return tracks['items']

    # Function to create a new playlist with given tracks
    def create_playlist(self, user_id, name, track_ids):
        playlist = self.sp.user_playlist_create(user_id, name)
        self.sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)
        return playlist

    def get_saved_tracks(self):
        saved_tracks = self.sp.current_user_saved_tracks(limit=50, offset=0)
        return saved_tracks['items']


if __name__ == "__main__":
    config = ConfigParser()
    config.read('settings.conf')
    client = SpotifyClient(config['GENERAL']['CLIENT_ID'], config['GENERAL']['CLIENT_SECRET'], config['GENERAL']['REDIRECT_URI'])

    # Retrieve and print user's playlists
    playlists = client.get_user_playlists()
    print("\nUser's playlists - ")
    for playlist in playlists:
        print(f"Playlist: {playlist['name']} (ID: {playlist['id']})")
    
    # Get tracks from the Discover Weekly playlist, and print
    print("\nTracks in Discover Weekly - ")
    tracks = client.get_playlist_tracks(DISCOVER_WEEKLY_ID)
    for track in tracks:
        print(f"- {track['track']['name']} by {track['track']['artists'][0]['name']}")

    sorted_tracks = sorted(tracks, key=lambda x: x['track']['popularity'], reverse=True)

    # Get and print the users saved tracks.
    saved_tracks = client.get_saved_tracks()
    print("\nSaved Tracks - ")
    for track in saved_tracks:
        print(f"- {track['track']['name']} by {track['track']['artists'][0]['name']}")
