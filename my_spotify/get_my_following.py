# -*- coding: utf-8 -*-

import configparser
import time
from pprint import pprint

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


def main():
    try:
        self = Param()
        response = self.sp.current_user_followed_artists(limit=2)
        for artist in response['artists']['items']:
            artist_id = artist['id']
            albums = self.sp.artist_albums(artist['uri'])
            album_id = albums['items'][0]['id']
            album_name = albums['items'][0]['name']
            pprint(f'{artist_id=},{album_id=},{album_name=}')

            break
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
