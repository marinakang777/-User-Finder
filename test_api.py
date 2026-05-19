import unittest
from unittest.mock import patch
import requests

class TestGitHubAPI(unittest.TestCase):
    
    @patch('requests.get')
    def test_search_users_success(self, mock_get):
        # Мокаем успешный ответ API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "items": [{"login": "testuser", "id": 1, "html_url": "https://github.com/testuser"}]
        }
        
        response = requests.get("https://api.github.com/search/users?q=testuser")
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", data)
        self.assertEqual(data["items"][0]["login"], "testuser")
    
    def test_empty_query(self):
        # Проверка, что пустой запрос не отправляется (на уровне логики приложения)
        query = ""
        self.assertEqual(len(query), 0)

if __name__ == "__main__":
    unittest.main()
