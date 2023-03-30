from typing import Optional

from flask import Flask
from flask_login import LoginManager, login_user, \
    logout_user, login_required, UserMixin

from ..model.util import init_app

class Auth:

    def __init__ (self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)
        else:
            raise Exception ("No flask app provided")

    def init_app (self, app: Flask):
        self.app = app

        init_app(self.app) # DB init

        # try:
        #     init_app(self.app) # DB init
        # except Exception as e:
        #     #logger.info(str(e))
        #     print ("DB init failed- likely due to incorrect Flask config")

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        # @self.login_manager.user_loader
        # def load_user (id):




    # def _authenticate_password (self, username_or_email: str, password: str):
    #     user = AuthUser(username_or_email, password, None)

