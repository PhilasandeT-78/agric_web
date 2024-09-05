from werkzeug.security import generate_password_hash

# Test the hashing method
try:
    hashed_password = generate_password_hash('mysecretpassword', method='pbkdf2:sha256')
    print('Password hashed successfully:', hashed_password)
except ValueError as e:
    print('Error:', e)
