import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import sounddevice as sd
import speech_recognition as sr
import wave
import time
import sys


MEETING_DIR = Path(__file__).resolve().parent / "meeting_notes"
MEETING_DIR.mkdir(parents=True, exist_ok=True)


def record_audio(duration=7, sample_rate=16000, channels=1):
    print("Listening... speak now.")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="int16",
    )
    sd.wait()
    return recording


def save_audio_file(audio_data, sample_rate=16000, channels=1):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = MEETING_DIR / f"meeting_{timestamp}.wav"

    # Determine sample width (bytes per sample)
    try:
        sample_width = audio_data.dtype.itemsize
    except Exception:
        sample_width = 2

    # Write a proper WAV file with header
    with wave.open(str(filename), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio saved to: {filename}")
    return filename


def transcribe_audio(audio_data, sample_rate=16000):
    recognizer = sr.Recognizer()
    audio_bytes = audio_data.tobytes()
    try:
        sample_width = audio_data.dtype.itemsize
    except Exception:
        sample_width = 2

    audio = sr.AudioData(audio_bytes, sample_rate, sample_width)

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"API error during transcription (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                time.sleep(0.5 * attempt)
                continue
            return ""


def summarize_transcript(transcript):
    cleaned = transcript.strip()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]

    action_keywords = ["action item", "next step", "todo", "need to", "should", "will", "follow up"]
    action_items = []
    for sentence in sentences:
        lower_text = sentence.lower()
        if any(keyword in lower_text for keyword in action_keywords):
            action_items.append(sentence)

    summary_sentences = sentences[:3] if len(sentences) >= 3 else sentences
    summary = " ".join(summary_sentences) if summary_sentences else "No spoken content captured."

    return {
        "summary": summary,
        "action_items": action_items or ["No explicit action items detected."],
        "word_count": len(cleaned.split()),
    }


def save_meeting_notes(transcript, summary_result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = MEETING_DIR / f"meeting_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    payload = {
        "timestamp": timestamp,
        "transcript": transcript,
        "summary": summary_result["summary"],
        "action_items": summary_result["action_items"],
        "word_count": summary_result["word_count"],
    }

    filename.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Meeting notes saved to: {filename}")
    return filename


def run_live_meeting(duration=7):
    audio_data = record_audio(duration=duration)
    save_audio_file(audio_data)
    transcript = transcribe_audio(audio_data)
    summary_result = summarize_transcript(transcript)
    save_meeting_notes(transcript, summary_result)

    print("\nTranscript:")
    print(transcript)
    print("\nMeeting Summary:")
    print(summary_result["summary"])
    print("\nAction Items:")
    for item in summary_result["action_items"]:
        print(f"- {item}")


def run_demo():
    demo_transcript = (
        "Hi team, we discussed the launch plan today. "
        "We need to finalize the budget by Friday. "
        "Next step is to send the proposal to the client. "
        "Action item: Maya will prepare the slides."
    )
    summary_result = summarize_transcript(demo_transcript)
    save_meeting_notes(demo_transcript, summary_result)

    print("\nDemo Transcript:")
    print(demo_transcript)
    print("\nMeeting Summary:")
    print(summary_result["summary"])
    print("\nAction Items:")
    for item in summary_result["action_items"]:
        print(f"- {item}")


def parse_tasks_from_transcript(transcript):
    if not transcript:
        return []

    # Split by linebreaks, semicolons, or sentence boundaries
    parts = [p.strip() for p in re.split(r"[\n;]+|(?<=[.!?])\s+| and | then ", transcript) if p.strip()]

    tasks = []
    for p in parts:
        # Keep task titles short (max 7 words)
        words = p.split()
        title = " ".join(words[:7])
        # Remove trailing punctuation
        title = title.strip().rstrip(".,:;!")
        if title:
            tasks.append(title)

    return tasks


def run_voice_task_capture(duration=10):
    print("Please speak your tasks after the prompt. Recording will start shortly...")
    time.sleep(0.5)
    audio_data = record_audio(duration=duration)
    audio_path = save_audio_file(audio_data)
    transcript = transcribe_audio(audio_data)

    print("\nCaptured Transcript:")
    print(transcript or "(no transcript)")

    tasks = parse_tasks_from_transcript(transcript)
    if not tasks:
        print("No tasks detected in your speech.")
        if not sys.stdin.isatty():
            print("Interactive input not available in this environment.")
            print("Run the script with `--type-tasks` to enter tasks by typing, or run in an interactive terminal.")
            return []

        # Prompt the user to type tasks interactively
        print("Please type your tasks now, one per line. Enter an empty line when done.")
        typed_lines = []
        try:
            while True:
                line = input().strip()
                if not line:
                    break
                typed_lines.append(line)
        except EOFError:
            pass

        for p in typed_lines:
            words = p.split()
            title = " ".join(words[:7]).strip().rstrip(".,:;!")
            if title:
                tasks.append(title)

        if not tasks:
            print("No tasks entered. Exiting voice-tasks mode.")
            return []


def run_type_task_capture():
    if not sys.stdin.isatty():
        print("Interactive input not available in this environment.")
        return []

    print("Please type your tasks now, one per line. Enter an empty line when done.")
    typed_lines = []
    try:
        while True:
            line = input().strip()
            if not line:
                break
            typed_lines.append(line)
    except EOFError:
        pass

    tasks = []
    for p in typed_lines:
        words = p.split()
        title = " ".join(words[:7]).strip().rstrip(".,:;!")
        if title:
            tasks.append(title)

    if not tasks:
        print("No tasks entered.")
    else:
        print("\nDetected Tasks:")
        for t in tasks:
            print(f"- {t}")

    return tasks


def save_tasks_to_file(tasks):
    if not tasks:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = MEETING_DIR / f"todo_{timestamp}.json"

    payload = []
    for i, t in enumerate(tasks, start=1):
        payload.append({"id": i, "title": t, "status": "not-started"})

    filename.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Tasks saved to: {filename}")
    return filename



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI meeting assistant mini project")
    parser.add_argument("--duration", type=int, default=7, help="Seconds to record for live mode")
    parser.add_argument("--demo", action="store_true", help="Run with a built-in sample transcript")
    parser.add_argument("--voice-tasks", action="store_true", help="Record spoken tasks and convert to todo list")
    parser.add_argument("--type-tasks", action="store_true", help="Type tasks interactively without recording")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.voice_tasks:
        tasks = run_voice_task_capture(duration=args.duration)
        if tasks:
            saved = save_tasks_to_file(tasks)
            print("\n---TASKS LIST START---")
            for i, t in enumerate(tasks, start=1):
                print(f"{i}. {t} — not-started")
            print("---TASKS LIST END---")
        else:
            print("No tasks captured.")
    elif args.type_tasks:
        tasks = run_type_task_capture()
        # Save and print tasks as a simple numbered list for external consumption
        if tasks:
            saved = save_tasks_to_file(tasks)
            print("\n---TASKS LIST START---")
            for i, t in enumerate(tasks, start=1):
                print(f"{i}. {t} — not-started")
            print("---TASKS LIST END---")
    else:
        run_live_meeting(duration=args.duration)
