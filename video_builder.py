import os
import json
import requests
# V2 Syntax: We now import directly from moviepy
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from dotenv import load_dotenv

# 1. Load keys
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_image(keyword, index):
    print(f"📷 Searching Pexels for: '{keyword}'...")
    
    url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=1&orientation=landscape"
    headers = {"Authorization": PEXELS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("photos") and len(data["photos"]) > 0:
            img_url = data["photos"][0]["src"]["large"]
            img_data = requests.get(img_url).content
            
            filename = f"slide_{index}.jpg"
            with open(filename, 'wb') as f:
                f.write(img_data)
            return filename
    except Exception as e:
        print(f"❌ Error fetching {keyword}: {e}")
        
    print(f"⚠️ Could not find image for '{keyword}'.")
    return None

def build_video():
    print("🎬 1. Loading slide data and audio track...")
    
    if not os.path.exists("slide_data.json") or not os.path.exists("news_voiceover.mp3"):
        print("❌ Error: Missing slide_data.json or news_voiceover.mp3. Run script_voice_gen.py first!")
        return
        
    with open("slide_data.json", "r", encoding="utf-8") as f:
        slides = json.load(f)
        
    audio = AudioFileClip("news_voiceover.mp3")
    
    duration_per_slide = audio.duration / len(slides)
    print(f"⏱️ Total Audio: {audio.duration:.1f}s. Each of the {len(slides)} slides will show for {duration_per_slide:.1f}s.")
    
    image_clips = []
    
    for i, slide in enumerate(slides):
        img_path = fetch_image(slide["image_keyword"], i)
        
        if img_path:
            # V2 Syntax: with_duration instead of set_duration
            clip = ImageClip(img_path).with_duration(duration_per_slide)
            image_clips.append(clip)
            
    if not image_clips:
        print("❌ No images were successfully downloaded. Aborting.")
        return

    print("\n🎞️ 2. Stitching images together...")
    final_video = concatenate_videoclips(image_clips, method="compose")
    
    # V2 Syntax: with_audio instead of set_audio
    final_video = final_video.with_audio(audio)
    
    output_filename = "final_daily_news.mp4"
    print(f"\n💾 3. Rendering final video to {output_filename}...")
    print("⏳ (This might take a minute or two depending on your CPU)")
    
    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    
    print("\n✅ Video rendering complete!")

if __name__ == "__main__":
    build_video()