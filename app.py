from flask import Flask, render_template, request, redirect, url_for, send_file, json
from pytube import YouTube
import datetime
import os

app = Flask(__name__)

if not os.path.exists('downloads'):
    os.makedirs('downloads')


def format_file_size(bytes_size):
    if bytes_size < 1024:
        size_b = bytes_size
        return f"{size_b} B"
    elif bytes_size < 1024 * 1024:
        size_kb = round(bytes_size / 1024, 2)
        return f"{size_kb} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        size_mb = round(bytes_size / (1024 * 1024), 2)
        return f"{size_mb} MB"
    else:
        size_gb = round(bytes_size / (1024 * 1024 * 1024), 2)
        return f"{size_gb} GB"


@app.route('/', methods=['GET', 'POST'])
def index():
    video_options = []
    mp3_options = []
    audio_options = []
    video_url = request.form.get('video_url')
    video_play_url = ''  # Initialize video_play_url here

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'download':
            download_itag = request.form.get('download_itag')
            try:
                yt = YouTube(video_url)
                stream = yt.streams.get_by_itag(download_itag)
                if stream:
                    file_path = os.path.join("downloads", f"{yt.title}.{stream.subtype}")
                    stream.download(output_path="downloads", filename=f"{yt.title}.{stream.subtype}")
                    return send_file(file_path, as_attachment=True)
                else:
                    return redirect(url_for('index', error="Error downloading file."))
            except Exception as e:
                print(f"Error downloading file: {e}")
                return redirect(url_for('index', error="Error downloading file."))

    # video info
    if video_url and request.method == 'POST':
        try:
            yt = YouTube(video_url)
            thumbnail_url = yt.thumbnail_url
            video_title = yt.title
            video_length = yt.length
            video_length_formatted = str(datetime.timedelta(seconds=video_length))

            # Get progressive video streams for playback
            progressive_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            if progressive_streams:
                video_play_url = progressive_streams[0].url  # Use the highest resolution progressive stream for playback

            # Get all video streams for download options
            all_video_streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()

            # Get audio streams (only audio)
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()

            # collect the video options with file size and resolution
            for stream in all_video_streams:
                if stream.resolution:
                    file_size = format_file_size(stream.filesize_approx)
                    video_options.append({
                        "resolution": stream.resolution,
                        "size": file_size,
                        "stream_id": stream.itag
                    })

            # collect the audio options with file size
            for stream in audio_streams:
                file_size = format_file_size(stream.filesize)
                audio_options.append({
                    "format": stream.mime_type.split('/')[1].upper(),
                    "size": file_size,
                    "stream_id": stream.itag
                })
                if stream.abr:
                    mp3_options.append({
                        "quality": stream.abr,
                        "size": file_size,
                        "stream_id": stream.itag
                    })

            return render_template('index.html',
                                   thumbnail_url=thumbnail_url,
                                   video_title=video_title,
                                   video_length=video_length_formatted,
                                   video_options=video_options,
                                   mp3_options=mp3_options,
                                   audio_options=audio_options,
                                   video_play_url=video_play_url
                                   )
        except Exception as e:
            print(f"Error fetching thumbnail: {e}")
            return redirect(url_for('index', error="Error fetching thumbnail."))

    thumbnail_url = request.args.get('thumbnail_url')
    error = request.args.get('error')
    video_title = request.args.get('video_title')
    video_length = request.args.get('video_length')
    video_options = json.loads(request.args.get('video_options', '[]'))
    mp3_options = json.loads(request.args.get('mp3_options', '[]'))
    audio_options = json.loads(request.args.get('audio_options', '[]'))

    return render_template('index.html',
                           thumbnail_url=thumbnail_url,
                           video_title=video_title,
                           video_length=video_length,
                           error=error,
                           video_options=video_options,
                           mp3_options=mp3_options,
                           audio_options=audio_options,
                           video_play_url=video_play_url
                           )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/terms of services')
def terms():
    return render_template('terms.html')


@app.route('/privacy policy')
def privacy():
    return render_template('privacy.html')





if __name__ == '__main__':
    app.run(debug=True)
