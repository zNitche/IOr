import json
from typing import Any
from io_remastered import db, authentication_manager
from io_remastered.models import UserSecurityLog
from io_remastered.types import LogTypeEnum, ActionLogKeyEnum, SecurityLogKeyEnum


def log_security(key: SecurityLogKeyEnum, formats: dict[str, Any] | None = None,
                 user_id: int | None = None):
    __create_log(type=LogTypeEnum.Security, message_obj={
        "key": key.value,
        "formats": formats
    }, user_id=user_id)


def log_action(key: ActionLogKeyEnum, formats: dict[str, Any] | None = None):
    __create_log(type=LogTypeEnum.Action, message_obj={
        "key": key.value,
        "formats": formats
    })


def __create_log(type: LogTypeEnum, message_obj: dict[str, Any], user_id: int | None = None):
    user = authentication_manager.current_user
    user_id = user_id if user_id is not None else user.id if user is not None else None

    if user_id is None:
        return

    dumped_message_obj = json.dumps(message_obj)

    log = UserSecurityLog(
        type=type.value, message_obj=dumped_message_obj, user_id=user_id)
    db.add(log)
