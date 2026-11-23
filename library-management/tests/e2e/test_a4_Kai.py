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

