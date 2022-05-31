from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xc4\x05\xc6iN\xb3\xd9\x8f\x0ea\x19\xd7\xae\xf3\xfbK'
