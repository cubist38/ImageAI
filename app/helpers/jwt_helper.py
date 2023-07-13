import jwt

class JwtHelper:
    _instance = None 

    def __new__(cls):
        if (cls._instance == None): 
            cls._instance = super().__new__(cls)
            cls._instance.secret_key = 'this_is_a_weak_secret_key|X_X'
        return cls._instance

    def sign_jwt(self, email):
        payload = {'email': email}
        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return encoded_jwt

    def verify_jwt(self, encoded_jwt):
        try:
            decoded_payload = jwt.decode(encoded_jwt, self.secret_key, algorithms=['HS256'])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Expired token'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}
