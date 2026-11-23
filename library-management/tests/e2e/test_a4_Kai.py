import os
import time
from playwright.sync_api import Page, expect

BASE_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")


def test_create_book_success(page: Page):
    suffix = str(int(time.time()))# make a unique title on multiple runs
    book_title = "Hunger Games"
    isbn = "978" + suffix[-10:]

    # go to the books page
    page.goto(BASE_URL + "/ui/books")

    # fill out the form fields
    page.get_by_role("textbox", name="Title").fill(book_title)# add title
    page.get_by_role("textbox", name="Author").fill("Suzanne Collins")#add autheor

    page.get_by_role("textbox", name="Genre").fill("Dystopian")#add dystopian

    page.get_by_role("textbox", name="ISBN").fill(isbn)# add isbn

    page.get_by_role("spinbutton", name="Total Copies").fill("1") # add copies

    page.get_by_role("button", name="Add Book").click() # click the Add Book button

    expect(page.get_by_text(book_title).first).to_be_visible()# check that the book shows up in the table

    page.reload()# refresh the page 

    expect(page.get_by_text(book_title).first).to_be_visible()# check that the book shows up in the table


def test_create_loan_invalid_book_id(page: Page):
    suffix = str(int(time.time()))#makes test random over multiple runs
    invalid_book_id = "999999"#an invalid value(could be valid if test run enough)

    # create a member first so a valid member ID exists
    member_response = page.request.post(
        BASE_URL + "/members",
        data={
            "name": f"Member{ suffix}",
            "email": f"member_{suffix}@example.com",
        },
    )
    assert member_response.status == 201  # create_member returns 201 on creation
    member_id = str(member_response.json()["id"]) #gets the member id for the member

    # go to the loans page
    page.goto(BASE_URL + "/ui/loans")

    # fill out the loan form with a non-existent book ID and the new member ID
    page.get_by_role("spinbutton", name="Book ID").fill(invalid_book_id)
    page.get_by_role("spinbutton", name="Member ID").fill(member_id)

    # submit the form
    page.get_by_role("button", name="Check Out").click()

    expect(page.get_by_text(invalid_book_id).first).not_to_be_visible()  # check that the loan does not show up in the table

    # reload and confirm the failed loan was not added to the loans table
    page.reload()

    expect(page.get_by_role("cell", name=invalid_book_id)).not_to_be_visible() # check that the loan does not show up in the table
