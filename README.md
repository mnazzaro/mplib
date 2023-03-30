# Metal Poker Lib

This library is intended to abstract away all datastore calls made by the rest of the application.
Any python module can import mplib to gain utilities for authentication, authorization and sessions
so that they are consistent across all the services. Mplib will also contains helpers and 
abstractions for game logic in the future.