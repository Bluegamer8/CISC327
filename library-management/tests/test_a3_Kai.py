from unittest.mock import patch

def test_checkout_handles_notification_stub_success(client):
    """
    The stub makes sure the application handles a successful notification correctly
    """
    with patch("app.routes.loans.send_notification") as mock_send: 
        
        mock_send.return_value = True #setting the stub to a success 
        payload1 = {
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "isbn": "978-0123456789",
            "total_copies": 1, 
        }
        client.post("/books", json=payload1)# adda book
        
        payload2 = {
            "name": "Peter Hollander",
            "email": "hollander25@example.com",
        }
        client.post("/members", json=payload2)#adda mamber
        
        loan_payload = {
            "book_id": 1,
            "member_id": 1,
        }
        response = client.post("/loans", json=loan_payload)#add a loan
        
        assert response.status_code == 201#veryifying creation
        data = response.get_json()
        assert data["notified"] is True#verifying success


def test_checkout_sends_notification_mock_success(client):
    """
    The mock makes sure that the notification has the correct content when sent
    """
    with patch("app.routes.loans.send_notification") as mock_send: 
        mock_send.return_value = True  #setting the mock to a success 
        
        payload1 = {
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "isbn": "978-0123456789",
            "total_copies": 1, 
        }
        client.post("/books", json=payload1)#add book
        
        payload2 = {
            "name": "Peter Hollander",
            "email": "hollander25@example.com",
        }
        client.post("/members", json=payload2)#add member
        
        loan_payload = {
            "book_id": 1,
            "member_id": 1,
        }
        response = client.post("/loans", json=loan_payload)#add loan

        assert response.status_code == 201#veryifying creation
        data = response.get_json()
        assert data["notified"] is True#verifying success
        # make sure the notification has the right conntent
        mock_send.assert_called_once_with(
            "hollander25@example.com", 
            "City Library Book Checkout Confirmation", 
            f"You have successfully checked out The Hunger Games. It is due on {data['due_date']}."
        )

# _____Testing For Step 3 of assignment 3_____________________________________________________________________

#Reservation.py testing
def test_reservations_created(client):
        """A member POSTed to /reservations is returned with correct id book and and member.
        Testing to make sure the reservation is created properly and makes in the system
        """

        payload1 = {
                "title": "The Hunger Games",
                "author": "Suzanne Collins",
                "isbn": "978-0123456789",
                "total_copies": 1,
        }
        client.post("/books", json=payload1)#add book

        payload2 = {
                "name": "Peter Hollander",
                "email": "hollander25@example.com",
        }
        client.post("/members", json=payload2)#add memeber

        res_payload = {
                "book_id": 1,
                "member_id": 1,
        }
        responce = client.post("/reservations", json=res_payload)#add reservation
        assert responce.status_code == 201#make sure reservation is made
        
        
        #checking for correct reservation
        res_data = responce.get_json()
        assert res_data["book_id"] == 1
        assert res_data["member_id"] == 1
        assert res_data["id"] == 1
        assert res_data["fulfilled"] == False

def test_reservations_search_by_book_id(client):
    """Testing to make sure filtering reservations by book_id works properly in the system.
    """
    payload_book1 = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 2,
    }
    client.post("/books", json=payload_book1)  # add book 1

    payload_book2 = {
        "title": "Catching Fire",
        "author": "Suzanne Collins",
        "isbn": "978-0987654321",
        "total_copies": 2,
    }
    client.post("/books", json=payload_book2)  # add book 2

    payload_member = {
        "name": "Peter Hollander",
        "email": "hollander25@example.com",
    }
    client.post("/members", json=payload_member)  # add member

    res_payload1 = {
        "book_id": 1,
        "member_id": 1,
    }
    client.post("/reservations", json=res_payload1)  # add reservation 1

    res_payload2 = {
        "book_id": 2,
        "member_id": 1,
    }
    client.post("/reservations", json=res_payload2)  # add reservation 2

    # checking filter by book_id
    response = client.get("/reservations?book_id=1")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) ==  1
    assert data[0]["id"] == 1
    assert data[0]["book_id"] == 1
    assert data[0]["member_id"] == 1
    assert data[0]["fulfilled"] is False


def test_reservations_search_by_member_id(client):
    """Testing to make sure filtering reservations by member_id works properly in the system.
    """
    payload_book = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 2,
    }
    client.post("/books", json=payload_book)  # add book

    payload_member1 = {
        "name": "Peter Hollander",
        "email": "hollander25@example.com",
    }
    client.post("/members", json=payload_member1)  # add member 1

    payload_member2 = {
        "name": "Sarah Connor",
        "email": "connor@example.com",
    }
    client.post("/members", json=payload_member2)  # add member 2

    res_payload1 = {
        "book_id": 1,
        "member_id": 1,
    }
    client.post("/reservations", json=res_payload1)  # add reservation 1

    res_payload2 = {
        "book_id": 1,
        "member_id": 2,
    }
    client.post("/reservations", json=res_payload2)  # add reservation 2

    # checking filter by member_id
    response = client.get("/reservations?member_id=2")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) ==  1
    assert data[0]["id"] == 2
    assert data[0]["book_id"] == 1
    assert data[0]["member_id"] == 2
    assert data[0]["fulfilled"] is False

def test_reservation_no_book(client):
    """Tests a failure for reservation in case when book doesn't exist 
    """
    member_payload = {
            "name": "Peter Hollander",
            "email": "hollander25@example.com",
    }
    client.post("/members", json=member_payload)#add memeber

    res_payload = {
            "book_id": 1,
            "member_id": 1,
    }
    responce = client.post("/reservations", json=res_payload)#add reservation
    assert responce.status_code == 404#make sure it fails

def test_reservation_no_member(client):
    """Tests a failure for reservation in case when member doesn't exist 
    """
    payload1 = {
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "isbn": "978-0123456789",
            "total_copies": 1,
    }
    client.post("/books", json=payload1)#add book
   
    res_payload = {
            "book_id": 1,
            "member_id": 1,
    }
    responce = client.post("/reservations", json=res_payload)#add reservation
    assert responce.status_code == 404#make sure it fails

#Loans Testing
def test_renew_loan(client):
        """renew successfully extends the due date of an active loan."""
        payload1 = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 1,
        }
        client.post("/books", json=payload1)#add book

        payload2 = {
                "name": "Peter Hollander",
                "email": "hollander25@example.com",
        }
        client.post("/members", json=payload2)#add memeber

        loan_payload = {
                "book_id": 1,
                "member_id": 1,
        }
        loan = client.post("/loans", json=loan_payload)#add loan
        initial_due_date = loan.get_json()["due_date"]

        # Renew the loan
        response = client.put("/loans/1/renew")
        assert response.status_code == 200
        
        new_due_date = response.get_json()["due_date"]
        assert new_due_date != initial_due_date #make sure new due date is note same as old

def test_get_fine(client):
        """Gets the fines and calculates and returns the fine amount for a loan."""
        payload1 = {
                "title": "The Hunger Games",
                "author": "Suzanne Collins",
                "isbn": "978-0123456789",
                "total_copies": 1,
        }
        client.post("/books", json=payload1)#add book

        payload2 = {
                "name": "Peter Hollander",
                "email": "hollander25@example.com",
        }
        client.post("/members", json=payload2)#add memeber

        loan_payload = {
                "book_id": 1,
                "member_id": 1,
        }
        client.post("/loans", json=loan_payload)#add loan
        response = client.get("/loans/1/fine")
        assert response.status_code == 200

        data = response.get_json()
        assert data["loan_id"] == 1
        assert isinstance(data["fine_amount"], float)

def test_check_out_book_with_no_book(client):
    """try to check out but with no existing book
    """
    payload1 = {
        "name": "Peter Hollander",
        "email": "hollander25@example.com",
    }
    client.post("/members", json=payload1)#add memeber

    loan_payload = {
        "book_id": 1,
        "member_id": 1,
    }
    loan = client.post("/loans", json=loan_payload)#add loan
    assert loan.status_code == 404 #asserting that there was an error when attemping to make loan

def test_renew_loan_with_no_loan(client):
        """trys to renew a loan despite the fact the loan does not exist"""
        
        # Renew the loan
        response = client.put("/loans/1/renew")
        assert response.status_code == 404 # fails cause loan was never created

def test_get_fine_with_no_loan(client):
      """
        Attemptign to get the fine from a lone that does not exist
      """
      response = client.get("/loans/1/fine")
      assert response.status_code == 404 #fails since loan 1 doesn't exist


#book testing
def test_change_book_post_redirect(client):
    """ Makes sure the system updates the book and redirects."""
    payload = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 1,
    }
    client.post("/books", json=payload)#add book
    
    payload2 = {
        "title": "The Hunger Games 10th Edition",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 7,
    }
   
    response = client.post("/books/1", data=payload2) 
    
    assert response.status_code == 302 #testing for a redirect

    #check that changes are saved properly
    updated = client.get("/books/1").get_json()
    assert updated["title"] == "The Hunger Games 10th Edition"
    assert updated["total_copies"] == 7

def test_list_books_with_search(client):
        """Testing to make sure able to filer out books by search
            """
        payload_book1 = {    
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "isbn": "978-0123456789",
            "total_copies": 2,
        }
        client.post("/books", json=payload_book1)  # add book 1
    
        payload_book2 = {
            "title": "Catching Fire",
            "author": "Suzanne Collins",
            "isbn": "978-0987654321",
            "total_copies": 2,
        }
        client.post("/books", json=payload_book2)  # add book 2
        response = client.get("/books?search=The Hunger Games")
        assert response.status_code == 200
        data = response.get_json()

        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["title"] == "The Hunger Games"
        assert data[0]["author"] == "Suzanne Collins"
        assert data[0]["isbn"] == "978-0123456789"
        assert data[0]["total_copies"] == 2
        assert data[0]["available_copies"] == 2
