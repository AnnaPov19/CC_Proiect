import unittest
import main
import firebase_admin

class TestTicketAPI(unittest.TestCase):
    def setUp(self):
        self.app = main.app.test_client()
        
    def test_create_ticket(self):
        response = self.app.post('/ticket', json={
            "data": "12.06.2025",
            "destinație": "Cluj-Napoca",
            "nume_client": "Andrei Popescu",
            "ora": "09:30"
        })
        self.assertEqual(response.status_code, 201)
        
    def test_get_invalid_ticket(self):
        response = self.app.get('/ticket/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()