from os import listdir
from pathlib import Path

import pytest

from express_env.cli import main

cases = Path(__file__).parent / "cases"


@pytest.mark.parametrize("path", listdir(cases))
def test_from_directories(path: Path, capsys):
    config_file = cases / path / "default.yml"
    result_file = cases / path / ".env"
    main(["--config", config_file.as_posix(), "generate", "-"])
    captured = capsys.readouterr()
    assert captured.out == open(result_file).read()
