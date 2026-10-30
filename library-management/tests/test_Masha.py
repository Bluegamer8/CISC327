def test_update_book_returns_updated_data(client):
    """Test updating a book returns the updated data."""
    # Create the book in the system.
    client.post("/books", json= {
        "title": "Cherry Grotter",
        "author": "JK. R",
        "isbn": "24999-000",
        "total_copies": 2,
     })

    # Update the book with new information.
    response = client.put("/books/1", json= {
        "title": "Cherry Grotter 2nd Edition",
        "author": "JK. R",
        "isbn": "24999-000",
        "total_copies": 4,  
     })

    # Check that the update response is correct.
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Cherry Grotter 2nd Edition"
    assert data["author"] == "JK. R"
    assert data["total_copies"] == 4
    assert data["id"] == 1

