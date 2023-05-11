from typing import Optional, Any
from flask import Flask

from datetime import datetime, timedelta
from pytz import UTC

import redis
# import rediscluster

import jwt
import uuid
import os
import secrets
import json

from ..base.globals import get_application_config

class MemoryStore:

    def __init__(self, 
                 host: str, 
                 port: int,
                 cluster: bool = True, 
                 fake: bool = False) -> None:

        # TODO: Add fakeredis for testing

        # TODO: FIX PYTHON VERSION TO ALLOW FOR STRICTREDISCLUSTER
        # if cluster:
        #     self.r = redis.StrictRedisCluster(
        #         startup_nodes=[{'host': host, 'port': str(port)}],
        #         skip_full_coverage_check=True # TODO: We will probably have to reevaluate this later
        #     )
        # else:
        #     self.r = redis.StrictRedis(host=host, port=port)
        self.r = redis.StrictRedis(host=host, port=port)

    def write_dict_as_json (self, key: str, data: dict, expiration: Optional[float] = None) -> None:
        self.r.set(key, json.dumps(data), ex=expiration)
        # TODO: Handle json errors and redis connection errors

    def read_json_as_dict (self, key: str) -> Optional[dict]:
        return json.loads(self.r.get(key))
    
    def write_raw (self, key: str, data: Any, expiration: Optional[float] = None) -> None:
        self.r.set(key, data, ex=expiration)

    def read_raw (self, key: str) -> Optional[Any]:
        self.r.get(key)
    
    # TODO: Change these to our values later
    @classmethod
    def init_app(cls, app: Flask = None) -> None:
        """Set default configuration parameters for an application instance."""
        config = get_application_config(app)
        config.setdefault('REDIS_HOST', 'host.docker.internal')
        config.setdefault('REDIS_PORT', '6379')
        config.setdefault('REDIS_DATABASE', '0')
        config.setdefault('REDIS_TOKEN', None)
        config.setdefault('REDIS_CLUSTER', '1')
        config.setdefault('REDIS_FAKE', False)

    @classmethod
    def build (cls, app: Flask):
        cls.init_app(app)
        config = get_application_config(app)
        return cls(
            host=config.get('REDIS_HOST'),
            port=config.get('REDIS_PORT'),
            cluster=config.get('REDIS_CLUSTER'),
            fake=config.get('REDIS_FAKE')
        )