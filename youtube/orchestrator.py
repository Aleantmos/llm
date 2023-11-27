import pickle
import os
import time

from youtube_video_info_extractor import YouTubeVideoInfoExtractor
from youtube_video_transcript_summarizer import YoutubeVideoTranscriptSummarizer

import scrapetube


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


class Orchestrator:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        self._video_info_extractor = YouTubeVideoInfoExtractor()
        self._video_transcript_summarizer = YoutubeVideoTranscriptSummarizer()

    def get_youtube_channel_video_transcripts(self, channel_name):
        channel_video_data_file_path = os.path.join(DATA_DIR, f"{channel_name}.pcl")

        with open(channel_video_data_file_path, 'rb') as f:
            channel_video_data = pickle.load(f)

        for video_info in channel_video_data:
            if video_info.get('summary') is not None:
                continue
            summary = self._video_transcript_summarizer.summarize_transcript(video_info)
            video_info['summary'] = summary

            with open(channel_video_data_file_path, 'wb') as f:
                f.write(pickle.dumps(channel_video_data))

    def get_youtube_channel_video_infos(self, channel_name, channel_url=None, num_videos=None):
        print(f"Getting video infos for channel '{channel_name}' ...")

        # Why .pcl format?
        channel_video_data_file_path = os.path.join(DATA_DIR, f"{channel_name}.pcl")

        try:
            with open(channel_video_data_file_path, 'rb') as f:
                channel_video_data = pickle.load(f)
        except:
            channel_video_data = []

        if not (channel_url or channel_video_data):
            raise ValueError

        channel_url = channel_url or channel_video_data[0]['channel_url']
        # Are these all videos of the specific channel?
        channel_videos_raw = scrapetube.get_channel(channel_url=channel_url)

        # So we iterate through the scraped videos of the channel
        for i, scraped_video_obj in enumerate(channel_videos_raw):
            n = i + 1
            if (num_videos is not None) and (n > num_videos):
                break
            #Not exactly sure what this line does?
            video_data = [vd for vd in channel_video_data if vd['id'] == scraped_video_obj['videoId']]

            # Why check if video_data != null => skipping video
            if video_data:
                continue

            start_time = time.time()
            video_data = self._video_info_extractor.get_video_info(scraped_video_obj)
            end_time = time.time()

            video_data['channel_url'] = channel_url
            channel_video_data.append(video_data)
            print(f"{n}: {video_data['title']} (time: {int(end_time - start_time)} seconds)")

            # w -> write mode, b -> binary mode => opened in binary write mode
            with open(channel_video_data_file_path, 'wb') as f:
                f.write(pickle.dumps(channel_video_data))
