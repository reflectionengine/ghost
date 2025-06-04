"""
Utility functions to handle data input/output operations for the Ghost Protocol Dashboard.
Includes:
- Loading and saving JSON files
- Loading YAML config files
- Fetching mock outputs from predefined structure

Dependencies:
- json
- yaml (PyYAML)

Usage:
from utils.io import load_json, load_yaml, get_mock_output_by_id
"""

import json
import yaml
from typing import Any, Dict


def load_json(path: str) -> Dict[str, Any]:
    """Load a JSON file from disk."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: str, data: Dict[str, Any]) -> None:
    """Save a dictionary to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_yaml(path: str) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_mock_output_by_id(data: Dict[str, Any], identifier: str) -> Dict[str, Any]:
    """Fetch a specific mock entry from mock_outputs.json by ID."""
    return data.get(identifier, {})
