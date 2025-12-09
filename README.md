# MCP-Book-Project

Deploy a Database with books, create an API for that Database, then use an MCP server to access that data.

This repository contains an MCP server (using the [`mcp[cli]`](https://pypi.org/project/mcp/) Python package) that calls a separate Books API defined by this OpenAPI spec:

- <https://booksapi-webapp.azurewebsites.net/openapi.json>

The server exposes two tools:

- `get_books_by_author` → calls `GET /author/{author_name}`
- `get_books_by_title` → calls `GET /books/{book_name}`

Both tools support an optional `publish_by_date` query parameter.

## Requirements

- Python **3.13** or newer
- `pip` or `uv`

## Installation

From the root of this repository, install the project in your current environment: `pip install .`

This will install:

- The `mcp-book-project` package
- The console script `mcp-books-server`

If you prefer an editable/development install: `pip install -e .`

## Running the MCP server

### Direct CLI usage

You can run the server directly from the installed console script: `mcp-books-server`

This starts the MCP server over stdio, ready to be used by an MCP-compatible client.

### Using `mcp` CLI (if you want to register it as a server)

If you are using the `mcp` CLI, you can configure it to use this server.

First, ensure the package is installed (as above), then add a server entry to your MCP client configuration pointing to the `mcp-books-server` command.

A typical invocation (from a client that supports MCP) will look like: `mcp run mcp-books-server` (Exact commands depend on your MCP client; consult that client’s documentation.)

## Tools exposed

Once the server is running, your MCP client will see two tools:

### `get_books_by_author`

- **Description:** Search for books by author name (partial match).
- **Parameters:**
  - `author_name` (string, required) – Author name or partial name.
  - `publish_by_date` (string, optional) – Filter by publish date (e.g. `YYYY-MM-DD`).

### `get_books_by_title`

- **Description:** search for books by book title (partial match).
- **Parameters:**
  - `book_name` (string, required) – Book title or partial title.
  - `publish_by_date` (string, optional) – Filter by publish date (e.g. `YYYY-MM-DD`).

Both tools return a JSON array of book objects as defined by the Books API.

## Development

To set up a development environment:

```
uv venv
source .venv/bin/activate
pip install -e .
```

You can then run the server with: `mcp-books-server`
