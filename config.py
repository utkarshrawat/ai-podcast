import os
from dotenv import load_dotenv

load_dotenv()

# --- THE TEAM ---
HOST_1_NAME = "Utkarsh"  # Change this to whatever you like
HOST_2_NAME = "Anshuly"   # Change this to whatever you like

# --- VOICE OPTIONS (Choose one for each host) ---
# MALE 1: "en-US-GuyNeural" (Professional, standard)
# MALE 2: "en-US-ChristopherNeural" (Slightly deeper, news-like)
# FEMALE 1: "en-US-AriaNeural" (Highly expressive, conversational)
# FEMALE 2: "en-US-EmmaNeural" (Bright, friendly)

HOST_1_VOICE = "en-US-ChristopherNeural" 
HOST_2_VOICE = "en-US-EmmaNeural"

# --- PROJECT SETTINGS ---
COMPANY_TO_TEARDOWN = "Airbnb"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- HOSTING SETTINGS ---
GITHUB_USERNAME = "YourGitHubUsername"
GITHUB_REPO_NAME = "ai-podcast" # The name of the repo you just created
PODCAST_NAME = "The AI PM Teardown"
PODCAST_DESC = "Two AI agents ruthlessly tearing down product strategies."