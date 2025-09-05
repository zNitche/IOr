from uuid import uuid4
from flask import Flask
from io_remastered import app_helpers
from io_remastered import authentication_manager, __version__
from io_remastered.io_forms import CSRFTokenField


def setup_constext_processor(app: Flask):
    app.context_processor(
        lambda: {"get_static_resource": app_helpers.context_processor_funcs.get_static_resource})

    app.context_processor(
        lambda: {"icon_for_file_extension": app_helpers.context_processor_funcs.icon_for_file_extension})

    app.context_processor(
        lambda: {"current_user": lambda: authentication_manager.current_user})

    app.context_processor(
        lambda: {"get_taken_user_storage": app_helpers.user_storage.get_taken_storage})

    app.context_processor(
        lambda: {"csrf_hidden_input": CSRFTokenField})

    app.context_processor(
        lambda: {"io_version": __version__})
    
    app.context_processor(
        lambda: {"unpack_dict": app_helpers.context_processor_funcs.unpack_dict})
    
    app.context_processor(
        lambda: {"is_viewed_by_owner": app_helpers.context_processor_funcs.is_viewed_by_owner})
    
    app.context_processor(
        lambda: {"get_uuid": lambda: uuid4().hex})


def setup_template_filters(app: Flask):
    app.jinja_env.filters["formatted_file_size"] = app_helpers.jinja_filters.formatted_file_size
