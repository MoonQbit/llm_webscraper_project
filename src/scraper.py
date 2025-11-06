import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger

def extract_urls(text: str) -> list[str]:
	url_pattern = r"(?P<url>https?:\/\/[^\s]+)" #1
	urls = re.findall(url_pattern, text) #2
	return urls

"""
# 1 A simple regex pattern that captures the URLs into a named group called url
and matches both http and https protocols. For simplicity, this pattern matches
more loosely defined URLs and doesn’t validate the structure of a domain name or
path, nor does it account for query strings or anchors in a URL.
"""

"""# 2 Find all nonoverlapping matches of the regex pattern in the text."""

def parse_inner_text(html_string: str) -> str:
	soup = BeautifulSoup(html_string, "lxml")
	if content := soup.find("div", id="bodyContent"): #3
		return content.get_text()
	logger.warning('Could not parse the HTML content')
	return ''

"""
# 3 Use the bs4 Beautiful Soup package to parse the HTML string. In Wikipedia
pages, the article content is nested within a div container with the
id="bodyContent", so the parsing logic assumes only Wikipedia URLs will be
passed in. You can change this logic for other URLs or just use soup.getText()
to grab any text content nested within the HTML. However, bear in mind that
there will be lots of noise in the parsed content if you parse the raw HTML
like that, which can confuse the LLM.
"""

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
	async with session.get(url) as response: #4
		html_string = await response.text()
		return parse_inner_text(html_string)

"""
# 4 Given an aiohttp session and a URL, perform an asynchronous get request.
Create a response async context manager and await the response within this
context manager.
"""

async def fetch_all(urls: list[str]) -> str:
	async with aiohttp.ClientSession() as session: #5
		results = await asyncio.gather(
			*[fetch(session, url) for url in urls], return_exceptions=True	
		)
	success_results = [result for result in results if isinstance(result, str)]
	if len(results) != len(success_results): #6
		logger.warning("Some URLs could not be fetched")
	return " ".join(success_results)

"""
#5 Given a list of URLs, create a client session async context manager to
asynchronously perform multiple fetch calls. Since fetch() is a coroutine
function (i.e., it uses the await keyword), fetch_all() will need to run
multiple fetch() coroutines inside the asyncio.gather() to be scheduled for
asynchronous execution on the event loop.

#6 Check that all URLs have been fetched successfully and, if not, raise a
warning.
"""