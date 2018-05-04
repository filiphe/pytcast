#!/usr/bin/env python3

import os
import pytz
import youtube_dl

from datetime import datetime
from feedgen.feed import FeedGenerator

ydl_opts = {
        'format': 'bestaudio/best',
        'writethumbnail': True,
        'outtmpl': '%(upload_date)s-%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'}, ],
        }

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/playlist?list=PLPjdPog_vKX0MjJEN0GF521kA-xlXbxVa'])


fg = FeedGenerator()
fg.load_extension('podcast')
fg.podcast.itunes_category('Culture', 'Gaming')

fg.id('http://titb.hesslund.org')
fg.title('Trapped in the Birdcage Podcast')
fg.description('Trapped in the Birdcage Podcast')
fg.link(href='http://titb.hesslund.org', rel='alternate')
fg.link(href='http://titb.hesslund.org/feed.rss', rel='self')
fg.language('en')

for (root, _, files) in os.walk('Trapped.in.the.Birdcage'):
    for i, f in enumerate(sorted(files)):
        if not f.endswith(".mp3"):
            continue
        t = f.split('-')[0]
        yr = int(t[0:4])
        m = int(t[4:6])
        d = int(t[6:])
        fe = fg.add_entry()
        fe.id('http://titb.hesslund.org/{}'.format(f))
        fe.title(f)
        fe.description(f)
        fe.enclosure('http://titb.hesslund.org/{}'.format(f), 0, 'audio/mpeg')
        time = datetime(yr, m, d, 0, 0, tzinfo=pytz.UTC)
        fe.published(time)
        os.utime(os.path.join(root, f), (time.timestamp(), time.timestamp()))

fg.rss_str(pretty=True)
fg.rss_file('Trapped.in.the.Birdcage/feed.rss')
