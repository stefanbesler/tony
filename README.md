# Tony - Synchronize Mp3s with a Creative Tonie

This simple script can be used to upload mp3s to a Creative Tonie. Mp3s are either uploaded from a local directory or can also be specified via a Spotify playlist.
The latter option uses [spotDL](https://github.com/spotDL/spotify-downloader) and is implemented as a proof-of-concept and should not be used due to legal reasons.

## Installation

``` bash
git clone [[<repo>](https://github.com/stefanbesler/tony.git)](https://github.com/stefanbesler/tony.git)
cd tony
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

To upload all mp3 located in the directory <dir> to a Creative Tonie use

``` bash
cd <repo>
python tony.py --username <tonies.com username> --password <tonies.com password> --input-path <dir>
```

To upload all files from a Spotify playlist first get the link <playlist_url> to your public Spotify playlist. You can find this in the Spotify application when
sharing your playlist with others. In the Spotify desktop app the simplest way to get the URL is to right click the playlist and click 'Invite Collaborators' 

``` bash
cd <repo>
python tony.py --username <tonies.com username> --password <tonies.com password> --playlist <playlist_url>
```
