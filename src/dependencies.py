from fastapi import Body
from loguru import logger
from .schemas import TextModelRequest
from .scraper import extract_urls, fetch_all

async def get_urls_content(body: TextModelRequest = Body(...)) -> str: #1
    urls = extract_urls(body.prompt)
    if urls:
        try:
            urls_content = await fetch_all(urls)
            return urls_content
        except Exception as e:
            logger.warning(f"Failed to fetch one or several URLs - Error: {e}")
    return ""  

"""
#1 Implement a get_urls_content FastAPI dependency that gets a user prompt from
the request body and finds all URLs. It then returns the content of all URLs
as a long string. The dependency has exception handling built in to handle
any I/O errors by returning an empty string and logging a warning on the
server.
"""