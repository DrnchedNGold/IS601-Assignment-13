import pytest
from playwright.sync_api import Page

@pytest.mark.e2e
def test_register_valid(page: Page):
    page.goto("http://localhost:8000/register")
    page.fill("#username", "testuser1")
    page.fill("#email", "testuser1@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "ValidPass123!")
    page.fill("#confirm_password", "ValidPass123!")
    page.fill("#password", "ValidPass123!")
    page.fill("#confirm_password", "ValidPass123!")
    page.click("button[type=submit]")
    page.wait_for_selector("#successAlert", state="visible")
    assert "Registration successful" in page.inner_text("#successMessage")

@pytest.mark.e2e
def test_register_short_password(page: Page):
    page.goto("http://localhost:8000/register")
    page.fill("#username", "testuser2")
    page.fill("#email", "testuser2@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "short")
    page.fill("#confirm_password", "short")
    page.click("button[type=submit]")
    page.wait_for_selector("#errorAlert", state="visible")
    assert "Password must be at least 8 characters" in page.inner_text("#errorMessage")

@pytest.mark.e2e
def test_login_valid(page: Page):
    # First, register the user
    page.goto("http://localhost:8000/register")
    page.fill("#username", "testuser3")
    page.fill("#email", "testuser3@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "ValidPass123!")
    page.fill("#confirm_password", "ValidPass123!")
    page.click("button[type=submit]")
    page.wait_for_selector("#successAlert", state="visible")
    # Now login
    page.goto("http://localhost:8000/login")
    page.fill("#username", "testuser3")
    page.fill("#password", "ValidPass123!")
    page.click("button[type=submit]")
    page.wait_for_selector("#successAlert", state="visible")
    assert "Login successful" in page.inner_text("#successMessage")
    # Check JWT stored
    access_token = page.evaluate("window.localStorage.getItem('access_token')")
    assert access_token is not None and len(access_token) > 0

@pytest.mark.e2e
def test_login_wrong_password(page: Page):
    # First, register the user
    page.goto("http://localhost:8000/register")
    page.fill("#username", "testuser4")
    page.fill("#email", "testuser4@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "ValidPass123!")
    page.fill("#confirm_password", "ValidPass123!")
    page.click("button[type=submit]")
    page.wait_for_selector("#successAlert", state="visible")
    # Now login with wrong password
    page.goto("http://localhost:8000/login")
    page.fill("#username", "testuser4")
    page.fill("#password", "WrongPass123")
    page.click("button[type=submit]")
    page.wait_for_selector("#errorAlert", state="visible")
    assert "Invalid username or password" in page.inner_text("#errorMessage")
