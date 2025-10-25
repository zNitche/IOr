import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from tests.consts import UsersConsts
from tests.test_app_config import TestAppConfig
from io_remastered import create_app, models, db, forms, CSRF


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app(config_class=TestAppConfig)
    client = flask_app.test_client()

    with flask_app.test_request_context():
        user = models.User(username=UsersConsts.TEST_USER_NAME,
                           password=UsersConsts.TEST_USER_PASSWORD,
                           max_storage_size=20)

        user.password = generate_password_hash(user.password)

        db.add(user, commit_on_completion=True)

        yield client


@pytest.fixture(scope="function")
def logged_test_user(test_client):
    form_data = {}
    csrf_token = CSRF.generate_token()

    form_data["name"] = UsersConsts.TEST_USER_NAME
    form_data["password"] = UsersConsts.TEST_USER_PASSWORD
    form_data["csrf_token"] = csrf_token

    login_form = forms.LoginForm(form_data=form_data)

    test_client.post(url_for("auth.login_submit"),
                     data=login_form.form_data, follow_redirects=True)

    yield

    test_client.get(url_for("auth.logout"), follow_redirects=True)
