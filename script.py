import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs, urlencode
import typer
import json
import time

# Initialize a Typer application; Typer is a library for building CLI applications.
app = typer.Typer()

# Function to validate each URL entered as input
def validate_url(ctx, param, value):
    urls = value
    for url in urls:
        parsed = urlparse(url)
        # Check if the URL has a scheme (http, https) and a network location (domain)
        if not parsed.scheme:
            raise typer.BadParameter(f"Invalid URL: {url}")
    return urls

# Asynchronous function to fetch the HTML content of a URL
async def fetch(session, url):
    try:
        # Asynchronously request the URL and wait for the response
        async with session.get(url) as response:
            response.raise_for_status()  # Will raise an exception for 4XX/5XX errors
            html = await response.text()  # Get the text content of the page
            return html, None
    except aiohttp.ClientError as e:
        return None, e
    except Exception as e:
        return None, e

# Asynchronous function to extract links from the fetched HTML content
async def extract_links(session, url):
    html, error = await fetch(session, url)
    if error:
        return url, error, set()

    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML
    links = set()

    # Iterate over all 'a' tags with an href attribute
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Ensure the link is absolute; if not, make it absolute by joining with the base URL
        if not href.startswith(('http:', 'https:')):
            href = urljoin(url, href)
        links.add(href)

    return url, None, links

# Main command function that processes URLs to fetch links
@app.command()
def main(
    urls: list[str] = typer.Option(..., "-u", "--url", help="URLs to fetch links from", callback=validate_url),
    output: str = typer.Option("stdout", "-o", "--output", help="Output format"),
    sleep_forever: bool = typer.Option(False, "-s","--sleep-forever", help="Sleep forever after scraping")
):
    asyncio.run(handle_main(urls, output, sleep_forever))  # Run the asynchronous main handler

# Asynchronous main handler that orchestrates fetching links from multiple URLs
async def handle_main(urls, output, sleep_forever):
    all_links = {}
    async with aiohttp.ClientSession() as session:
        tasks = [extract_links(session, u) for u in urls]
        results = await asyncio.gather(*tasks)  # Run all tasks concurrently

        for u, error, links in results:
            if error:
                typer.echo(f"Error fetching {u}: {error}", err=True)
                continue

            if output == 'json':
                # Process each link extracted
                for link in links:
                    parsed_link = urlparse(link)
                    base_url = f"{parsed_link.scheme}://{parsed_link.netloc}"
                    if base_url not in all_links:
                        all_links[base_url] = []
                    # Append only the path and query to the list of links
                    path_with_query = parsed_link.path
                    if parsed_link.query:
                        path_with_query += '?' + parsed_link.query
                    all_links[base_url].append(path_with_query)
            else:
                for link in links:
                    typer.echo(link)

    if output == 'json':
        typer.echo(json.dumps(all_links, indent=2))

    if sleep_forever:
        while True:
            time.sleep(60)  # Keep the program running/sleeping indefinitely

# Entry point check
if __name__ == "__main__":
    app()
