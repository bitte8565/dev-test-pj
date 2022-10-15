# -*- coding: utf-8 -*-

import configparser
import time

import boto3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from my_spotify import json_logger
from my_spotify.ssm import get_parameters

logger = json_logger.get_logger(__name__)

cfg = configparser.ConfigParser()
cfg.read('config/config.ini', encoding='utf-8')


class Param:
    def __init__(self):
        self.ssm = boto3.client('ssm', region_name='ap-northeast-1')
        self.client_id = get_parameters(self, param_key="/spotify/client_id")
        self.client_secret = get_parameters(self, param_key="/spotify/client_secret")
        self.redirect_uri = get_parameters(self, param_key="/spotify/redirect_uri")
        self.playlist_id = get_parameters(self, param_key="/spotify/playlist_id")
        scope = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing " \
                "app-remote-control streaming playlist-read-private playlist-read-collaborative " \
                "playlist-modify-private playlist-modify-public user-follow-modify user-follow-read " \
                "user-read-playback-position user-top-read user-read-recently-played user-library-modify " \
                "user-library-read user-read-email user-read-private"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=scope))


def get_top_tracks(self):
    # ['short_term', 'medium_term', 'long_term']
    top_tracks = self.sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')
    for track in top_tracks['items']:
        track['album']['available_markets'] = None
        track['available_markets'] = None
        track_name = track['name']
        artists_name = []
        for artist in track['artists']:
            artists_name.append(artist['name'])
        artist_name = ",".join(artists_name)
        score = track['popularity']

        print(f'track:{track_name} artist:{artist_name} score:{score}')


def main():
    logger.info('start')
    start_unix_time = time.time()
    try:
        param = Param()
        # 再生回数上位の曲を取得する
        get_top_tracks(param)
    except Exception as e:
        logger.exception(e)
    finally:
        end_unix_time = time.time()
        duration_sec = int(end_unix_time - start_unix_time)
        logger.info('end', extra={'duration': duration_sec})


if __name__ == '__main__':
    main()
