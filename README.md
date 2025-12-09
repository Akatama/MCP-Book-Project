# MCP-Book-Project

Deploy a Database with books, create an API for that Database, then use an MCP server to access that data.

This repository contains an MCP server (using the [`mcp[cli]`](https://pypi.org/project/mcp/) Python package) that calls a separate Books API defined by this OpenAPI spec:

- https://booksapi-webapp.azurewebsites.net/openapi.json

The server exposes two tools:

- `get_books_by_author` → calls `GET /author/{author_name}`
- `get_books_by_title` → calls `GET /books/{book_name}`

Both tools support an optional `publish_by_date` query parameter.

## Requirements

- Python **3.13** or newer
- `pip` (or another PEP 517–compatible installer)

## Installation

From the root of this repository, install the project in your current environment:

