from flask import url_for, session, g
from tests.consts import UsersConsts
from io_remastered import forms, CSRF
from io_remastered.io_csrf.csrf import CSRF_TOKEN_FIELD_NAME, CSRF_BARE_TOKEN_FIELD_NAME


def get_login_form(test_client):
    form_data = {}

    csrf_token = CSRF.generate_token()

    with test_client.session_transaction() as session:
        session[CSRF_TOKEN_FIELD_NAME] = g.get(CSRF_BARE_TOKEN_FIELD_NAME)

    form_data["name"] = UsersConsts.TEST_USER_NAME
    form_data["password"] = UsersConsts.TEST_USER_PASSWORD
    form_data["csrf_token"] = csrf_token

    return forms.LoginForm(form_data=form_data)


def test_login_as_non_auth(test_client):
    response = test_client.get(url_for("auth.login"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_login_as_auth(test_client, logged_test_user):
    response = test_client.get(url_for("auth.login"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")


def test_login_submit_as_non_auth(test_client):
    login_form = get_login_form(test_client)

    response = test_client.post(url_for("auth.login_submit"),
                                data=login_form.form_data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")


def test_login_submit_as_auth(test_client, logged_test_user):
    response = test_client.post(url_for("auth.login_submit"),
                                data={}, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")


def test_password_authentication_as_non_auth(test_client):
    response = test_client.get(
        url_for("auth.password_authentication"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_password_authentication_as_auth_empty_origin(test_client, logged_test_user):
    response = test_client.get(
        url_for("auth.password_authentication"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")


def test_password_authentication_as_auth(test_client, logged_test_user):
    with test_client.session_transaction() as session:
        session["password_authentication_origin"] = url_for("core.files")

    response = test_client.get(
        url_for("auth.password_authentication"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.password_authentication")


def test_password_authentication_submit_as_non_auth(test_client):
    response = test_client.post(
        url_for("auth.password_authentication_submit"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_password_authentication_submit_as_auth(test_client, logged_test_user):
    form_data = {}
    csrf_token = CSRF.generate_token()

    with test_client.session_transaction() as session:
        session[CSRF_TOKEN_FIELD_NAME] = g.get(CSRF_BARE_TOKEN_FIELD_NAME)
        session["password_authentication_origin"] = url_for("core.files")

    form_data["password"] = UsersConsts.TEST_USER_PASSWORD
    form_data["csrf_token"] = csrf_token

    form = forms.PasswordAuthenticationForm(form_data=form_data)

    response = test_client.post(
        url_for("auth.password_authentication_submit"), data=form.form_data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.files")
