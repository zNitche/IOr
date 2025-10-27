from flask import url_for


def test_storage_directories_preview_as_non_auth(test_client):
    response = test_client.get(
        url_for("storage.directories.preview", uuid="123"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_storage_directories_preview_as_auth(test_client, logged_test_user, with_directory):
    target_url = url_for("storage.directories.preview", uuid="123")

    response = test_client.get(target_url, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == target_url


def test_storage_directories_preview_as_auth_not_found(test_client, logged_test_user):
    target_url = url_for("storage.directories.preview", uuid="1234")

    response = test_client.get(target_url, follow_redirects=True)

    assert response.status_code == 404


def test_storage_directories_preview_as_auth_not_owner(test_client, logged_test_user, with_directory_2):
    target_url = url_for("storage.directories.preview", uuid="12345")

    response = test_client.get(target_url, follow_redirects=True)

    assert response.status_code == 404
