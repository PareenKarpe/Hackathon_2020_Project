from user import app
import unittest

class JunitTest1(unittest.TestCase):
   def test_authentication_req (self):
   	tester = app.test_client(self)
   	#valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
    #response = self.app.get('/api/v1/login/', headers={'Authorization': 'Basic ' + valid_credentials})
   	response = tester.get('/user',method='GET')
   	print("Testing scenario: Cannot get user details without  basic authentication")
   	print("status_code:")
   	print(response.status_code)
   	self.assertEqual(response.status_code,401)
if __name__ == '__main__':
	unittest.main()