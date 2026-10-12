# Classroom demo guide

## Before class

1. Run `.\Start-Demo.ps1` and open http://localhost:5001. The top of the page should say "Server connected."
2. Ask one question with **F5-TTS (model)** so the model is loaded and you know how long it takes. Write the times on slide 13.
3. Keep a short recording of a Spanish question (for example "¿Hablas criollo?") ready, in case the microphone acts up.

## Three-minute walkthrough

1. Type **What languages can you speak?** Show the answer, the matched question and the similarity score.
2. Upload or say **¿Hablas criollo?** Show Whisper's transcript, the detected language (Spanish), the English translation used for matching, and the English answer. Explain that Sky answers in English for now because F5-TTS's base model was trained on English and Chinese, not Spanish.
3. Type **How much is tuition?** The score is below 0.5, so Sky says to ask a staff member instead of guessing.
4. Play an answer with **F5-TTS (model)** and point out the wait time.

## Backups

- Microphone not working: upload the recording, or type the question.
- F5-TTS too slow or offline: use **Browser voice (fast)** and say it is the browser's voice, not the model.
- Web page problem: use the command-line version, `.\Run-CLI.ps1 -Text "What is Sky?"`.

## What to explain

Whisper turns speech into text. TF-IDF and cosine similarity (Week 6) pick the closest FAQ question. The TTS server from Week 4 turns the answer into speech with F5-TTS. Current limits: exact-word matching, a six-topic FAQ, English-only answers (the voice model has no Spanish training), and generation time.
