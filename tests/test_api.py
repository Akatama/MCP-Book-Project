import asyncio
import pytest
import httpx

# from main import (
#     BOOKS_API_BASE_URL,
#     fetch_books_by_author,
#     fetch_books_by_title,
# )
from typing import Any, Dict
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "author_name", ["Jane Austen", "Kurt Vonnegut", "Douglas Adams"]
)
async def test_get_books_by_author(author_name):
    """Call the Get Books By Author API and verify the result from the MCP server function"""
    params: Dict[str, Any] = {}
    expected_result = ""

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/author/{author_name}", params=params)
        resp.raise_for_status()
        expected_result = resp.json()

    actual_result = await main.fetch_books_by_author(author_name)

    assert expected_result == actual_result


@pytest.mark.asyncio
@pytest.mark.parametrize("author_name", ["123", "{}", "~"])
async def test_get_books_by_author_with_invalid_author_name(author_name):
    """Call the Get Books By Author API with an invalid author name"""
    params: Dict[str, Any] = {}
    expected_result = ""
    expected_status = 0

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/author/{author_name}", params=params)
        expected_result = resp.json()
        expected_status = resp.status_code

    assert expected_status == 200
    actual_result = await main.fetch_books_by_author(author_name)

    assert expected_result == actual_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "author_name,publish_by_date",
    [
        ("Jane Austen", "2000-01-01"),
        ("Kurt Vonnegut", "1990-06-21"),
        ("Douglas Adams", "2004-03-15"),
    ],
)
async def test_get_books_by_author_with_publish_by_date(author_name, publish_by_date):
    """Call the Get Books By Author API with a publish by date and verify the result from the MCP server function"""
    params: Dict[str, Any] = {}
    headers = {"user_agent": "test"}
    data = {"integer": 123, "boolean": True, "list": ["a", "b", "c"]}
    params["publish_by_date"] = publish_by_date
    expected_result = ""

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0, headers=headers
    ) as client:
        resp = await client.get(f"/author/{author_name}", params=params)
        resp = await client.post(f"/author/{author_name}", params=params, json=data)
        resp.raise_for_status()
        expected_result = resp.json()

    actual_result = await main.fetch_books_by_author(author_name, publish_by_date)

    assert expected_result == actual_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "author_name,publish_by_date",
    [
        ("Jane Austen", "2000"),
        ("Kurt Vonnegut", "06-21"),
        ("Douglas Adams", "03"),
    ],
)
async def test_get_books_by_author_with_invalid_publish_by_date(
    author_name, publish_by_date
):
    """Call the Get Books By Author API with invalid publish by date"""
    params: Dict[str, Any] = {}
    params["publish_by_date"] = publish_by_date
    expected_result = ""
    expected_status = 0

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/author/{author_name}", params=params)
        expected_status = resp.status_code
        expected_result = resp.json()

    assert expected_status == 500
    assert expected_result == {"detail": "Error querying database using search_author"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_title",
    ["Hitchhikers", "Slaughterhouse", "Pride"],
)
async def test_get_books_by_title(book_title):
    """Call the Get Books by Title API and verify the result from the MCP server function"""
    params: Dict[str, Any] = {}
    expected_result = ""

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/books/{book_title}", params=params)
        resp.raise_for_status
        expected_result = resp.json()

    actual_result = await main.fetch_books_by_title(book_title)

    assert expected_result == actual_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_title",
    ["()", "123", "%"],
)
async def test_get_books_by_title_with_invalid_book_title(book_title):
    """Call the Get Books by Title API with an invalid book title"""
    params: Dict[str, Any] = {}
    expected_result = ""
    expected_status = 0

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/books/{book_title}", params=params)
        resp.raise_for_status
        expected_result = resp.json()
        expected_status = resp.status_code

    assert expected_status == 200
    actual_result = await main.fetch_books_by_title(book_title)

    assert expected_result == actual_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_title,publish_by_date",
    [
        ("Hitchhikers", "2000-01-01"),
        ("Slaughterhouse", "1980-10-15"),
        ("Pride", "2005-01-01"),
    ],
)
async def test_get_books_by_title_with_publish_by_date(book_title, publish_by_date):
    """Call the Get Books by Title API and verify the result from the MCP server function"""
    params: Dict[str, Any] = {}
    params["publish_by_date"] = publish_by_date
    expected_result = ""

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/books/{book_title}", params=params)
        resp.raise_for_status
        expected_result = resp.json()

    actual_result = await main.fetch_books_by_title(book_title, publish_by_date)

    assert expected_result == actual_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_title,publish_by_date",
    [
        ("Hitchhikers", "2000"),
        ("Slaughterhouse", "10-15"),
        ("Pride", "01"),
    ],
)
async def test_get_books_by_title_with_invalid_publish_by_date(
    book_title, publish_by_date
):
    """Call the Get Books by Title API with an invalid publish by date"""
    params: Dict[str, Any] = {}
    params["publish_by_date"] = publish_by_date
    expected_result = ""
    expected_status = 0

    async with httpx.AsyncClient(
        base_url=main.BOOKS_API_BASE_URL, timeout=30.0
    ) as client:
        resp = await client.get(f"/books/{book_title}", params=params)
        expected_status = resp.status_code
        expected_result = resp.json()

    assert expected_status == 500
    assert expected_result == {"detail": "Error querying database using search_books"}
