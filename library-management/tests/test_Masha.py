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



def test_delete_member_removes_from_store(client):

    """Test deleting a member removes them from the store."""

    # Create the member in the system.

    client.post("/members", json={

        "name": "Jane Doe",
        "email": "jane@example.com"
    })

    # Delete the member by their ID.

    response = client.delete("/members/1")

    assert response.status_code in [200, 204]

    # Check that the member can no longer be found.

    get_response = client.get("/members/1")

    assert get_response.status_code == 404


