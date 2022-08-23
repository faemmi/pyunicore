import json, unittest

import credentials
        
class TestJWTCredentials(unittest.TestCase):
    def setUp(self):
        pass

    def test_hs256(self):
        print("*** test_hs256")
        credential = credentials.JWTToken("CN=Demouser", "CN=My Service",
                                          secret="test123", algorithm="HS256", etd=True)
        print(credential.create_token())

if __name__ == '__main__':
    unittest.main()
