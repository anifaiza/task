from app import app, db
from app import User, Book
import os
import unittest
from unittest.mock import patch

class TestMyApp(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()
    
    def test_getting_all_books(self):
        #tester = app.test_client(self)
        resp = self.tester.get('/book')
        #status_code = resp.status_code
        self.assertEqual(resp.status_code, 401)

    #check if the content returned is application/json
    def test_content(self):
        #tester = app.test_client(self)
        resp = self.tester.get('/book')
        self.assertEqual(resp.content_type, 'application/json')

    '''def test_content_data(self):
        tester = app.test_client(self)
        resp = tester.get('/book')
        self.assertTrue(b'author' in resp.data)'''

if __name__ == '__main__':
    unittest.main()