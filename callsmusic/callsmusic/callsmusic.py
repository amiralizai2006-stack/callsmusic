from typing import Dict, Any

from pytgcalls import GroupCall

from . import client
from .. import queues

instances: Dict[int, GroupCall] = {}
active_chats: Dict[int, Dict[str, Any]] = {}


def init_instance(chat_id: int):
    if chat_id not in instances:
        instances[chat_id] = GroupCall(client)

    instance = instances[chat_id]

    @instance.on_playout_ended
    async def ___(__, _):
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await stop(chat_id)
        else:
            next_item = queues.get(chat_id)
            # next_item expected to be dict with 'file' and optional metadata
            instance.input_filename = next_item.get('file') if isinstance(next_item, dict) else next_item
            # update current metadata
            if chat_id in active_chats and isinstance(next_item, dict):
                active_chats[chat_id]['current'] = {
                    'title': next_item.get('title'),
                    'by': next_item.get('by'),
                }


def remove(chat_id: int):
    if chat_id in instances:
        del instances[chat_id]

    if not queues.is_empty(chat_id):
        queues.clear(chat_id)

    if chat_id in active_chats:
        del active_chats[chat_id]


def get_instance(chat_id: int) -> GroupCall:
    init_instance(chat_id)
    return instances[chat_id]


async def start(chat_id: int):
    await get_instance(chat_id).start(chat_id)
    active_chats[chat_id] = {'playing': True, 'muted': False, 'current': None}


async def stop(chat_id: int):
    await get_instance(chat_id).stop()

    if chat_id in active_chats:
        del active_chats[chat_id]


async def set_stream(chat_id: int, file: str, metadata: Dict[str, str] = None):
    if chat_id not in active_chats:
        await start(chat_id)
    get_instance(chat_id).input_filename = file
    if chat_id in active_chats:
        active_chats[chat_id]['current'] = {
            'title': metadata.get('title') if metadata else None,
            'by': metadata.get('by') if metadata else None,
        }


def pause(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif not active_chats[chat_id]['playing']:
        return False

    get_instance(chat_id).pause_playout()
    active_chats[chat_id]['playing'] = False
    return True


def resume(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif active_chats[chat_id]['playing']:
        return False

    get_instance(chat_id).resume_playout()
    active_chats[chat_id]['playing'] = True
    return True


def mute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif active_chats[chat_id]['muted']:
        return 1

    get_instance(chat_id).set_is_mute(True)
    active_chats[chat_id]['muted'] = True
    return 0


def unmute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif not active_chats[chat_id]['muted']:
        return 1

    get_instance(chat_id).set_is_mute(False)
    active_chats[chat_id]['muted'] = False
    return 0
