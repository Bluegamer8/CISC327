def test_update_book_returns_updated_data(client):
    """Test updating a book returns the updated data."""
    # create book
    client.post("/books", json= {
        "title": "Cherry Grotter",
        "author": "JK. R",
        "genre": "Horror",
        "isbn": "24999-000",
        "total_copies": 2,
     })

    # Update the book with new information.
    response = client.put("/books/1", json= {
        "title": "Cherry Grotter 2nd Edition",
        "author": "JK. R",
        "genre": "Fantasy",
        "isbn": "24999-000",
        "total_copies": 4,  
     })

    # Check that the update response is correct.
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Cherry Grotter 2nd Edition"
    assert data["author"] == "JK. R"
    assert data["genre"] == "Fantasy"
    assert data["total_copies"] == 4
    assert data["id"] == 1

def test_delete_book_removes_from_library(client):
    """Test deleting a book removes it from the library."""
    # Create the book in the system.
    client.post("/books", json= {
        "title": "Cherry Grotter",
        "author": "JK. R",
        "genre": "Fantasy",
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


def test_look_up_loans_return_list(client):
    """Test looking up loans returns a list."""
    # Create a book and a member, then create a loan.
    client.post("/books", json={
        "title": "Hamlet", "author": "Jane Doe", "genre": "Horror", "isbn": "12345", "total_copies": 2
    })
    client.post("/members", json={
        "name": "Bob",
        "email": "bob@email.com"
    })
    client.post("/loans", json={"book_id": 1, "member_id": 1})

    # Get the list of loans from the system.
    response = client.get("/loans")

    # Check that the loans list is correct.
    assert response.status_code == 200
    loans = response.get_json()
    assert isinstance(loans, list)
    assert len(loans) == 1
    assert loans[0]["book_id"] == 1
    assert loans[0]["member_id"] == 1



def test_return_loaned_book_updates_status_copies(client):
    """Test returning a loaned book updates its status copies."""
    # Create a book and a member, then create a loan.
    client.post("/books", json={
        "title": "Little Women", "author": "Jane", "genre": "Horror", "isbn": "102030", "total_copies": 1
    })
    client.post("/members", json={
        "name": "Bob",
        "email": "bob@email.com"
    })
    client.post("/loans", json={"book_id": 1, "member_id": 1})

    # Check that available copies decreased.
    book_check = client.get("/books/1")
    assert book_check.get_json()["available_copies"] == 0

    # Return the loaned book back to the library.
    response = client.put("/loans/1/return")
    assert response.status_code == 200

    # Check that available copies increased back.
    book_after_return = client.get("/books/1")
    assert book_after_return.get_json()["available_copies"] == 1


def test_update_nonexistant_value(client):
    """ Test ensuring updating a nonexistant value returns 404 """
    response = client.put("/books/1", json= {
        "title": "Cherry Grotter 2nd Edition",
        "author": "JK. R",
        "genre": "Fantasy",
        "isbn": "24999-000",
        "total_copies": 4,  
     })

    assert response.status_code == 404
