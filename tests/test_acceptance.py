from os import listdir
from pathlib import Path

import pytest

from express_env.cli import main

cases = []

cases_dir = Path(__file__).parent / "cases"

for path in listdir(cases_dir):
    files = listdir(cases_dir / path)
    if ".env" in files:
        cases.append([path, ".env", "dotenv"])

    if "env.sh" in files:
        cases.append([path, "env.sh", "bash"])


@pytest.mark.parametrize("path,out_file,format", cases)
def test_from_directories(path: Path, out_file, format, capsys):
    config_file = cases_dir / path / "default.yml"

    result_file = cases_dir / path / out_file
    main(["--config", config_file.as_posix(), "generate", "--format", format])
    captured = capsys.readouterr()
    assert captured.out == open(result_file).read()
