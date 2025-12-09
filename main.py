import asyncio
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP, Context

BOOKS_API_BASE_URL = "https://booksapi-webapp.azurewebsites.net"

app = FastMCP("books-api-server")


async def fetch_books_by_author(
    author_name: str, publish_by_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {}
    if publish_by_date is not None:
        params["publish_by_date"] = publish_by_date

    async with httpx.AsyncClient(base_url=BOOKS_API_BASE_URL, timeout=30.0) as client:
        resp = await client.get(f"/author/{author_name}", params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_books_by_title(
    book_name: str, publish_by_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {}
    if publish_by_date is not None:
        params["publish_by_date"] = publish_by_date

    async with httpx.AsyncClient(base_url=BOOKS_API_BASE_URL, timeout=30.0) as client:
        resp = await client.get(f"/books/{book_name}", params=params)
        resp.raise_for_status()
        return resp.json()


@app.tool(
    name="get_books_by_author",
    description=(
        "Search for books by author name. "
        "The author_name is treated as a partial match pattern. "
        "Optionally filter by publish_by_date (YYYY-MM-DD)."
    ),
)
async def get_books_by_author(
    ctx: Context,
    author_name: str,
    publish_by_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for books by author name.

    Args:
        ctx: FastMCP context (unused, but required by FastMCP).
        author_name: Author name (partial match allowed).
        publish_by_date: Optional publish-by date filter in YYYY-MM-DD format.

    Returns:
        A list of book objects from the Books API.
    """
    author_name = author_name.strip()
    if not author_name:
        raise ValueError("author_name is required")

    return await fetch_books_by_author(author_name, publish_by_date)


@app.tool(
    name="get_books_by_title",
    description=(
        "Search for books by book title. "
        "The book_name is treated as a partial match pattern. "
        "Optionally filter by publish_by_date (YYYY-MM-DD)."
    ),
)
async def get_books_by_title(
    ctx: Context,
    book_name: str,
    publish_by_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for books by book title.

    Args:
        ctx: FastMCP context (unused, but required by FastMCP).
        book_name: Book title (partial match allowed).
        publish_by_date: Optional publish-by date filter in YYYY-MM-DD format.

    Returns:
        A list of book objects from the Books API.
    """
    book_name = book_name.strip()
    if not book_name:
        raise ValueError("book_name is required")

    return await fetch_books_by_title(book_name, publish_by_date)


def main() -> None:
    """
    Entry point for running the MCP server over stdio using FastMCP.
    """
    asyncio.run(app.run_stdio())


if __name__ == "__main__":
    app.run(transport="stdio")
