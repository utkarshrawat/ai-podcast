import os
import asyncio
import brain
import voice
import publisher
from config import COMPANY_TO_TEARDOWN, HOST_1_NAME, HOST_2_NAME

# --- THE RUTHLESS EXECUTIVE PRODUCER PROMPT ---
EDITOR_PROMPT = f"""
Role: You are the Executive Producer of a top-tier Product Management podcast (think Acquired or Lenny's Podcast) and a former Principal Product Manager.
Task: You are reviewing a draft script for a product teardown of {{company}}. Your job is to rewrite it so it is wildly engaging to listen to, but absolutely ruthless and precise in its business and product analysis. Do not accept surface-level PR narratives or "happy path" assumptions.

Rules for the Rewrite:
1. Eradicate AI Fluff & Platitudes: Completely remove robotic language, overly enthusiastic agreements, and filler.
2. Introduce Friction & Debate: {HOST_1_NAME} and {HOST_2_NAME} should not just blindly agree with each other. Have them push back!
3. Enforce Ruthless Product Rigor: Inject hard business realities (Unit Economics, Operational Bottlenecks, Second-Order Effects).
4. Sharpen the Vernacular: Use real product and marketplace terminology natively.

CRITICAL FORMATTING: You must perfectly maintain the line-by-line formatting below. Return ONLY the polished script, with no intro or outro text.
[{HOST_1_NAME}]: <text>
[{HOST_2_NAME}]: <text>
"""

def main():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    draft_path = os.path.join(output_dir, "draft_script.txt")
    audio_path = os.path.join(output_dir, "final_podcast.mp3")

    print(f"\n🚀 Starting Product Teardown for: {COMPANY_TO_TEARDOWN}")
    print("-" * 50)

    # ---------------------------------------------------------
    # STEP 1 & 2: SCRIPT GENERATION (State Aware)
    # ---------------------------------------------------------
    if os.path.exists(draft_path):
        skip_text = input(f"📝 Found existing draft script. Skip AI generation and use it? (y/n): ").strip().lower()
        if skip_text != 'y':
            brain.generate_draft(COMPANY_TO_TEARDOWN, output_dir)
            brain.run_ai_editor(COMPANY_TO_TEARDOWN, EDITOR_PROMPT, output_dir)
        else:
            print("⏭️  Skipping script generation...")
    else:
        brain.generate_draft(COMPANY_TO_TEARDOWN, output_dir)
        brain.run_ai_editor(COMPANY_TO_TEARDOWN, EDITOR_PROMPT, output_dir)

    # ---------------------------------------------------------
    # STEP 3: HUMAN REVIEW
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("🛑 PAUSED FOR HUMAN REVIEW 🛑")
    print(f"1. Open '{draft_path}' in Cursor.")
    print("2. Make any final tweaks.")
    print("3. Save the file.")
    print("="*50 + "\n")
    
    input("Press ENTER when you are ready to proceed...")

    # ---------------------------------------------------------
    # STEP 4: AUDIO GENERATION (State Aware)
    # ---------------------------------------------------------
    if os.path.exists(audio_path):
        skip_audio = input(f"\n🎵 Found existing audio file. Skip TTS generation and use it? (y/n): ").strip().lower()
        if skip_audio != 'y':
            asyncio.run(voice.build_audio(output_dir))
        else:
            print("⏭️  Skipping audio generation...")
    else:
        asyncio.run(voice.build_audio(output_dir))

    # ---------------------------------------------------------
    # STEP 5: PUBLISH TO WEB
    # ---------------------------------------------------------
    print("\n🌐 Starting Publishing Process...")
    title, notes = publisher.generate_metadata(output_dir)
    publisher.write_rss_feed(title, notes, output_dir)
    publisher.push_to_github()
    
    print("\n🎉 AGENT RUN COMPLETE! Your podcast is live on the internet.")

if __name__ == "__main__":
    main()