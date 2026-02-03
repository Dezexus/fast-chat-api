import logging
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("Starting FastChat API...")

app = FastAPI(title="FastChat API")

app.include_router(api_router, prefix=settings.API_V1_STR)
