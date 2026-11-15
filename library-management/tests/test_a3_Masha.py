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
        client.post("/members", json=payload2)  # add member
        
        loan_payload = {
            "book_id": 1,
            "member_id": 1,
        }
        response = client.post("/loans", json=loan_payload)  

        assert response.status_code == 400  # checking checkout failed
        mock_send.assert_not_called()  # verifying no notification was sent

