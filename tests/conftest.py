import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from tests.consts import UsersConsts, StorageConsts
from tests.test_app_config import TestAppConfig
from tests import utils
from io_remastered import create_app, models, db


@pytest.fixture(scope="module")
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

    with test_client.session_transaction() as session:
        session.clear()


@pytest.fixture(scope="function", autouse=False)
def with_file():
    file = models.File(name="test_file", extension="txt",
                       size=200, sha256_sum="123", owner_id=1)

    db.add(file, commit_on_completion=True)


@pytest.fixture(scope="function", autouse=False)
def with_shared_file():
    file = models.File(name="test_file", extension="txt",
                       size=200, sha256_sum="123", owner_id=1,
                       share_uuid=StorageConsts.SHARED_FILE_SHARE_UUID)

    db.add(file, commit_on_completion=True)


@pytest.fixture(scope="function", autouse=False)
def with_shared_directory():
    directory = models.Directory(name="test_directory", owner_id=1,
                                 share_uuid=StorageConsts.SHARED_DIRECTORY_SHARE_UUID)

    db.add(directory, commit_on_completion=True)
