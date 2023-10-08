# -*- coding: utf-8 -*-

import logging
import re
import os
import subprocess
import sys
import time
import glob
import spotdl
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
parser.add_argument("-P", "--playlist", dest="playlist", required=False, help="Link you get be clicking 'Invite  collaborators' in Spotify")
parser.add_argument("-i", "--input-path", dest="input_path", required=False, help="")   
parser.add_argument("-c", "--cache-path", dest="cache_path", required=False, help="Defaults to ~/.local/share/tony")   

args = parser.parse_args()

# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s | %(message)s' )

def main():
    
    if(args.input_path is None and args.playlist is None):
        raise ValueError(f"--playlist or --input-path argument is required")
    
    if(args.input_path is not None and args.playlist is not None):
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
        subprocess.run(["spotdl", "download", args.playlist, "--save-file", "cache.spotdl"], check=True)
        logging.info("Download complete")
    else:
        os.chdir(args.input_path)
        
    playlist_titles = [PlaylistTitle(filepath=mp3, title=os.path.basename(mp3)) for mp3 in glob.iglob('*.mp3', recursive=False)]
    
    tonie_api = TonieAPI(args.username, args.password)
    household = tonie_api.get_households()[0]
    creative_tonie = tonie_api.get_all_creative_tonies_by_household(household)[0]
    
    new_titles = [PlaylistTitle(filepath="", title=ch.title) not in playlist_titles for ch in  creative_tonie.chapters]

    if True in new_titles:
        logging.info(f"Remove all chapters from '{creative_tonie.name}'")
        tonie_api.clear_all_chapter_of_tonie(creative_tonie)
        
        logging.info(f"Uploading {len(playlist_titles)} chapters to Creative Tonie {creative_tonie.name}")    
        for t in playlist_titles:
            logging.info(f" - {t.title}")
            tonie_api.upload_file_to_tonie(creative_tonie, t.filepath, t.title)
    else:
        logging.info(f"'{creative_tonie.name}' is up-to-date")

    sys.exit(0)
    
if __name__ == '__main__':
    main()
