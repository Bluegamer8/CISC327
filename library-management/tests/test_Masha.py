def test_delete_book_removes_from_library(client):

    """Test deleting a book removes it from the library."""

    # Create the book in the system.

    client.post("/books", json= {

        "title": "Cherry Grotter",

        "author": "JK. R",

        "isbn": "24999-000",

        "total_copies": 2,
     })

    # Delete the book by its ID.

    response = client.delete("/books/1")
    assert response.status_code in [200, 204]

    # Check that the book can no longer be found.

    get_response = client.get("/books/1")
    assert get_response.status_code == 404



def test_update_member_returns_updated_data(client):

    """Test updating a member returns the updated data."""

    # Create the member in the system.

    response1 = client.post("/members", json={

        "name": "Jeff M",

        "email": "jeff@email.com"

    })

    assert response1.status_code == 201

    member = response1.get_json()

    member_id = member["id"]



    # Update the member with new information.

    response = client.put(f"/members/{member_id}", json={ 

        "name": "Jeffery John",   

        "email": "j.john@email.com"

    })

    # Check that the update response is correct.

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Jeffery John"

    assert data["email"] == "j.john@email.com"


