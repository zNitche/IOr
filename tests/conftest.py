import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from tests.consts import UsersConsts
from tests.test_app_config import TestAppConfig
from tests import utils
from io_remastered import create_app, models, db


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app(config_class=TestAppConfig)

    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            user = models.User(username=UsersConsts.TEST_USER_NAME,
                               password=UsersConsts.TEST_USER_PASSWORD,
                               max_storage_size=20)

            user.password = generate_password_hash(user.password)
            db.add(user, commit_on_completion=True)

            yield client


@pytest.fixture(scope="function", autouse=False)
def logged_test_user(test_client):
    login_form = utils.get_login_form(test_client)

    test_client.post(url_for("auth.login_submit"),
                     data=login_form.form_data)

    yield

    test_client.get(url_for("auth.logout"))
