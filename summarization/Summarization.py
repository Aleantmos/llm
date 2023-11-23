import canvas
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from pytube import YouTube
from openai import OpenAI

import re

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

llm = ChatOpenAI(temperature=1.0)


class YouTubeTranscriber:
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url

    def download_audio(self):
        # Create a YouTube object
        yt = YouTube(self.youtube_url)

        # Select the stream with only audio
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio and return the file name
        return audio_stream.download(output_path='.', filename='downloaded_audio.mp4')

    def transcribe_audio(self, file_path):
        # Load the Whisper model
        # model = whisper.load_model("base")
        client = OpenAI()
        audio_file = open(file_path, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        # Transcribe the audio file
        # result = model.transcribe(file_path)
        return transcript

    def run_transcription(self):
        # Download the audio
        audio_file = self.download_audio()

        # Transcribe and return the text
        transcription = self.transcribe_audio(audio_file)

        # Optionally, remove the downloaded audio file
        # os.remove(audio_file)

        return transcription

    def generate_pdf(self, text, output_path='transcription.pdf'):
        # Create a PDF document
        pdf = canvas.Canvas(output_path, pagesize=letter)

        # Set font and size
        pdf.setFont("Helvetica", 12)

        # Set margin
        margin = 30
        width, height = letter
        text_object = pdf.beginText(margin, height - margin)
        text_object.setFont("Helvetica", 12)

        # Split the text into lines and add to the PDF
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        for sentence in sentences:
            text_object.textLine(sentence)

        # Add the text object to the PDF
        pdf.drawText(text_object)

        # Save the PDF
        pdf.save()


def generate_summary(path):
    loader = PyPDFLoader(path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    result = chain.run(docs)
    print(result)
    return result


if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    transcriber = YouTubeTranscriber(youtube_url)

    audio_file = transcriber.download_audio()

    # Transcribe and get the text
    transcript = transcriber.transcribe_audio(audio_file)

    print(transcript)
    #
    # # Generate and save the PDF
    pdf_output_path = 'transcription.pdf'

    transcriber.generate_pdf(transcript, pdf_output_path)

    pdf_file_path = "transcription.pdf"

    result = generate_summary(pdf_file_path)
    transcriber.generate_pdf(result, "summary.pdf")
