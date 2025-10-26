from flask import g
from typing import Any
from tests.consts import UsersConsts
from io_remastered import forms, CSRF
from io_remastered.io_csrf.csrf import CSRF_TOKEN_FIELD_NAME, CSRF_BARE_TOKEN_FIELD_NAME


def inject_into_session(test_client, data: dict[str, Any]):
    with test_client.session_transaction() as session:
        for key in data.keys():
            session[key] = data[key]


def get_login_form(test_client):
    form_data = {}

    csrf_token = CSRF.generate_token()

    inject_into_session(
        test_client, {CSRF_TOKEN_FIELD_NAME: g.get(CSRF_BARE_TOKEN_FIELD_NAME)})

    form_data["name"] = UsersConsts.TEST_USER_NAME
    form_data["password"] = UsersConsts.TEST_USER_PASSWORD
    form_data["csrf_token"] = csrf_token

    return forms.LoginForm(form_data=form_data)
