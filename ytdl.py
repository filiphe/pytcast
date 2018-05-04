import youtube_dl

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
