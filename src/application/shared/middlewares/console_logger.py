from fastapi import Request

from core.utils.logger.logger import console_logger


async def log_to_console(request: Request, call_next):
    console_logger.info(f"Received Request: {request.method} {request.url}")
    response = await call_next(request)
    console_logger.info(f"Sent Response: {response}")
    return response