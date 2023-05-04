from flask import Flask

from typing import List, Callable

from .base_middleware import WSGIMiddlewareFactory, WSGIApp

def wrap (app: Flask, middlewares: List[WSGIMiddlewareFactory]) -> Callable:
    if not hasattr(app, 'wsgi_app'):
        raise TypeError('Not a valid Flask app or middleware')
    if not hasattr(app, 'middlewares'):
        app.middlewares = {}

    # Middlewares need to be wrapped in reverse order of how they should be called
    wrapped_app: WSGIApp = app.wsgi_app
    for middleware in middlewares[::-1]:
        try:
            wrapped_app = middleware(wrapped_app, config=app.config)
        except TypeError as e:
            # TODO: Add logging
            # TODO: Add warning
            # TODO: Is this even a problem in python 3.11?
            """
            Maintain backward compatibility with middlewares
            that don't accept **kwargs. This should be extremely
            rare
            """
            wrapped_app = middleware(wrapped_app)

        key = getattr(middleware, '__name__', str(middleware))
        app.middlewares[key] = wrapped_app

    app.wsgi_app = wrapped_app
    return app