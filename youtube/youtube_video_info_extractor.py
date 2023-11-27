import os
import subprocess
import traceback

from openai import OpenAI
from pytube import YouTube


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_PATH = os.path.join(BASE_DIR, 'tmp_downloads')
FILE_EXTENSION = 'mp4'


class YouTubeVideoInfoExtractor:
    def __init__(self, verbose=True):
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)

        self._verbose = verbose
        self._open_ai_client = OpenAI()

    @staticmethod
    def _safe_filename(title):
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '')
        return title

    @staticmethod
    def _extract_text_from_srt(text_srt):
        lines = text_srt.split('\n')

        text = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line.isdigit() and i + 2 < len(lines):
                j = i + 2
                while j < len(lines) and lines[j].strip() != "":
                    text.append(lines[j].strip())
                    j += 1

        return ' '.join(text)

    @staticmethod
    def _get_whisper_prompt_for_video(video_obj):
        prompt_intro = "The audio is from a YouTube video."

        title_part = f"Title: {video_obj['title']}"
        author_part = f"Author: {video_obj['author']}"
        publish_date_part = f"Publish Date: {video_obj['publish_date']}"
        keywords_part = f"Keywords: {', '.join(video_obj['keywords'])}"

        return f"{prompt_intro}\n\n{title_part}\n{author_part}\n{publish_date_part}\n{keywords_part}"

    def _extract_transcript_from_file(self, audio_file, video_obj):
        prompt = self._get_whisper_prompt_for_video(video_obj)
        transcript_srt = self._open_ai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format='srt',
            prompt=prompt,
        )
        transcript_txt = self._extract_text_from_srt(transcript_srt)

        return {'srt': transcript_srt.strip(), 'txt': transcript_txt.strip()}

    def _get_video_transcript(self, video):
        yt_obj = video['raw']['pytube_obj']

        title = video['title']
        file_name = self._safe_filename(title)
        full_file_name = f'{file_name}.{FILE_EXTENSION}'
        file_path = os.path.join(DOWNLOAD_PATH, full_file_name)

        # Not sure why we're doing this in the try() except()
        try:
            audio_stream = yt_obj.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=DOWNLOAD_PATH, filename=full_file_name)
        except Exception as e:
            command = ["yt-dlp", "-f", "bestaudio", video['url'], "-o", file_path]
            subprocess.run(command, shell=True)

        with open(file_path, 'rb') as f:
            try:
                #Extracting in srt as well as txt format
                transcript = self._extract_transcript_from_file(f, video)
            except Exception as e:
                transcript = None
                print(f"Exception occurred: {e}")
                print(traceback.format_exc())
        os.remove(file_path)

        return transcript

    def get_video_info(self, scraped_video_obj):
        video_id = scraped_video_obj['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        yt_obj = YouTube(
            video_url,
            use_oauth=True,
            allow_oauth_cache=True,
        )
        try:
            yt_obj.streams.first()  # Raises an error for age-restricted videos. Think of a fix.
        except Exception as e:
            pass

        # Not sure what exactly are we sorting here?
        thumbnails = sorted(scraped_video_obj['thumbnail']['thumbnails'], key=lambda x: x['width'] * x['height'])
        video_info = {
            'id': video_id,
            'url': video_url,
            'publish_date': yt_obj.publish_date,
            'title': yt_obj.title,
            'description': yt_obj.description,
            'keywords': yt_obj.keywords,
            'author': yt_obj.author,
            'length': yt_obj.length,
            'views': yt_obj.views,
            'age_restricted': yt_obj.age_restricted,
            #thumbnails[-1] negative number - iterating through the back side of the array?...........['url']
            'thumbnail_img_url': thumbnails[-1]['url'],
            'raw': {'scraped_obj': scraped_video_obj, 'pytube_obj': yt_obj},
        }
        video_info['transcript'] = self._get_video_transcript(video_info)

        return video_info
