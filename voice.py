import os
import re
import asyncio
import edge_tts
from moviepy import AudioFileClip, concatenate_audioclips
from config import HOST_1_NAME, HOST_2_NAME, HOST_1_VOICE, HOST_2_VOICE

async def build_audio(output_dir):
    input_path = os.path.join(output_dir, "draft_script.txt")
    output_path = os.path.join(output_dir, "final_podcast.mp3")
    
    print(f"\n📖 Parsing script from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pattern = re.compile(r'^\[(.*?)]: (.*)', re.IGNORECASE)
    audio_clips = []
    temp_files = []

    # Use a safe fallback in case someone typos a name in the text file
    for i, line in enumerate(lines):
        match = pattern.match(line.strip())
        if match:
            speaker = match.group(1).strip()
            text = match.group(2).strip()
            
            if speaker.lower() == HOST_1_NAME.lower():
                voice = HOST_1_VOICE
            else:
                voice = HOST_2_VOICE
            
            temp_file = os.path.join(output_dir, f"temp_{i}.mp3")
            await edge_tts.Communicate(text, voice).save(temp_file)
            
            clip = AudioFileClip(temp_file)
            audio_clips.append(clip)
            temp_files.append(temp_file)

    if not audio_clips:
        print("❌ Error: No valid dialogue lines found to generate.")
        return

    print("🎞️ Stitching audio together...")
    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile(output_path, logger=None)

    print("🧹 Cleaning up temporary audio chunks...")
    for clip in audio_clips:
        clip.close()
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)