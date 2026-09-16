from asyncio import Queue as _Queue
from asyncio import QueueEmpty as Empty
from typing import Dict, List, Any


class Queue(_Queue):
    def __init__(self):
        super().__init__()
        # maintain a snapshot list for read-only views
        self._items: List[Dict[str, Any]] = []

    async def put(self, item):
        # item is expected to be a dict
        self._items.append(item)
        await super().put(item)

    def get_nowait(self):
        # pop from snapshot then return from underlying queue
        try:
            item = super().get_nowait()
        except Exception:
            raise Empty
        # also remove from snapshot if present
        if self._items:
            try:
                self._items.pop(0)
            except Exception:
                pass
        return item

    def qsize(self):
        return len(self._items)

    def empty(self):
        return len(self._items) == 0

    def task_done(self):
        try:
            super().task_done()
        except Exception:
            pass

    def clear(self):
        # clear snapshot and drain underlying queue
        self._items.clear()
        try:
            while True:
                super().get_nowait()
        except Exception:
            pass


queues: Dict[int, Queue] = {}


async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()


def get(chat_id: int) -> Dict[str, Any]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return {}
    return {}


def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True


def task_done(chat_id: int):
    if chat_id in queues:
        queues[chat_id].task_done()


def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].clear()
    raise Empty


def list_queue(chat_id: int) -> List[Dict[str, Any]]:
    """Return a snapshot list of queued items for chat_id without removing them."""
    if chat_id in queues:
        return list(queues[chat_id]._items)
    return []
