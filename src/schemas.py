from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress, PositiveInt

class ModelRequest(BaseModel):
	prompt: Annotated[str, Field(min_length=1, max_length=10000)] #1

class ModelResponse(BaseModel):
	request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)] #2

	ip: Annotated[str, IPvAnyAddress] | None #3
	content: Annotated[str | None, Field(min_length=0, max_length=10000)] #4
	created_at: datetime = datetime.now()

class TextModelRequest(ModelRequest):
	model: Literal["TinyLlama/TinyLlama-1.1B-Chat-v1.0"]
	temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.7)] #5

class TextModelResponse(ModelResponse):
	temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.7)]


ImageSize = Annotated[ #6
	tuple[PositiveInt, PositiveInt], "Width and height of an image in pixels"
]

class ImageModelRequest(ModelRequest):
	model: Literal["tinysd", "sd1.5"]
	output_size: ImageSize #6
	num_inference_steps: Annotated[int, Field(ge=0, le=2000)] = 200 #7

class ImageModelResponse(ModelResponse):
	size: ImageSize #6
	url: Annotated[str, HttpUrl] | None #8