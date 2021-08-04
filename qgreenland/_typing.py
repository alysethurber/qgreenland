"""QGreenland type definitions.

NOTE: This module is named strangely to avoid conflicts with the stdlib's
`types` module.
"""
from typing import Any, Dict, Literal


ConfigStepType = Literal['command', 'python', 'template']
