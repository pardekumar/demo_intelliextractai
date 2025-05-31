import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Paths:
    root: Path = Path(__file__).parent
    data: Path = root / "upload"

    pdf_upload: Path = (
          data
          / "pdf"
    )
