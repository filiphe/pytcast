#!/usr/bin/env python3

import argparse
import os
import pytz
import yaml
import youtube_dl

from datetime import datetime
from feedgen.feed import FeedGenerator

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='path to configuration', default='config.yml')
args = parser.parse_args()


with open(args.config, 'r') as f:
    content = f.read()
    data = yaml.load(content)

config = data['general']
podcasts = data['podcasts']


def get_ydl_opts(target_dir):
    ydl_opts = {
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'outtmpl': '{}/{}/%(upload_date)s-%(title)s.%(ext)s'.format(config['output_dir'], target_dir),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                },
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'}, ],
#            'quiet': True,
            'nooverwrites': True,
            'ignoreerrors': True,
            'download_archive': './archive_file.txt',
            }
    return ydl_opts


def get_ydl_thumbnail_opts(target_dir):
    ydl_opts = {
            'writethumbnail': True,
            'nooverwrites': True,
            'ignoreerrors': True,
            'skip_download': True,
            'outtmpl': '{}/{}/logo.%(ext)s'.format(config['output_dir'], target_dir),
            'playlist_items': '1',
            }
    return ydl_opts


def download_list(key):
    with youtube_dl.YoutubeDL(get_ydl_opts(key)) as ydl:
        ydl.download(['{}'.format(get_playlist_url(key))])


def download_thumbnail(key):
    with youtube_dl.YoutubeDL(get_ydl_thumbnail_opts(key)) as ydl:
        ydl.download(['{}'.format(get_playlist_url(key))])


def get_playlist_url(key):
    return config['playlist_base'] + podcasts[key]['playlist_id']


def gen_feed(directory, name, url):
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.podcast.itunes_category('Culture', 'Gaming')

    fg.id(url)
    fg.title(name)
    fg.description(name)
    fg.link(href=url, rel='alternate')
    fg.link(href=url, rel='self')
    fg.logo('{}/{}'.format(url, 'logo.jpg'))
    fg.language('en')

    for (root, _, files) in os.walk(os.path.join(config['output_dir'], directory)):
        for i, f in enumerate(sorted(files)):
            if not f.endswith(".mp3"):
                continue
            t = f.split('-')[0]
            yr = int(t[0:4])
            m = int(t[4:6])
            d = int(t[6:])
            fe = fg.add_entry()
            fe.id('{}/{}'.format(url, f))
            fe.title(f)
            fe.description(f)
            fe.enclosure('{}/{}'.format(url, f), 0, 'audio/mpeg')
            time = datetime(yr, m, d, 0, 0, tzinfo=pytz.UTC)
            fe.published(time)
            os.utime(os.path.join(root, f), (time.timestamp(), time.timestamp()))

    fg.rss_str(pretty=True)
    fg.rss_file('{}/{}/feed.rss'.format(config['output_dir'], directory))


def main():
    for podcast in podcasts:
        download_list(podcast)
        download_thumbnail(podcast)
        gen_feed(podcast, podcasts[podcast]['name'], '{}/{}'.format(config['url_base'], podcast))


if __name__ == '__main__':
    main()
