from unittest.mock import patch

def test_checkout_handles_notification_stub_failure(client):
    """
    The stub makes sure the application handles a failed notification correctly
    """
    with patch("app.routes.loans.send_notification") as mock_send: 
        
        mock_send.return_value = False  # Setting the stub to a failure 
        payload1 = {
            "title": "Harry Potter",
            "author": "JK R",
            "isbn": "1233-000",
            "total_copies": 1, 
        }
        client.post("/books", json=payload1)
        
        payload2 = {
            "name": "Peter Parker",
            "email": "parker99@example.com",
        }
        client.post("/members", json=payload2)
        
        loan_payload = {
            "book_id": 1,
            "member_id": 1,
        }
        response = client.post("/loans", json=loan_payload)

        assert response.status_code == 201  #checking creation
        data = response.get_json()
        assert data["notified"] is False  #verifying failure

def test_checkout_sends_no_notification_when_book_unavailable(client):
    """
    The mock makes sure that no notification is sent if the checkout fails
    """
    with patch("app.routes.loans.send_notification") as mock_send: 
        payload1 = {
            "title": "The Hunger Games",
            "author": "Jane Doe",
            "isbn": "44-9977",
            "total_copies": 0,  # 0 copies so checkout fails
        }
        client.post("/books", json=payload1)  
        
        payload2 = {
            "name": "Justin Bieber",
            "email": "bieber540@example.com",
        }
        client.post("/members", json=payload2)  # add memberfrom app.store import store
        
        loan_payload = {
            "book_id": 1,
            "member_id": 1,
        }
        response = client.post("/loans", json=loan_payload)  

        assert response.status_code == 400  # checking checkout failed
        mock_send.assert_not_called()  # verifying no notification was sent

def test_home_route(client):
    """
    Ensures the home route responds with a 200 status code 
    and successfully renders the home page.
    """
    response = client.get("/")
    
    assert response.status_code == 200


def test_books_page_get(client):
    """
    Ensures a GET request to the books page returns 200 OK 
    and successfully renders the template.
    """
    response = client.get("/ui/books")
    
    assert response.status_code == 200


def test_books_page_post_creates_book(client):
    """
    Ensures a POST request successfully creates a book
    and redirects back to the books page.
    """
    payload = {
        "title": "Little Prince",
        "author": "Jane Doe",
        "genre": "Fantasy",
        "isbn": "123-888",
        "total_copies": "3"
    }
    
    response = client.post("/ui/books", data=payload, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Little Prince" in response.data
    assert b"Jane Doe" in response.data

def test_delete_a_book(client):
    """
    Ensures a POST request to the delete route removes the book from the store 
    and redirects back to the books page.
    """

    form_data = {
        "title": "Book777",
        "author": "Jane Doe",
        "genre": "Romance",
        "isbn": "888044-3",
        "total_copies": "2"
    }
    client.post("/ui/books", data=form_data)
    
    response = client.post("/ui/books/1/delete", follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Book777" not in response.data


def test_delete_book_non_existent(client):
    """
    Ensures that trying to delete a book that doesn't exist handles 
    without throwing an error and redirects back to page
    """
    response = client.post("/ui/books/999/delete", follow_redirects=True)
    
    assert response.status_code == 200


def test_members_page(client):
    """
    Checks GET returns 200 OK and POST successfully creates a member 
    and redirects back to members page
    """

    response = client.get("/ui/members")
    assert response.status_code == 200

    # create member
    form_data = {
        "name": "Jane D",
        "email": "dd@gmail.com"
    }
    response = client.post("/ui/members", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Jane D" in response.data
    assert b"dd@gmail.com" in response.data


def test_delete_member_success(client):
    """
    Ensures posting to the delete route removes the member from the store.
    """
    # create member
    client.post("/ui/members", data={"name": "Bobby Smith", "email": "bobby@gmail.com"})
    
    # delete member
    response = client.post("/ui/members/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Bobby Smith" not in response.data


def test_loans_page(client):
    """
    Tests a successful loan creation returns an OK 200 status code
    """

    client.post("/ui/books", data={
        "title": "bookbook", "author": "jane", "genre": "none", "isbn": "123-667", "total_copies": "1"
    })
    
    client.post("/ui/members", data={"name": "Jennnie", "email": "jennie@gmail.com"})

    loan_data = {
        "book_id": "1",
        "member_id": "1"
    }
    response = client.post("/ui/loans", data=loan_data, follow_redirects=True)
    assert response.status_code == 200


def test_loans_page_post_no_available_copies_shows_error(client):
    """
    Tests that an attempt to check out a book with 0 available copies 
    prevents loan creation and displays the 'No available copies.' error message.
    """

    client.post("/ui/books", data={
        "title": "bookbook", "author": "jane", "genre": "none", "isbn": "123-667", "total_copies": "0"
    })

    client.post("/ui/members", data={"name": "Jennnie", "email": "jennie@gmail.com"})

    # Attempt to make a loan
    loan_data = {
        "book_id": "1",
        "member_id": "1"    
    }
   
    response = client.post("/ui/loans", data=loan_data)
    
    assert response.status_code == 200

    assert b"No availble copies." in response.data


def test_return_loan_page(client):
    """
    Tests that posting to the return route successfully updates
    and redirects back to the loans page
    """
    
    client.post("/ui/books", data={
        "title": "bookbook", "author": "jane", "genre": "none", "isbn": "123-667", "total_copies": "1"
    })
    
    client.post("/ui/members", data={"name": "Jennnie", "email": "jennie@gmail.com"})

    client.post("/ui/loans", data={"book_id": "1", "member_id": "1"})

    response = client.post("/ui/loans/1/return", follow_redirects=True)
    
    assert response.status_code == 200

#comment to test if CI integration was properly added to main