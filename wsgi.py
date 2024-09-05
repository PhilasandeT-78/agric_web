import sys
import os


path = '/Users/user/web-system'
if path not in sys.path:
    sys.path.insert(0, path)


os.environ['FLASK_APP'] = 'app'


from app import app as application


