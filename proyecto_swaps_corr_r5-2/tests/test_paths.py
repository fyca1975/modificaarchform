# tests/test_paths.py
from pathlib import Path
from file_path import load_paths

def test_paths_exist_and_are_dirs():
    rutas = load_paths()
    assert Path(rutas["INPUT_DIR"]).exists() and Path(rutas["INPUT_DIR"]).is_dir()
    assert Path(rutas["OUTPUT_DIR"]).exists() and Path(rutas["OUTPUT_DIR"]).is_dir()
    assert Path(rutas["LOG_DIR"]).exists() and Path(rutas["LOG_DIR"]).is_dir()
