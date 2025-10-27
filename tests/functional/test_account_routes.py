from flask import url_for, g
from tests.consts import UsersConsts
from tests import utils
from io_remastered import forms, CSRF
from io_remastered.io_csrf.csrf import CSRF_TOKEN_FIELD_NAME, CSRF_BARE_TOKEN_FIELD_NAME


def test_account_home_as_non_auth(test_client):
    response = test_client.get(url_for("account.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_account_home_as_auth(test_client, logged_test_user):
    response = test_client.get(url_for("account.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("account.home")


def test_change_password_as_non_auth(test_client):
    response = test_client.get(
        url_for("account.change_password"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_change_password_as_auth(test_client, logged_test_user):
    response = test_client.get(
        url_for("account.change_password"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("account.change_password")


def test_login_sessions_as_non_auth(test_client):
    response = test_client.get(
        url_for("account.login_sessions"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_login_sessions_as_auth(test_client, logged_test_user):
    response = test_client.get(
        url_for("account.login_sessions"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("account.login_sessions")


def test_storage_stats_as_non_auth(test_client):
    response = test_client.get(
        url_for("account.storage_stats"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_storage_stats_as_auth(test_client, logged_test_user):
    response = test_client.get(
        url_for("account.storage_stats"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("account.storage_stats")


def test_logs_preview_as_non_auth(test_client):
    response = test_client.get(
        url_for("account.logs_preview"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_logs_preview_as_auth(test_client, logged_test_user):
    response = test_client.get(
        url_for("account.logs_preview"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("account.logs_preview")


def test_handle_change_password_as_non_auth(test_client):
    response = test_client.post(
        url_for("account.handle_change_password"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_handle_change_password_as_auth(test_client, logged_test_user):
    form_data = {}
    csrf_token = CSRF.generate_token()

    utils.inject_into_session(test_client, {
        CSRF_TOKEN_FIELD_NAME: g.get(CSRF_BARE_TOKEN_FIELD_NAME),
    })

    form_data["password"] = UsersConsts.TEST_USER_PASSWORD
    form_data["new_password"] = UsersConsts.TEST_USER_CHANGED_PASSWORD
    form_data["confirm_password"] = UsersConsts.TEST_USER_CHANGED_PASSWORD
    form_data["csrf_token"] = csrf_token

    form = forms.ChangePasswordForm(form_data=form_data)

    response = test_client.post(
        url_for("account.handle_change_password"), data=form.form_data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("account.change_password")

    response = test_client.get(url_for("auth.logout"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")

    login_form = utils.get_login_form(
        test_client, password=UsersConsts.TEST_USER_CHANGED_PASSWORD)

    utils.inject_into_session(test_client, {
        CSRF_TOKEN_FIELD_NAME: g.get(CSRF_BARE_TOKEN_FIELD_NAME),
    })

    response = test_client.post(url_for("auth.login_submit"),
                                data=login_form.form_data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")
