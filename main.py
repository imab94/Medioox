from fastapi import FastAPI, Request,HTTPException,Form,UploadFile,File,Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pytube import YouTube
import shutil
import os
from TextToSpeechAI.main import main
from AudioToTranscribe.code import fetch_transcribe

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Mount the /static/uploads directory to serve files
app.mount("/static/uploads", StaticFiles(directory="static/uploads"), name="uploads")


@app.get("/")
async def index(request: Request, dummy_param: str = None):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
   
    
@app.post("/download")
async def download_youtube_shorts(link: str = Form(...)):
    try:
        # Download the video
        youtube = YouTube(link)
        video = youtube.streams.filter(file_extension="mp4",progressive=True).first()
        video.download("downloads", filename="downloaded_shorts.mp4")

        # Provide the downloaded video as a response
        return FileResponse("downloads/downloaded_shorts.mp4", media_type="video/mp4", filename="downloaded_shorts.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...), locale: str = Form(...)):
    upload_dir = 'static/uploads/'
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "locale": locale}


@app.post("/generate_audio")
async def generate_audio_file():
    # Get the full path to the static directory
    static_dir = os.path.join(os.getcwd(), "static")
    
    # Get the full path to the uploads directory within the static directory
    folder_path = os.path.join(static_dir, "uploads")

    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if files:
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f))) 
        latest_file_path = os.path.join(folder_path, latest_file)
        main(latest_file_path)
        final_audio_dir = os.path.join(os.getcwd(), "final_audio")
        audio_files = [f for f in os.listdir(final_audio_dir) if os.path.isfile(os.path.join(final_audio_dir, f))]
        if audio_files:
            latest_audio_file = max(audio_files, key=lambda f: os.path.getmtime(os.path.join(final_audio_dir, f)))
            generated_audio__file_path = os.path.join(final_audio_dir,latest_audio_file)
        return FileResponse(generated_audio__file_path, media_type="audio/mp3", filename="generated_audio.mp3")
    else:
        return {
            "message": "No files found in the specified directory."
            }
        
@app.get("/text_to_audio")
async def text_to_audio(request: Request, dummy_param: str = None):
    return templates.TemplateResponse(
        "TextToAudio.html",
        {"request": request}
    )
    
@app.get("/youtube_shorts_video")
async def youtube_shorts_video(request: Request, dummy_param: str = None):
    return templates.TemplateResponse(
        "youtube_shorts.html",
        {"request": request}
    )
    
@app.get("/add_caption_video")
async def add_caption_video(request: Request, dummy_param: str = None):
    return templates.TemplateResponse(
        "captionToVideos.html",
        {"request": request}
    )
    
    
@app.get("/instagram_reels")
async def instagram_reels(request: Request, dummy_param: str = None):
    return templates.TemplateResponse(
        "InstagramReels.html",
        {"request": request}
    )
    
@app.get('/audio_to_text')
async def audio_to_text(request: Request, dummy_param: str = None):
    return templates.TemplateResponse(
        "audio_to_text.html",
        {"request": request}
    )
    
@app.post('/download_audio_to_text')
async def download_audio_to_text(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())

        # Call the fetch_transcribe function with the file path
        fetch_transcribe(file.filename)

        english_text = None
        hindi_text = None

        # Check if English text file exists
        if os.path.exists("english_textfile.txt"):
            with open("english_textfile.txt", "r", encoding="utf-8") as english_file:
                english_text = english_file.read()
            # Delete English text file
            os.remove("english_textfile.txt")

        # Check if Hindi text file exists
        if os.path.exists("hindi_textfile.txt"):
            with open("hindi_textfile.txt", "r", encoding="utf-8") as hindi_file:
                hindi_text = hindi_file.read()
            # Delete Hindi text file
            os.remove("hindi_textfile.txt")

        # Return success response with text content
        return {
            "status": "success",
            "message": "Transcription completed",
            "english_text": english_text,
            "hindi_text": hindi_text
        }
    except Exception as e:
        # Return error response
        raise HTTPException(status_code=500, detail=str(e))
