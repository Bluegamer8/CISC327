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






