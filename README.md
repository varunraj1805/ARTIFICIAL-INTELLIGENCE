# ARTIFICIAL-INTELLIGENCE
## AI Meeting Assistant

An AI-powered meeting assistant that records voice input, converts speech to text, summarizes meetings, extracts action items, and automatically creates a to-do list from spoken conversations. The assistant helps users stay organized by transforming meeting discussions into structured tasks with deadlines and priorities.

## Features

* Voice recording during meetings
* Speech-to-text transcription
* AI-generated meeting summaries
* Automatic extraction of action items
* Voice-based to-do list creation
* Priority detection (High / Medium / Low)
* Due date recognition from speech
* Task completion tracking
* Export notes and tasks
* Simple and user-friendly interface

## How it works

1. Start recording the meeting.
2. The assistant captures voice input.
3. Speech is converted into text using speech recognition.
4. AI analyzes the transcript.
5. Important decisions and action items are extracted.
6. A structured to-do list is automatically generated.

### Example

**Voice input**

“Call the client tomorrow morning, finish the AI presentation by Friday, and send the project report to the professor.”

**Generated to-do list**

* Call the client — Tomorrow morning
* Finish the AI presentation — Friday
* Send the project report to the professor — Pending

## Technologies used

* Python
* SpeechRecognition
* OpenAI / NLP
* Tkinter or Streamlit
* PyAudio
* Transformers (optional)
* SQLite or JSON

## Project structure

ai-meeting-assistant/

* app.py
* speech_to_text.py
* summarizer.py
* todo_extractor.py
* tasks.json
* requirements.txt
* README.md

## Installation

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

## Future enhancements

* Speaker identification
* Calendar integration
* Email reminders
* Multi-language support
* Cloud synchronization
* Mobile application support

## Applications

* Business meetings
* College project discussions
* Team stand-ups
* Online classes
* Personal productivity

## Sample workflow

Record voice → Speech-to-text → AI summary → Task extraction → To-do list generation

## Conclusion

AI Meeting Assistant reduces manual note-taking by automatically summarizing meetings and converting spoken action items into an organized to-do list. It improves productivity, ensures important tasks are not missed, and provides a smart voice-driven meeting management solution.
