from app import app, db
import os
import unittest

class TestMyApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.tester = app.test_client()
        db.create_all()
    
    def test_getting_all_books(self):
        #tester = app.test_client(self)
        resp = self.tester.get('/book')
        status_code = resp.status_code
        self.assertEqual(status_code, 401)

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