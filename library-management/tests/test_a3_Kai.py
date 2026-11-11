from unittest.mock import patch

def test_checkout_sends_notification_successfully(client):
    with patch("app.routes.loans.send_notification") as mock_send: 

        mock_send.return_value = True  #return_value check the state is assrted to be True making it a stub
        
        payload1 = {
                "title": "The Hunger Games",
                "author": "Suzanne Collins",
                "isbn": "978-0123456789",
                "total_copies": 1, 
        }
        client.post("/books", json=payload1)  # add book
        
        payload2 = {
                "name": "Peter Hollander",
                "email": "hollander25@example.com",
        }
        client.post("/members", json=payload2)  # add member
        
        loan_payload = {
                "book_id": 1,
                "member_id": 1,
        }
        response = client.post("/loans", json=loan_payload)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["notified"] is True
        
        # Verify interaction: check recipient, subject, and message for mock assertion
        mock_send.assert_called_once_with(
            "hollander25@example.com", 
            "City Library Book Checkout Confirmation",  # Match your route's subject string format
            f"You have successfully checked out The Hunger Games. It is due on {data['due_date']}."
        )





