from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = "you are a youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the entire summary within 250 words. The transcript text is appended here. Please provide the summary of the text given here."


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            print(i)
            transcript += " " + i["text"]
        return transcript

    except Exception as e:
        raise e


def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("YouTube Transcriber")
youtube_link = st.text_input("Enter the video Link from YouTube")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(
        f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)
