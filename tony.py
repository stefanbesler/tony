# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import json
import os
import subprocess
import sys
import time
import glob
import spotdl
import http.client
import urllib

from pathlib import Path
from itertools import chain
from argparse import ArgumentParser
from dataclasses import dataclass
from tempfile import TemporaryDirectory

from spotdl import Spotdl
import spotdl.console
from tonie_api.api import TonieAPI
from tonie_api.models import Config, CreativeTonie, User

@dataclass(eq=False)
class PlaylistTitle:
    filepath: str
    title: float
    
    def __eq__(self, other):
        return self.title == other.title    


usage = """
""".format(sys.version, os.path.basename(__file__))

parser = ArgumentParser(usage=usage)
parser.add_argument("-u", "--username", dest="username", required=True, help="")
parser.add_argument("-p", "--password", dest="password", required=True, help="")
parser.add_argument("-a", "--pushover-apptoken", dest="pushover_apptoken", required=False, help="") 
parser.add_argument("-k", "--pushover-userkey", dest="pushover_userkey", required=False, help="") 
parser.add_argument("-P", "--playlist", dest="playlist", required=False, help="Link you get be clicking 'Invite  collaborators' in Spotify")
parser.add_argument("-i", "--input-path", dest="input_path", required=False, help="")   
parser.add_argument("-c", "--cache-path", dest="cache_path", required=False, help="Defaults to ~/.local/share/tony")   

args = parser.parse_args()

# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s | %(message)s' )

def notify(user_key, app_token, title, message):
    
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": app_token,
        "user": user_key, 
        "title": title,
        "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    
    response = conn.getresponse()
    
    if response.status != 200:
        raise Exception(f"Pushover error: {response.reason}")

def main():
    
    try:
        if(args.input_path is None and args.playlist is None):
            raise ValueError(f"--playlist or --input-path argument is required")
                
        input_path = args.input_path
        if args.playlist is not None:
            if args.cache_path is None:
                args.cache_path = os.path.join(os.path.expanduser("~"), ".local", "share", "tony")
            
            if not os.path.exists(args.cache_path):
                logging.info(f"Creating cache folder {args.cache_path}")
                os.makedirs(args.cache_path)
            
            os.chdir(args.cache_path)
            logging.info("Start download")
            try:
                subprocess.run(["/usr/local/bin/spotdl", "download", args.playlist, "--save-file", "cache.spotdl"], check=True)
            except:
                subprocess.run(["spotdl", "download", args.playlist, "--save-file", "cache.spotdl"], check=True)
                
            logging.info("Download complete")
            
        playlist_titles = []
        if args.cache_path is not None:
            os.chdir(args.cache_path)
            try:
                json_path = os.path.join(args.cache_path, 'cache.spotdl')
                with open(json_path, 'r') as f:
                    logging.info(f"Loading {json_path}")
                    playlist_titles = [PlaylistTitle(filepath=os.path.join(args.cache_path, ", ".join(p["artists"]) + " - " + p["name"] + ".mp3"), 
                                    title = ", ".join(p["artists"]) + " - " + p["name"]) for p in json.load(f)]
            except:
                logging.error(e)
                playlist_titles += [PlaylistTitle(filepath=os.path.join(args.cache_path, mp3), title=os.path.splitext(os.path.basename(mp3))[0]) for mp3 in glob.iglob('*.mp3', recursive=False)]
        
        if args.input_path is not None:
            os.chdir(args.input_path)
            playlist_titles += [PlaylistTitle(filepath=os.path.join(args.input_path, mp3), title=os.path.splitext(os.path.basename(mp3))[0]) for mp3 in glob.iglob('*.mp3', recursive=False)]
        
        tonie_api = TonieAPI(args.username, args.password)
        household = tonie_api.get_households()[0]
        creative_tonie = tonie_api.get_all_creative_tonies_by_household(household)[0]
        
        new_titles = [pt.title not in map(lambda x: x.title, creative_tonie.chapters) for pt in playlist_titles]

        if True in new_titles or len(playlist_titles) != len(creative_tonie.chapters):
            logging.info(f"Remove all chapters from '{creative_tonie.name}'")
            tonie_api.clear_all_chapter_of_tonie(creative_tonie)
            
            logging.info(f"Uploading {len(playlist_titles)} chapters to Creative Tonie {creative_tonie.name}")    
            for t in playlist_titles:
                logging.info(f" - {t.title}")
                tonie_api.upload_file_to_tonie(creative_tonie, t.filepath, t.title)
                
            notify(args.pushover_userkey, args.pushover_apptoken, "Update successful", "\n".join([t.title for t in playlist_titles]))                
        else:
            logging.info(f"'{creative_tonie.name}' is up-to-date with {len(playlist_titles)} tracks")

        sys.exit(0)
        
    except Exception as ex:
        logging.critical(ex, exc_info=True)
        notify(args.pushover_userkey, args.pushover_apptoken, "Update error", str(ex))
        sys.exit(-1)
    
if __name__ == '__main__':
    main()
