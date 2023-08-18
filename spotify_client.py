import json
import os
from dataclasses import dataclass

import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

dotenv.load_dotenv()


@dataclass
class Playlist:
    name: str
    description: str
    tracks: list[str]


class SpotifyClient:
    def __init__(self) -> None:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        self.spotify = spotipy.Spotify(auth_manager=auth_manager)

    def get_playlist(self, id: str):
        playlist = self.spotify.playlist(id)
        queries = []
        batch_tracks = playlist["tracks"]
        all_tracks = batch_tracks["items"]
        while batch_tracks["next"]:
            batch_tracks = self.spotify.next(batch_tracks)
            all_tracks.extend(batch_tracks["items"])
        playlist["tracks"]["items"] = all_tracks
        with open(f"{playlist['name']}.json", "w") as f:
            json.dump(playlist, f, indent=4)
        for track in all_tracks:
            track_name = track["track"]["name"]
            artists = ", ".join(
                [artist["name"] for artist in track["track"]["artists"]]
            )
            queries.append(f"{track_name} by {artists}")
        return Playlist(playlist["name"], playlist["description"], queries)

if __name__ == "__main__":
    spotify = SpotifyClient()
    print(spotify.get_playlist("4YaYDXynaq60Q8nHwD9zYT"))