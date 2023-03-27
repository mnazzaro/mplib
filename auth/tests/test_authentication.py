from flask import Flask

from unittest import TestCase

from .. import Auth, authentication
from .. auth_user import AuthUser
from ...model import model, util

class TestAuthenticationController (TestCase):

    @classmethod
    def setUpClass (self):
        self.redis = 'redis://127.0.0.1:6379'
        self.db = 'postgresql://test:test@localhost/mpdb'
        self.expiry = 500


    def setUp (self):
        self.app = Flask(__name__) # Build plain flask app
        self.app.config['SECRET_KEY'] = 'super_secret_secret'
        self.app.config['SERVICE_TYPE_FOR_AUTH'] = 'GAME'
        self.app.config['CELERY_RESULT_BACKEND'] = self.redis
        self.app.config['CELERY_BROKER_URL'] = self.redis
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

        Auth(self.app)
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        with self.app.app_context():
            util.drop_all()
            util.create_all()

            with util.transaction() as session:
                salt = authentication._generate_salt()
                player = model.DBPlayer (
                    username='markn',
                    first_name='Mark',
                    last_name='Nazzaro',
                    email='marknazzaro2@gmail.com',
                    pass_hash=authentication._get_pass_hash('passw0rD!', salt),
                    salt=salt,
                    account_balance=200
                )
                session.add(player)
                session.commit()

    def test_login_success (self):
        with self.app.app_context():
            with self.client:
                player = AuthUser('marknazzaro2@gmail.com', 'passw0rD!', None)
                response = authentication.try_login(player)
                self.assertEqual(response, True, f"Successful login incorrectly returns False {player.get()}")

    def test_login_failure (self):
        with self.app.app_context():
            with self.client:
                player = AuthUser('badguy@gmail.com', 'passw0rD!', None)
                response = authentication.try_login(player)
        self.assertEqual(response, False, "Failed login incorrectly returns True")



"""
VALUES (
    DEFAULT, -- Auto-incrementing integer starting at 0
    'markn', 
    'Mark',
    'Nazzaro',
    'marknazzaro2@gmail.com',
    DEFAULT, -- Timezone aware timestamp of now
    

)

SERVICE_TYPE_FOR_AUTH = 'GAME'

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

SQLALCHEMY_DATABASE_URI = 'postgresql://markn@localhost/mpdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
"""