# -*- coding: utf-8 -*-
from functools import wraps

from filelock import FileLock

from .async_filelock import AsyncFileLock


def celery_once(lock_path, exit_if_locked=True):
    def deco(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            lock = FileLock(lock_path)
            if lock.is_locked and exit_if_locked:
                return

            with lock:
                return f(*args, **kwargs)

        return wrapper

    return deco


def acelery_once(lock_path, exit_if_locked=True):
    def deco(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            lock = AsyncFileLock(lock_path)
            if lock.is_locked and exit_if_locked:
                return

            async with lock:
                return await f(*args, **kwargs)

        return wrapper

    return deco
