import os
import tempfile
from unittest import mock

import pytest

from app import utils


def test_generate_pdf_creates_file(tmp_path):
    file_name = 'test.pdf'
    lines = ['line1', 'line2']
    with mock.patch.object(utils, 'settings') as settings_mock:
        settings_mock.LOCAL_STORAGE_PATH = tmp_path
        path = utils.generate_pdf(file_name, lines)

    assert os.path.exists(path)
    with open(path, 'rb') as f:
        content = f.read()
    assert len(content) > 0


@pytest.mark.asyncio
async def test_process_natural_language_returns_text():
    class FakeResp:
        text = 'processed'

    def fake_create(**kwargs):
        return FakeResp()

    with mock.patch.object(utils.client.responses, 'create', side_effect=fake_create):
        text = await utils.process_natural_language('hello')
    assert text == 'processed'
