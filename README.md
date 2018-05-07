# pytcast
A program to generate a podcast feed from a Youtube playlist

## How to use
```bash
$ python3 generate_feed.py --help
usage: generate_feed.py [-h] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to configuration
```

## Config
```yaml
podcasts:
  trapped-in-the-birdcage:
    playlist_id: PLfS8QgUdeGYo8L-g8uHr1_hV8UcJDbM33
    name: Trapped in the Birdcage
  mirrorshades:
    playlist_id: PL-oTJHKXHicTdbGTF_9uNvrE_ehvI8eJ-
    name: Mirrorshades
  the-west-marches:
    playlist_id: PL-oTJHKXHicSxKhs57c2hYuoPcayPoBJc
    name: The West Marches
  misscliks-lost-mine:
    playlist_id: PLSOKvcIdcJJdaeOrHvdeJGFPzBrrclXxl
    name: Missclicks D&D Lost Mine
  court-of-swords:
    playlist_id: PL-oTJHKXHicQpK4d231BKSC9UJQr3HQny
    name: Court of Swords

general:
  playlist_base: https://www.youtube.com/playlist?list=
  video_base: https://www.youtube.com/watch?v=
  url_base: http://podcast.hesslund.org
  output_dir: podcasts
```
