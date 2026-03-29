import os
import asyncio
import brain
import voice
from config import COMPANY_TO_TEARDOWN, HOST_1_NAME, HOST_2_NAME

# --- THE RUTHLESS EXECUTIVE PRODUCER PROMPT ---
EDITOR_PROMPT = f"""
Role: You are the Executive Producer of a top-tier Product Management podcast (think Acquired or Lenny's Podcast) and a former Principal Product Manager.
Task: You are reviewing a draft script for a product teardown of {{company}}. Your job is to rewrite it so it is wildly engaging to listen to, but absolutely ruthless and precise in its business and product analysis. Do not accept surface-level PR narratives or "happy path" assumptions.

Rules for the Rewrite:
1. Eradicate AI Fluff & Platitudes: Completely remove robotic language, overly enthusiastic agreements, and filler (e.g., "Ah, yes," "In conclusion," "It's important to note," "That's a delicate balance"). Make it sound like two incredibly sharp PMs having a beer and dissecting a business.
2. Introduce Friction & Debate: {HOST_1_NAME} and {HOST_2_NAME} should not just blindly agree with each other. Have them push back! If one suggests a metric or a feature, the other should challenge its unit economics, scalability, or potential legal/regulatory risks.
3. Enforce Ruthless Product Rigor: You MUST inject hard business realities into the conversation. Focus on:
   - Unit Economics: Talk about margins, take rates, and profitability, not just raw volume.
   - Operational Bottlenecks: Why don't certain features scale? (e.g., human-in-the-loop dependencies, high friction).
   - Second-Order Effects: How does the product create negative externalities (e.g., regulatory backlash, cannibalization, game theory among competitors)?
4. Sharpen the Vernacular: Use real product and marketplace terminology natively (e.g., cross-side network effects, liquidity, LTV:CAC, churn cohorts, first-mover disadvantage).

CRITICAL FORMATTING: You must perfectly maintain the line-by-line formatting below. Return ONLY the polished script, with no intro or outro text.
[{HOST_1_NAME}]: <text>
[{HOST_2_NAME}]: <text>
"""

def main():
    # 1. Setup the Output Directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Workspace ready. Outputs will be routed to ./{output_dir}/")

    print(f"\n🚀 Starting Product Teardown for: {COMPANY_TO_TEARDOWN}")
    print("-" * 50)

    # 2. Generate Draft
    brain.generate_draft(COMPANY_TO_TEARDOWN, output_dir)
    
    # 3. AI Editor Review
    brain.run_ai_editor(COMPANY_TO_TEARDOWN, EDITOR_PROMPT, output_dir)
    
    # 4. Human Review Pause
    print("\n" + "="*50)
    print("🛑 PAUSED FOR HUMAN REVIEW 🛑")
    print(f"1. Open '{output_dir}/draft_script.txt' in Cursor.")
    print("2. Make any final tweaks.")
    print(f"3. Ensure all spoken lines still start with [{HOST_1_NAME}]: or [{HOST_2_NAME}]:")
    print("4. Save the file.")
    print("="*50 + "\n")
    
    input("Press ENTER when you are ready to generate the final audio...")
    
    # 5. Final Audio Generation
    asyncio.run(voice.build_audio(output_dir))
    
    print(f"\n✅ COMPLETE! Your podcast is ready in: {output_dir}/final_podcast.mp3")

# 6. Publish to the Web
    title, notes = publisher.generate_metadata(output_dir)
    publisher.write_rss_feed(title, notes, output_dir)
    publisher.push_to_github()
    
    print("\n🎉 AGENT RUN COMPLETE. Episode is live on the internet!")


if __name__ == "__main__":
    main()