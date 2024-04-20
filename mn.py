import uvicorn
from functools import lru_cache
from fastapi import FastAPI
from  pydantic_settings import BaseSettings
import config
import boto3
from pydantic import BaseModel
import base64


app = FastAPI()

@lru_cache()
def get_settings():
    
    return config.Settings()


class Text(BaseModel):
    content: str
    output_format: str



@app.post("/")
async def get_audio(text: Text):
    client = boto3.client('polly', aws_access_key_id=get_settings().AWS_AK, aws_secret_access_key=get_settings().AWS_SAK, region_name='us-east-1')
    result = client.synthesize_speech(Text=text.content, OutputFormat=text.output_format, VoiceId='Brian')
    audio = result['AudioStream'].read()
    encoded_audio = base64.b64encode(audio).decode('utf-8')
    return {"message": "Audio convertion complete", "data" : {
        "text": text.content,
        "output_format": text.output_format,
        "audio": encoded_audio
    }}


if __name__ == "__main__":
    uvicorn.run("mn:app", host="0.0.0.0", port=8080, reload=True)