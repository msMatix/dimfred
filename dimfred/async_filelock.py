# -*- coding: utf-8 -*-
import asyncio

from filelock import FileLock


class AsyncFileLock(FileLock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def acquire(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, super().acquire)

    def release(self, *args, **kwargs):
        super().release()

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, type_, value, traceback):
        self.release()
