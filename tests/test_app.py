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

    def test_spanish_answer(self):
        response = self.ask("What is Sky?", "es")
        self.assertEqual(response.json["language"], "es")
        self.assertIn("Soy Sky", response.json["answer"])

    def test_validation(self):
        for payload in [None, [], {}, {"text": 2}, {"text": ""}, {"text": "Sky", "language": "fr"}]:
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


if __name__ == "__main__":
    unittest.main()
