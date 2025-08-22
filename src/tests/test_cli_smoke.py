# Basic smoke tests for CLI
# Focus: import and running list() without exceptions

import importlib


def test_cli_import() -> None:
    mod = importlib.import_module("src.cli")
    assert hasattr(mod, "app")
