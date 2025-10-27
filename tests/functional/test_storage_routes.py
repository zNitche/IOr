from flask import url_for, g
from tests import utils
from io_remastered import forms, CSRF
from io_remastered.io_csrf.csrf import CSRF_TOKEN_FIELD_NAME, CSRF_BARE_TOKEN_FIELD_NAME


def test_storage_add_directory_as_non_auth(test_client):
    response = test_client.post(
        url_for("storage.add_directory"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_storage_add_directory_as_auth_invalid_csrf(test_client, logged_test_user):
    form_data = {}
    form_data["name"] = "test_dir_name"

    form = forms.CreateDirectoryForm(form_data=form_data)

    response = test_client.post(
        url_for("storage.add_directory"), data=form.form_data, follow_redirects=True)

    assert response.status_code == 403


def test_storage_add_directory_as_auth(test_client, logged_test_user):
    form_data = {}
    csrf_token = CSRF.generate_token()

    utils.inject_into_session(test_client, {
        CSRF_TOKEN_FIELD_NAME: g.get(CSRF_BARE_TOKEN_FIELD_NAME),
    })

    directory_name = "test_dir_name"

    form_data["name"] = directory_name
    form_data["csrf_token"] = csrf_token

    form = forms.CreateDirectoryForm(form_data=form_data)

    response = test_client.post(
        url_for("storage.add_directory"), data=form.form_data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")
