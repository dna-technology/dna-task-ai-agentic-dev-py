import logging
import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv("../.env")

from src.app import app  # noqa: E402

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    port = os.getenv("PORT")
    logger.info(f"ChargeShield API listening on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=int(port))
