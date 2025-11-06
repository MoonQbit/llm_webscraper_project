from fastapi import Body, Depends, Request, FastAPI
from .dependencies import get_urls_content
from .schemas import TextModelRequest, TextModelResponse
from .models import load_text_model, generate_text, delete_model
from contextlib import asynccontextmanager
from typing import AsyncIterator

models = {}

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
	# Load tinyml model
    models["text"] = load_text_model()
    yield
    # Clean up the LLM models and release the resources
    delete_model()
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/generate/text", response_model_exclude_defaults=True) #2
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content) #3
    ) -> TextModelResponse:
        prompt = body.prompt + " " + urls_content
        output = generate_text(models["text"], prompt, body.temperature)
        return TextModelResponse(content=output, ip=request.client.host)

"""
#2 When using aiohttp inside FastAPI, you don’t need to manage the event loop
yourself because FastAPI, as an asynchronous framework, handles the event loop.
You can define your endpoint as an async function and use aiohttp to make
asynchronous HTTP requests within the handler or via a dependency like in this
example.
"""

"""
#3 Inject the results of the get_urls_content dependency call to the handler via
the FastAPI’s Depends class. Using a FastAPI dependency here kept the controller
logic small, clean, and readable.
"""