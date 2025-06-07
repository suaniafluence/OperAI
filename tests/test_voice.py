from io import BytesIO
from unittest import mock

from fastapi.testclient import TestClient

import app.models as models
models.PyObjectId = str
from app.main import app
from app import voice

client = TestClient(app)


def test_transcribe(monkeypatch):
    fake_resp = mock.Mock()
    fake_resp.text = 'hello'
    monkeypatch.setattr(voice, 'client', mock.Mock())
    voice.client.audio.transcriptions.create.return_value = fake_resp

    file_content = BytesIO(b'audio')
    response = client.post('/transcribe', files={'file': ('test.wav', file_content, 'audio/wav')})
    assert response.status_code == 200
    assert response.json()['text'] == 'hello'
