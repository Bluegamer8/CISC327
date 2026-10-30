def test_get_all_books_returns_all_created_books(client):
    """GET /books returns a list containing all books that have been added.
        Testing to make sure 2 books added to book were correctly gotten
    """
    payload1 = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 1,
    }
    client.post("/books", json=payload1)#add book
    payload2 = {
        "title": "Lord of the Flies",
        "author": "William Golding",
        "isbn": "978-9876543210",
        "total_copies": 20,
    }
    client.post("/books", json=payload2)#add book 2

    response = client.get("/books") #add book get
    assert response.status_code == 200
    
    #Checking the output from get call
    books = response.get_json()
    assert isinstance(books, list)
    assert len(books) == 2
    assert books[0]["id"] == 1
    assert books[0]["title"] == "The Hunger Games"
    assert books[0]["author"] == "Suzanne Collins"
    assert books[0]["isbn"] == "978-0123456789"
    assert books[0]["total_copies"] == 1
    assert books[0]["available_copies"] == 1
    assert books[1]["id"] == 2
    assert books[1]["title"] == "Lord of the Flies"
    assert books[1]["author"] == "William Golding"
    assert books[1]["isbn"] == "978-9876543210"
    assert books[1]["total_copies"] == 20
    assert books[1]["available_copies"] == 20

def test_get_one_book_returns_correct_book(client):
    """GET /books/<id> returns the matching book with the ID by checking the title.
        Makes sure the id called returns expected book.
    """
    payload = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 1,
    }
    client.post("/books", json=payload) #add book


    #called with id 1 since it is first book
    response = client.get(f"/books/1")
    assert response.status_code == 200


    #checking to make sure correct book was gotten
    data = response.get_json()
    assert data["id"] == 1
    assert data["title"] == "The Hunger Games"

def test_get_all_members_returns_all_created_members(client):
    """GET /members returns a list containing all members that have been added.
        Testing to make sure 2 members added to memebers were correctly gotten
    """
    member1_payload = {
        "name": "Peter Hollander",
        "email": "hollander25@example.com",
    }
    client.post("/members", json=member1_payload)#add member
    member2_payload = {
        "name": "Jimmy John",
        "email": "jjohn@example.com",
    }
    client.post("/members", json=member2_payload)#add member


    #calls get
    response = client.get("/members")
    assert response.status_code == 200


    #checks to make sure all member match up correctly
    members = response.get_json()
    assert isinstance(members, list)
    assert len(members) == 2
    assert members[0]["id"] == 1
    assert members[0]["name"] == "Peter Hollander"
    assert members[0]["email"] == "hollander25@example.com"
    assert members[1]["id"] == 2
    assert members[1]["name"] == "Jimmy John"
    assert members[1]["email"] == "jjohn@example.com"

def test_create_member_returns_created_member(client):
    """A member POSTed to /members is returned with correct id and name.
        Testing to make sure member is created properly and makes in the system
    """
    payload = {
        "name": "Peter Hollander",
        "email": "hollander25@example.com",
    }


    response = client.post("/members", json=payload)#add member
    assert response.status_code == 201


    #checks to make sure the correct member was added
    data = response.get_json()
    assert data["name"] == "Peter Hollander"
    assert data["email"] == "hollander25@example.com"
    assert data["id"] == 1

def test_get_one_member_returns_correct_member(client):
    """GET /members/<id> returns the specific member matching the given ID.
        Test to make sure the member we get from id is the expected member
    """
    payload = {
        "name": "Peter Hollander",
        "email": "hollander25@example.com",
    }
    client.post("/members", json=payload)#add member


    response = client.get(f"/members/1") #get member
    assert response.status_code == 200


    #check that it's correct member
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Peter Hollander"

def test_check_out_book_creates_loan_and_decrements_copies(client):
    """POST /loans successfully checks out a book, creating a loan record and reducing available copies.
        Tests to make sure that a checked out book isproperly checked out by matching the member id, book id
        and the checkout id and laso checking the books availalbe copies
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

    loan_payload = {
        "book_id": 1,
        "member_id": 1,
    }
    loan = client.post("/loans", json=loan_payload)#add loan
    assert loan.status_code == 201


    #checking for correct loan
    loan_data = loan.get_json()
    assert loan_data["book_id"] == 1
    assert loan_data["member_id"] == 1
    assert loan_data["id"] == 1


    #checking book available copies amount
    book_after_return = client.get(f"/books/1")
    assert book_after_return.get_json()["available_copies"] == 0


def test_check_out_book_only_decrements_copies_when_available(client):
    """POST /loans successfully checks out a book, creating a loan record and reducing available copies.
        Tests to make sure that a checked out book is only deremeneted when there is copy available.
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

    loan_payload = {
        "book_id": 1,
        "member_id": 1,
    }
    loan = client.post("/loans", json=loan_payload)#add loan
    assert loan.status_code == 201

    loan = client.post("/loans", json=loan_payload)#add loan which should fail
    assert loan.status_code == 400

    #checking book available copies amount
    book_after_return = client.get(f"/books/1")
    assert book_after_return.get_json()["available_copies"] == 0

def test_check_out_book_where_starting_with_no_copies(client):
    """POST /loans successfully checks out a book, creating a loan record and reducing available copies.
        Tests to make sure that a checked out book is only deremeneted when there is copy available.
    """
    payload1 = {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "isbn": "978-0123456789",
        "total_copies": 0,
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
    assert loan.status_code == 400

    #checking book available copies amount
    book_after_return = client.get(f"/books/1")
    assert book_after_return.get_json()["available_copies"] == 0

