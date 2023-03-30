from typing import Callable, Tuple, Iterable, Mapping
from typing_extensions import Protocol

WSGIRequest = Tuple[dict, Callable]
WSGIResponse = Iterable
WSGIApp = Callable[[dict, Callable], WSGIResponse]

class WSGIMiddleware(Protocol):
    """Defines a minimal class that can be used as a middleware."""

    def __init__(self, wsgi_app: WSGIApp, config: Mapping = {}) -> None:
        """Initialize with an WSGI app and an optional configuration."""
        ...

    def __call__(self, environ: dict, start: Callable) -> WSGIResponse:
        """Support the WSGI protocol."""
        ...

    @property
    def wsgi_app(self) -> WSGIApp:
        """Offer a ``wsgi_app`` property, per :class:`.Flask` behavior."""
        ...


class WSGIMiddlewareFactory(Protocol):
    """Defines a minimal WSGI middleware factory."""

    def __call__(self, app: WSGIApp, config: Mapping = {}) -> IWSGIMiddleware:
        """Generate a :class:`.WSGIMiddleware`."""
        ...

class BaseMiddleware:

    def __init__ (self, wsgi_app: WSGIApp, config: Mapping = {}) -> None:
        self.app = wsgi_app
        self.config = config

    def before (self, environ: dict, start_response: Callable) -> WSGIRequest:
        return environ, start_response
    
    def after (self, response: WSGIResponse) -> WSGIResponse:
        return response
    
    def __call__ (self, environ: dict, start: Callable) -> WSGIResponse:
        environ, start_response = self.before(environ, start)
        response: WSGIResponse = self.app(environ, start)
        response = self.after(response)
        return response
    
    @property
    def wsgi_app (self):
        return self
