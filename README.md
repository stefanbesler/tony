# Tony - Synchronize Mp3s with a Creative Tonie

This simple script can be used to upload mp3s to a Creative Tonie. Mp3s are either uploaded from a local directory or by specifying a (public) Spotify playlist.
The latter option uses [spotDL](https://github.com/spotDL/spotify-downloader), is implemented as a proof-of-concept and should not be used due to legal reasons.

## Installation

``` bash
git clone https://github.com/stefanbesler/tony.git
cd tony
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage (local)

To upload all mp3 located in the directory `dir` to a Creative Tonie use

``` bash
cd <repo>
source venv/bin/activate
python tony.py --username <tonies.com username> --password <tonies.com password> --input-path <dir>
```

To upload all files from a Spotify playlist first get the link `playlist_url` to your public Spotify playlist. You can find this in the Spotify application when
sharing your playlist with others. In the Spotify desktop app the simplest way to get the URL is to right click the playlist and click 'Invite Collaborators' 

``` bash
cd <repo>
source venv/bin/activate
python tony.py --username <tonies.com username> --password <tonies.com password> --playlist <playlist_url>
```

## Docker

To run tony in a docker container and run it every hour, the following steps have to be taken

```
git clone https://github.com/stefanbesler/tony.git
cd tony
docker build --tag tony:main
docker run -d --restart=unless-stopped \
  -e TONY_USERNAME=<tonies.com username> \
  -e TONY_PASSWORD=<tonies.com password> \
  -e TONY_PLAYLIST=<playlist_url> \
  --name tony1 tony:main
```
