from moviepy.editor import *
from instaloader import Post
import instaloader
import requests
import whisper
import sys

reels = sys.argv[1]
reels_id = reels.split('/')[4]

print("Extraindo a URL... ", end='')

# Pega a url do reels
loader = instaloader.Instaloader()
post = Post.from_shortcode(loader.context, reels_id)
url = post.video_url
print("OK")


# Faz o download em mp4
print("Fazendo o download do video... ", end='')
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open('receita.mp4', 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
print("OK")


# Converte o video em mp3
print("Convertendo o video em mp3... ", end='')
video = VideoFileClip("receita.mp4")
video.audio.write_audiofile("receita.mp3")
print("OK")

# Transcreve o mp3 para texto usando whisper
print("Transcrevendo o texto...", end='\n\n')
model = whisper.load_model("base")
result = model.transcribe("./receita.mp3")
print(result["text"])
