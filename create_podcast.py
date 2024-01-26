from dotenv import load_dotenv
import os
from openai import OpenAI
import feedparser
import json
import requests

load_dotenv()

client = OpenAI()

eleven_labs_api_key = os.getenv("ELEVENLABS_API_KEY")

news_feed = "http://rss.cnn.com/rss/edition_technology.rss"

print("==== Processing news feed ====")
feed = feedparser.parse(news_feed)
stories = ""
stories_limit = 1

for item in feed.entries[:stories_limit]:
  # check if the item title and item.description exist if not skip  the item
  if item.title and item.description:
    stories = stories + "New Story: " + item.title + ". " + item.description

print("==== Processing ChatGPT ====")


prompt = "Please rewrite the following news headlines and summaries in a discussion way, as thought someone is talking about them one by one on a on-off podcast in a non-judgmental way and with no follow-up discussion, although there should be a final closing greeting: " + stories

chat_output = client.chat.completions.create(
    model="gpt-3.5-turbo-0301",
    messages=[{"role": "user", "content": prompt}]
)

chat_content = chat_output.choices[0].message.content

print(chat_content)

print("==== Processing Audio ====")

voice_id = "21m00Tcm4TlvDq8ikWAM"
audio_url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

payload = {
    "text": chat_content,
    "voice_settings": {
        "similarity_boost": 0,
        "stability": 0.2,
    }
}
headers = {"Content-Type": "application/json", "xi-api-key": eleven_labs_api_key, "accept": "audio/mpeg"}
response = requests.request("POST", audio_url, json=payload, headers=headers)


print("==== Saving Audio ====")

if response.status_code == 200:
  with open("test.mp3", "wb") as output_file:
    output_file.write(response.content)
else:
  print("Error: " + response.text) 

print("==== Done ====")