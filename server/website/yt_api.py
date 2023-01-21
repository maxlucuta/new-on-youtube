from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript("HulPgd-QgJk")

transcript_list = ""

for i in transcript:
    if(i['text'] != '[Music]'):
        transcript_list += i['text']

print(transcript_list)