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

