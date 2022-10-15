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


def add_playlist_current_playing(self):
    last_track_id = ""
    while True:
        try:
            current_playing = self.sp.current_user_playing_track()
            if current_playing is not None:
                track_name = current_playing['item']['name']
                track_id = current_playing["item"]["id"]
                artist_name = current_playing['item']['artists'][0]['name']
                if last_track_id != track_id:
                    last_track_id = track_id
                    print(track_name + "/" + artist_name)
                    self.sp.playlist_add_items(self.playlist_id, [track_id], position=0)
            else:
                print("no song is playing...")
        except Exception as e:
            logger.error(e)
        time.sleep(30)


def main():
    try:
        param = Param()
        # 現在再生中の曲をプレイリストに追加する
        add_playlist_current_playing(param)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
