import json
from typing import Any
from io_remastered import db, authentication_manager
from io_remastered.models import Log
from io_remastered.types import LogTypeEnum


def log_security(message_key: str, formats: dict[str, Any] | None = None,
                 user_id: int | None = None):
    create_log(type=LogTypeEnum.Security, message_obj={
        "key": message_key,
        "formats": formats
    }, user_id=user_id)


def log_action(message_key: str, formats: dict[str, Any] | None = None):
    create_log(type=LogTypeEnum.Action, message_obj={
        "key": message_key,
        "formats": formats
    })


def create_log(type: LogTypeEnum, message_obj: dict[str, Any], user_id: int | None = None):
    user = authentication_manager.current_user
    user_id = user_id if user_id is not None else user.id if user is not None else None

    if user_id is None:
        return

    dumped_message_obj = json.dumps(message_obj)

    log = Log(type=type.value, message_obj=dumped_message_obj, user_id=user_id)
    db.add(log)
