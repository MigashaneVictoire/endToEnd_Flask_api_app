# access all files in the main directory
import sys
sys.path.append("./")
import auth


# class TestMemberPortal(TestCase):

def test_auth_login_success(monkeypatch):
    # mock retrieve_data_db_with_sql to return a correct user
    def mock_retrieve(query, params):
        return [("john_doe", "password123")]

    # mimicke the retrieve_data_db_with_sql functino from the auth file
    monkeypatch.setattr("auth.retrieve_data_db_with_sql", mock_retrieve)

    result = auth.auth_login("john@example.com", "password123")
    assert result == (True, "john_doe")

def test_auth_login_wrong_password(monkeypatch):
    def mock_retrieve(query, params):
        return [("john_doe", "password123")]

    # mimicke the retrieve_data_db_with_sql functino from the auth file
    monkeypatch.setattr("auth.retrieve_data_db_with_sql", mock_retrieve)

    result = auth.auth_login("john@example.com", "wrongpass")
    assert result == (False, "Incorrect Password!")

def test_auth_login_email_not_found(monkeypatch):
    def mock_retrieve(query, params):
        raise IndexError("Email NOT found!")

    # mimicke the retrieve_data_db_with_sql functino from the auth file
    monkeypatch.setattr("auth.retrieve_data_db_with_sql", mock_retrieve)

    result = auth.auth_login("notfound@example.com", "anything")
    assert result == "Email NOT found!"
