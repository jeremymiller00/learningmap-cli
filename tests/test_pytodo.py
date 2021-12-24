# tests/test_pytodo.py

from typer.main import run
from typer.testing import CliRunner
from pytodo import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout