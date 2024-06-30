#!.venv/bin/python
import spotipy
from configparser import ConfigParser
from spotipy.oauth2 import SpotifyOAuth
from random import randint

DISCOVER_WEEKLY_ID = '37i9dQZEVXcJBxdUAjiLxu'

SCOPES = 'user-library-read playlist-read-private playlist-modify-private'

# Create a SpotifyOAuth object
class SpotifyClient:

    def __init__(self, client_id, client_secret, redirect_uri):
        sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=SCOPES)
        # Authenticate and create a Spotify client
        self.sp = spotipy.Spotify(auth_manager=sp_oauth)
        self.user_id = self.sp.current_user()['id']

    # Function to retrieve user's playlists
    def get_user_playlists(self):
        return self.sp.current_user_playlists()['items']

    # Function to retrieve tracks from a specific playlist
    def get_playlist_tracks(self, playlist_id):
        return self.sp.playlist_tracks(playlist_id, limit=50, offset=0)['items']

    # Function to create a new playlist with given tracks
    def create_playlist(self, user_id, name, track_ids):
        playlist = self.sp.user_playlist_create(user_id, name)
        self.sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)
        return playlist

    def get_saved_tracks(self):
        return self.sp.current_user_saved_tracks(limit=50, offset=0)['items']

    def remove_playlist_tracks(self, playlist_id, track_ids):
        self.sp.user_playlist_remove_all_occurrences_of_tracks(self.user_id, playlist_id, track_ids)

    def get_recommendations(self, seed_tracks):
        return self.sp.recommendations(seed_tracks=seed_tracks, limit=30)['tracks']

    def replace_playlist_tracks(self, playlist_id, track_ids):
        self.sp.playlist_replace_items(playlist_id, track_ids)


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
    recommendation_seed_track_ids = []
    # Get the top 3 Ids fom the sorted tracks
    for i in range(3):
        recommendation_seed_track_ids.append(sorted_tracks[i]['track']['id'])

    # Get and print the users saved tracks.
    saved_tracks = client.get_saved_tracks()
    print("\nSaved Tracks - ")
    for track in saved_tracks:
        print(f"- {track['track']['name']} by {track['track']['artists'][0]['name']}")
    
    # Get two range tracks from the saved tracks
    for i in range(2):
        index = randint(0, len(saved_tracks) - 1)
        recommendation_seed_track_ids.append(saved_tracks[index]['track']['id'])

    print(f"\nRecommendation_seeds - {recommendation_seed_track_ids}")
    recommendations = client.get_recommendations(recommendation_seed_track_ids)
    print(f"\nRecommendations - {[track['name'] for track in recommendations]}")

    client.replace_playlist_tracks(config['GENERAL']['DISCOVER_DAILY_TARGET_ID'], [track['id'] for track in recommendations])
