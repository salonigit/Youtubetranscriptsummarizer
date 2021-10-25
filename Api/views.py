from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi

def check(request,video_id):
    # transcript=YouTubeTranscriptApi.get_transcript(video_id)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    # transcript = transcript_list.find_generated_transcript(['en'])
    # transcript = transcript_list.find_manually_created_transcript(['en'])
    transcript = transcript_list.find_transcript(['en'])
    transcript=transcript.fetch()
    result=""
    for i in transcript:
        result+=' '+ i['text']
    from transformers import T5ForConditionalGeneration, T5Tokenizer
    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode("summarize: " + result, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs, 
        max_length=250, 
        min_length=100, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True)
    summary=( '. '.join(map(lambda s: s.strip().capitalize(), tokenizer.decode(outputs[0],skip_special_tokens=True).split('.'))))
    return render(request,'index.html',{'text': summary,'text1':result})