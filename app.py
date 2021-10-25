from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

youtube_video="https://www.youtube.com/watch?v=NFHDHcs4BvQ"
video_id=youtube_video.split("=")[1]
transcript = YouTubeTranscriptApi.get_transcript(video_id)
result=""
for i in transcript:
    result+=' '+ i['text']
# summarizer = pipeline('summarization')
# num_iters=int(len(result)/1000)
# summarized_text=[]
# for i in range(0,num_iters+1):
#     start =0
#     start =i*1000
#     end=(i+1)*1000
#     out=summarizer(result[start:end])
#     out=out[0]
#     out=out['summary_text']
#     summarized_text.append(out)
# summary_text=summarizer(result)[0]['summary_text']
# print(summary_text)
from transformers import T5ForConditionalGeneration, T5Tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base")
inputs = tokenizer.encode("summarize: " + result, return_tensors="pt", max_length=512, truncation=True)
outputs = model.generate(
    inputs, 
    max_length=250, 
    min_length=40, 
    length_penalty=2.0, 
    num_beams=4, 
    early_stopping=True)
print(tokenizer.decode(outputs[0],skip_special_tokens=True))