from orchestrator import Orchestrator


if __name__ == '__main__':
    orchestrator = Orchestrator()

    #channel_url = "https://www.youtube.com/@DaveShap"
    channel_url = "https://www.youtube.com/@jawed"
    channel_name = "jawed"

    orchestrator.get_youtube_channel_video_infos(channel_name, channel_url, num_videos=3)
    orchestrator.get_youtube_channel_video_transcripts(channel_name)
