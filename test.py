from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_check_word(self):
        app.testing = True
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'D', 'T'],
                                 ['U', 'V', 'W', 'O', 'G']]

            response = client.get('/check-word?word=zzz')  # Use a word that is not in the dictionary
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['result'], 'not-word')

            response = client.get('/check-word?word=dog')  # This word can be found on the board
            data = json.loads(response.data)
            self.assertEqual(data['result'], 'ok')  # Update the expected result to 'ok'

            response = client.get('/check-word?word=invalidword')
            data = json.loads(response.data)
            self.assertEqual(data['result'], 'not-word')


    def test_post_score(self):
        app.testing = True
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['plays'] = 1
                sess['high_score'] = 10

            response = client.post('/post-score', json={'score': 15})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['plays'], 2)
            self.assertEqual(data['high_score'], 15)

            response = client.post('/post-score', json={'score': 5})
            data = json.loads(response.data)
            self.assertEqual(data['plays'], 3)
            self.assertEqual(data['high_score'], 15)


if __name__ == '__main__':
    import unittest
    unittest.main()
