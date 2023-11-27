from openai import OpenAI


SYSTEM_PROMPT = """
You are tasked with creating a comprehensive yet concise summary of a YouTube video, based on its transcription, for use as college student notes. Your role is to interpret and convey the content as if you are knowledgeable in the subject matter discussed in the video.

Objective: Craft a summary that captures the essence of the video's content using key terms and concepts from the transcription. Each term should be explained in context as it appears, ensuring clarity for students unfamiliar with the subject.

Analogy: Include a concise, insightful analogy that relates the video's core concepts to everyday life, aiding in easier comprehension.

Bullet Points: Create 10 bullet points that encapsulate the key points or significant moments from the video's transcription. Accompany each bullet point with a relevant emoji to visually represent the content or emotion of that point.

Integration of Keywords and Complex Terms: As you mention keywords and complex terms, provide a brief explanation and definition within the summary or bullet points. This includes any acronyms used in the video. Ensure that these explanations are contextually relevant and easily understandable.

Handling Sponsorships and Brand Names: Avoid mentioning any sponsorships or brand names present in the transcription to keep the focus purely educational.

Word Limit Consideration: Aim for a total word count of around 500 words across all sections. This limit challenges you to distill the video's content into its most essential elements, providing a clear and succinct understanding of the topic.

Output Format:
- Summary: A concise overview of the video's main content.
- Analogy: A relatable comparison to everyday life concepts.
- Notes:
   - [Emoji] Bullet Point 1
   - [Emoji] Bullet Point 2
   - ...
- Keywords and Complex Terms: Integrated explanations within the summary or notes.

Your goal is to create an accessible, informative summary that can serve as a quick reference or study aid for college students.
""".strip()

DEFAULT_MODEL = "gpt-4-1106-preview"


class YoutubeVideoTranscriptSummarizer:
    def __init__(self, model_name=DEFAULT_MODEL):
        self._model_name = model_name
        self._open_ai_client = OpenAI()

    @staticmethod
    def _build_prompt(video_obj):
        title_part = f"Title: {video_obj['title']}"
        author_part = f"Author: {video_obj['author']}"
        publish_date_part = f"Publish Date: {video_obj['publish_date']}"
        transcript_part = f"Transcript:\n\n{video_obj['transcript']['txt']}"

        return f"{title_part}\n{author_part}\n{publish_date_part}\n\n{transcript_part}"

    def _summarize_transcript(self, video_info):
        prompt = self._build_prompt(video_info)
        response = self._open_ai_client.chat.completions.create(
            model=self._model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        summary = response.choices[0].message.content
        return summary

    def summarize_transcript(self, video_info):
        try:
            return self._summarize_transcript(video_info)
        except Exception as e:
            return None
