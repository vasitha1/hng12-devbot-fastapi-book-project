from tests import client
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_addition():
    assert 1 + 1 == 2

def test_get_all_books():
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_single_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"


def test_create_book():
    new_book = {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy",
    }
    response = client.post("/books/", json=new_book)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["title"] == "Harry Potter and the Sorcerer's Stone"


def test_update_book():
    updated_book = {
        "id": 1,
        "title": "The Hobbit: An Unexpected Journey",
        "author": "J.R.R. Tolkien",
        "publication_year": 1937,
        "genre": "Fantasy",
    }
    response = client.put("/books/1", json=updated_book)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit: An Unexpected Journey"


def test_delete_book():
    response = client.delete("/books/3")
    assert response.status_code == 204

    response = client.get("/books/3")
    assert response.status_code == 404


def test_get_book_success():
    """Test successfully getting a book by ID"""
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"
    assert data["publication_year"] == 1937
    assert data["genre"] == "SCI_FI"

def test_get_book_not_found():
    """Test getting a non-existent book"""
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_get_book_invalid_id():
    """Test getting a book with invalid ID type"""
    response = client.get("/books/invalid")
    assert response.status_code == 422  # FastAPI validation error for invalid type

@pytest.mark.parametrize(
    "book_id,expected_data", [
        (1, {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "publication_year": 1937,
            "genre": "SCI_FI"
        }),
        (2, {
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "publication_year": 1954,
            "genre": "FANTASY"
        })
    ]
)
def test_get_book_returns_correct_data(book_id, expected_data):
    """Parametrized test to verify correct book data is returned"""
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    for key, value in expected_data.items():
        assert data[key] == value

