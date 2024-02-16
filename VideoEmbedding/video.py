from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


# Load your video clip
def embedding_video(filename,text):
    print("filename and etxt----",filename,text)
    video_clip = VideoFileClip(filename)    
    # Create a TextClip with the desired text, font, and size
    font = "Arial"
    font_size = 12
    (w, h) = video_clip.size
    crop_width = h * (512)
    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    croppedClip = video_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
    text_clip = TextClip(text, font=font, fontsize=font_size, color='white',size=croppedClip.size,method='caption')
    
    # Set the left margin by adjusting the x parameter
    left_margin = 0
    text_clip = text_clip.set_position(('center','top')).set_duration(20)
    
    # Composite the text clip on top of the video clip
    video_with_text = CompositeVideoClip([video_clip.set_start(0), text_clip.set_start(0)])
    
    # Write the result to a new file
    video_with_text.write_videofile("output.mp4", codec='libx264', audio_codec='aac', fps=24)
    
    
# embedding_video("C:\\Users\\ARUNBHAR\\OneDrive - Capgemini\\Desktop\\JS\\Medioox\\youtube_story.mp4","arun is good boy")