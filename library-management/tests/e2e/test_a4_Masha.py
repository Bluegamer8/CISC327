import os
import re
import time
from playwright.sync_api import Page, expect

BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000")


def test_add_valid_member(page: Page):
    
    page.goto(f"{BASE_URL}/")

   
    add_link = page.get_by_role("link", name="Add Member")
    if add_link.count() > 0:
        add_link.first.click()
    else:
        page.goto(f"{BASE_URL}/ui/members")

   
    member_name = "John Smith"
    member_email = "john@mail.com"

    page.get_by_label("Name").fill(member_name)
    page.get_by_label("Email").fill(member_email)

    
    page.get_by_role("button", name="Add Member").click()

    
    expect(page.locator("body")).to_contain_text(member_name)



def test_add_member_missing_required_info(page: Page):

    page.goto(f"{BASE_URL}/")
    
    add_link = page.get_by_role("link", name="Add Member")
    if add_link.count() > 0:
        add_link.first.click()
    else:
        page.goto(f"{BASE_URL}/ui/members")


    page.get_by_label("Email").fill("someone@mail.com")

    page.get_by_role("button", name="Add Member").click()


    name_input = page.get_by_label("Name")
    is_invalid = name_input.evaluate("el => !el.checkValidity()")
    assert is_invalid, "Expected Name input to fail validation when left blank"
    expect(page.locator("body")).not_to_contain_text("someone@mail.com")


