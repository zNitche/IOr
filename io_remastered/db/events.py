import os
from sqlalchemy import event
from flask import current_app
from io_remastered import models, db


@event.listens_for(models.File, "after_delete")
def receive_after_file_delete(mapper, connection, target):
    if not current_app:
        return

    storage_root_path = current_app.config["STORAGE_ROOT_PATH"]
    file_path = os.path.join(storage_root_path, str(target.owner_id), target.uuid)

    if os.path.exists(file_path):
        os.remove(file_path)
