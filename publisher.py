import os
import time
from email.utils import formatdate
from git import Repo
from google import genai
from config import GEMINI_API_KEY, GITHUB_USERNAME, GITHUB_REPO_NAME, PODCAST_NAME, PODCAST_DESC

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_metadata(output_dir):
    print("\n📝 1. Asking AI to write Title and Show Notes...")
    
    draft_path = os.path.join(output_dir, "draft_script.txt")
    if not os.path.exists(draft_path):
        return "New Episode", "Tune in to this product teardown."

    with open(draft_path, "r", encoding="utf-8") as f:
        script_text = f.read()
        
    prompt = f"""
    You are a podcast marketer. Read this script and write:
    1. A catchy, high-stakes podcast title (under 60 characters).
    2. A 3-sentence engaging summary for the show notes.
    
    Format EXACTLY like this (no markdown, no extra text):
    TITLE: <your title>
    NOTES: <your notes>
    
    Script:
    {script_text[:3000]}
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        lines = response.text.strip().split('\n')
        
        title = "New Episode"
        notes = "Tune in to this product teardown."
        
        # Safely parse the AI's response
        for line in lines:
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
            elif line.startswith("NOTES:"):
                notes = line.replace("NOTES:", "").strip()
                
        return title, notes
    except Exception as e:
        print(f"⚠️ Could not generate metadata with AI: {e}")
        return "New Episode", "Tune in to this product teardown."

def write_rss_feed(title, notes, output_dir):
    print("📻 2. Generating RSS feed.xml...")
    
    mp3_path = os.path.join(output_dir, "final_podcast.mp3")
    mp3_url = f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPO_NAME}/output/final_podcast.mp3"
    
    # Spotify strictly requires the exact file size in bytes
    file_length = os.path.getsize(mp3_path) if os.path.exists(mp3_path) else 0
    pub_date = formatdate(time.time(), localtime=False)
    
    # Valid RSS Template for Spotify, including the owner verification block
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{PODCAST_NAME}</title>
    <description>{PODCAST_DESC}</description>
    <link>https://{GITHUB_USERNAME}.github.io/{GITHUB_REPO_NAME}/</link>
    <language>en-us</language>
    <itunes:owner>
      <itunes:name>{GITHUB_USERNAME}</itunes:name>
      <itunes:email>utkarshrawat11@gmail.com</itunes:email>
    </itunes:owner>
    <item>
      <title>{title}</title>
      <description>{notes}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{mp3_url}" type="audio/mpeg" length="{file_length}"/>
      <guid>{mp3_url}</guid>
    </item>
  </channel>
</rss>"""

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

def push_to_github():
    print("🌐 3. Pushing episode to GitHub Servers...")
    try:
        repo = Repo(os.getcwd())
        repo.git.add(all=True)
        repo.index.commit(f"Auto-Publish Episode: {formatdate(time.time())}")
        origin = repo.remote(name='origin')
        origin.push()
        print(f"✅ SUCCESS! Your RSS feed is live at: https://{GITHUB_USERNAME}.github.io/{GITHUB_REPO_NAME}/feed.xml")
    except Exception as e:
        print(f"❌ Git Push Failed: {e}")