import asyncio
from typing import Any, Dict, List, Optional

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ErrorData,
    ListToolsResult,
    TextContent,
    Tool,
)


BOOKS_API_BASE_URL = "https://booksapi-webapp.azurewebsites.net"


server = Server("books-api-server")


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


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """
    Expose the Books API operations as MCP tools.
    """
    return ListToolsResult(
        tools=[
            Tool(
                name="get_books_by_author",
                description=(
                    "Search for books by author name. "
                    "The author_name is treated as a partial match pattern. "
                    "Optionally filter by publish_by_date (YYYY-MM-DD)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "author_name": {
                            "type": "string",
                            "description": "Author name (partial match allowed).",
                        },
                        "publish_by_date": {
                            "type": ["string", "null"],
                            "description": (
                                "Optional publish-by date filter in YYYY-MM-DD format."
                            ),
                        },
                    },
                    "required": ["author_name"],
                },
            ),
            Tool(
                name="get_books_by_title",
                description=(
                    "Search for books by book title. "
                    "The book_name is treated as a partial match pattern. "
                    "Optionally filter by publish_by_date (YYYY-MM-DD)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "book_name": {
                            "type": "string",
                            "description": "Book title (partial match allowed).",
                        },
                        "publish_by_date": {
                            "type": ["string", "null"],
                            "description": (
                                "Optional publish-by date filter in YYYY-MM-DD format."
                            ),
                        },
                    },
                    "required": ["book_name"],
                },
            ),
        ]
    )


@server.call_tool()
async def call_tool(request: CallToolRequest) -> CallToolResult:
    """
    Handle tool invocations from the MCP client.
    """
    name = request.name
    args = request.arguments or {}

    try:
        if name == "get_books_by_author":
            author_name = str(args.get("author_name", "")).strip()
            if not author_name:
                raise ValueError("author_name is required")

            publish_by_date = args.get("publish_by_date")
            books = await fetch_books_by_author(author_name, publish_by_date)

            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=httpx.dumps(books, indent=2)  # type: ignore[attr-defined]
                        if hasattr(httpx, "dumps")
                        else str(books),
                    )
                ]
            )

        if name == "get_books_by_title":
            book_name = str(args.get("book_name", "")).strip()
            if not book_name:
                raise ValueError("book_name is required")

            publish_by_date = args.get("publish_by_date")
            books = await fetch_books_by_title(book_name, publish_by_date)

            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=httpx.dumps(books, indent=2)  # type: ignore[attr-defined]
                        if hasattr(httpx, "dumps")
                        else str(books),
                    )
                ]
            )

        return CallToolResult(
            error=ErrorData(
                code="tool_not_found",
                message=f"Unknown tool: {name}",
            )
        )

    except httpx.HTTPStatusError as e:
        return CallToolResult(
            error=ErrorData(
                code="http_error",
                message=f"HTTP error while calling Books API: {e.response.status_code} {e.response.text}",
            )
        )
    except Exception as e:
        return CallToolResult(
            error=ErrorData(
                code="internal_error",
                message=f"Unexpected error while calling tool {name}: {e}",
            )
        )


async def run() -> None:
    """
    Entry point for running the MCP server over stdio.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
