import pytest
from flask_testing import TestCase
from unittest.mock import patch

# access all files in the main directory
import sys
sys.path.append("./")
import main
from main import app

class TestMemberPortal(TestCase):

    # This method is required by Flask-Testing to create and configure the Flask app for testing
    def create_app(self):
         # Enable testing mode to propagate exceptions and disable error catching
        app.config['TESTING'] = True
        return app # http://127.0.0.1:5000
    
    ############### Test login #######################
    # test login function
    def test_login_render_correct_templete_and_status(self) -> None:
        """
        Test if the /login route has done the floowing:
            - return HTTP status code 200 (OK)
            - redered the 'login.html' template
        """
        # hen you inherit from flask_testing.TestCase, it automatically provides a self.client attribute
        response = self.client.get('/login/') # go to the /login endpoint with a GET request
        
        # is the response code 200?
        self.assert200(response)

        # is the templete used 'login.html'
        self.assert_template_used('login.html')
    
    @patch('main.auth.auth_login', return_value=(True, 'TestUser'))  # Mock the login logic (roll playing as the fuction)
    def test_login_post_and_redirect_to_home_and_set_session(self, mock_auth) -> None:
        """
        Test POST to /login:
            - sends credentials
            - sets session['user']
            - redirects to /home/<username>
        """
        with self.client as c:
            # Submit POST login form with dummy credentials
            response = c.post('/login/', data={
                'user_email': 'test@example.com',
                'user_password': 'password123'
            })

            # Check redirect status
            self.assertStatus(response, 302)

            # Confirm redirect URL ends with the correct username
            self.assertTrue(response.location.endswith('/home/TestUser'))

            # Access and verify session data
            with c.session_transaction() as sess:
                self.assertEqual(sess.get('user'), 'TestUser')

    ############## Test home #######################
    def test_home_render_correct_templete_and_status(self) -> None:
        """
        Test if home/<username>  endpoint have done the floowing
            - return status code 200 (OK)
            - rendered 'home.html' template
        """
        with self.client as c:
            # simulate a logged-in session
            with c.session_transaction() as sess:
                sess['user'] = 'TestUser'

            response = c.get('/home/TestUser') # go to the /home endpoint with a GET request
            self.assert200(response) # is the response code 200?
            self.assert_template_used('home.html') # is the templete used 'home.html'


    