"""Checks for the Sky demo web app. Whisper and F5-TTS are not loaded here."""
import io
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests  # noqa: E402

import app  # noqa: E402


class SkyDemoTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def ask(self, text, language="en"):
        return self.client.post("/demo/answer", json={"text": text, "language": language})

    def test_known_and_unknown_questions(self):
        known = self.ask("What is Sky?")
        self.assertEqual(known.status_code, 200)
        self.assertFalse(known.json["fallback"])
        self.assertIn("Sky", known.json["answer"])
        unknown = self.ask("How much is tuition?")
        self.assertTrue(unknown.json["fallback"])
        self.assertIn("staff", unknown.json["answer"])

    def test_voice_recognition_question_matches_stt_topic(self):
        response = self.ask("How do you recognize my voice?")
        self.assertIn("Whisper", response.json["answer"])

    def test_answers_are_english(self):
        response = self.client.post("/demo/answer", json={"text": "What is Sky?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["language"], "en")
        self.assertIn("I am Sky", response.json["answer"])

    def test_spoken_spanish_gets_english_answer(self):
        heard = ("¿Reconoces mi voz?", "es", "Do you recognize my voice?")
        with patch.dict(sys.modules, {"whisper": MagicMock()}), \
             patch.object(app, "speech_to_text", return_value=heard), \
             patch.object(app, "whisper_model", MagicMock()):
            data = {"file": (io.BytesIO(b"fake audio"), "q.wav")}
            response = self.client.post("/demo/transcribe", data=data,
                                        content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["spoken_language"], "es")
        self.assertEqual(response.json["language"], "en")
        self.assertIn("A speech to text model called Whisper", response.json["answer"])

    def test_validation(self):
        for payload in [None, [], {}, {"text": 2}, {"text": ""}]:
            self.assertEqual(self.client.post("/demo/answer", json=payload).status_code, 400)
        self.assertEqual(self.client.post("/demo/transcribe").status_code, 400)
        self.assertEqual(self.client.post("/tts", json=[]).status_code, 400)

    def test_uploads_rejected(self):
        for filename, content in [("q.wav", b""), ("q.txt", b"hello")]:
            response = self.client.post("/demo/transcribe", data={"file": (io.BytesIO(content), filename)})
            self.assertEqual(response.status_code, 400)

    def test_pages(self):
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/studio").status_code, 302)

    def test_tts_server_offline(self):
        with patch.object(app.requests, "get", side_effect=requests.ConnectionError()):
            health = self.client.get("/health").json
        self.assertEqual(health["status"], "running")
        self.assertEqual(health["tts_status"], "offline")
        with patch.object(app.requests, "post", side_effect=requests.ConnectionError()):
            response = self.client.post("/tts", json={"username": "default", "text": "Hi"})
        self.assertEqual(response.status_code, 503)

    def test_tts_forwarded(self):
        fake = MagicMock(status_code=200, content=b"RIFFdata", headers={"Content-Type": "audio/wav"})
        with patch.object(app.requests, "post", return_value=fake) as post:
            response = self.client.post("/tts", json={"username": "default", "text": "Hi"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"RIFFdata")
        self.assertTrue(post.call_args[0][0].endswith("/tts"))

    def test_saved_answer_plays_without_tts(self):
        import tempfile
        from pathlib import Path
        wav = b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 40
        with tempfile.TemporaryDirectory() as folder, patch.object(app, "SAVED_DIR", Path(folder)):
            # nothing saved yet: the TTS server is asked
            fake = MagicMock(status_code=200, content=wav, headers={"Content-Type": "audio/wav"})
            with patch.object(app.requests, "post", return_value=fake) as post:
                first = self.client.post("/tts", json={"username": "default", "text": "Hi"})
            self.assertEqual(first.headers["X-Sky-Source"], "generated")
            self.assertEqual(post.call_count, 1)
            # save it, then the same answer plays without calling the TTS server
            saved = self.client.post("/demo/save_answer", content_type="multipart/form-data", data={
                "file": (io.BytesIO(wav), "answer.wav"), "username": "default", "text": "Hi"})
            self.assertEqual(saved.status_code, 200)
            with patch.object(app.requests, "post") as post:
                second = self.client.post("/tts", json={"username": "default", "text": "Hi"})
            post.assert_not_called()
            self.assertEqual(second.headers["X-Sky-Source"], "saved")
            self.assertEqual(second.data, wav)
            # a different answer is not affected, and non-WAV uploads are refused
            bad = self.client.post("/demo/save_answer", content_type="multipart/form-data", data={
                "file": (io.BytesIO(b"not audio"), "x.wav"), "username": "default", "text": "Hi"})
            self.assertEqual(bad.status_code, 400)
            cleared = self.client.post("/demo/clear_saved").json
            self.assertEqual(cleared["removed"], 1)


if __name__ == "__main__":
    unittest.main()
