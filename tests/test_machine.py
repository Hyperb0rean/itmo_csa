import contextlib
import io
import json
import logging
import os
import tempfile

import pytest
from machine import computer
from translator import perform_translator


@pytest.mark.golden_test("golden/*.yml")
def test_bar(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdir:
        source_file = os.path.join(tmpdir, "source.vasm")
        target_file = os.path.join(tmpdir, "source.json")
        input_token = [ord(i) for i in golden["stdin"]]
        input_token.append(0)

        with open(source_file, "w", encoding="utf-8") as file:
            file.write(golden["source_code"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            perform_translator(golden["source_code"], target_file)
            print("=" * 25)
            code_dict = json.load(open(target_file, encoding="utf-8"))
            computer(code_dict, input_token)

        with open(target_file, encoding="utf-8") as file:
            human_readable = file.read()

        assert human_readable.rstrip("\n") == golden.out["out_code_readable"]
        assert stdout.getvalue().rstrip("\n") == golden.out["stdout"]
        assert caplog.text.rstrip("\n") == golden.out["out_log"]
