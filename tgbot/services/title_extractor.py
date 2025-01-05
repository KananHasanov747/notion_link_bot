import asyncio
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()


def fetch_html(url):
    response = http.request("GET", url)
    if response.status == 200:
        # Extract charset from 'content-type' header, default to 'utf-8'
        content_type = response.headers.get("content-type", "text/html; charset=utf-8")
        charset = "utf-8"  # Default charset
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
        return response.data.decode(charset)
    return None


def extract_title(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    # Check for Open Graph title
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"]
    # Fallback to the <title> tag
    return soup.title.string if soup.title else "No title found"


async def fetch_and_extract_title(url):
    loop = asyncio.get_event_loop()
    html_content = await loop.run_in_executor(None, fetch_html, url)
    if html_content:
        return extract_title(html_content)
    return None
