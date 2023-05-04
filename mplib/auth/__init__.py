from typing import Optional, Union, Any

from flask import Flask, Response, request
from flask_login import LoginManager, login_user, \
    logout_user, login_required, UserMixin

from ..model.util import init_app as init_db
from ..model.util import current_session
from ..model.domain import Session

class Auth:

    def __init__ (self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)
        else:
            raise Exception ("No flask app provided")

    def init_app (self, app: Flask):
        self.app = app

        init_db(self.app)
        self.app.before_request(self.load_session)

        @self.app.teardown_request
        def teardown_request(exception: Optional[Exception]) -> None:
            session = current_session()
            if exception:
                session.rollback()
            session.remove()

        @self.app.teardown_appcontext
        def teardown_appcontext(*args: Any, **kwargs: Any) -> None:
            session = current_session()
            session.rollback()
            session.remove()
        # try:
        #     init_app(self.app) # DB init
        # except Exception as e:
        #     #logger.info(str(e))
        #     print ("DB init failed- likely due to incorrect Flask config")

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        # @self.login_manager.user_loader
        # def load_user (id):

    def load_session (self) -> Optional[Response]:
        
        session: Optional[Union[Session, Exception]] = \
            request.environ.get('session')
        
        if isinstance(session, Exception):
            # TODO: Add logging
            raise session

        request.auth = session

        return None



    # def _authenticate_password (self, username_or_email: str, password: str):
    #     user = AuthUser(username_or_email, password, None)

