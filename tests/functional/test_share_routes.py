from flask import url_for
from tests.consts import StorageConsts


def test_file_preview_missing_as_non_auth(test_client, with_shared_file):
    file_url = url_for(
        "share.file_preview", share_uuid="123")

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 404
    assert response.request.path == file_url


def test_file_preview_as_non_auth(test_client):
    file_url = url_for(
        "share.file_preview", share_uuid=StorageConsts.SHARED_FILE_SHARE_UUID)

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == file_url


def test_file_preview_as_auth(test_client, logged_test_user):
    file_url = url_for(
        "share.file_preview", share_uuid=StorageConsts.SHARED_FILE_SHARE_UUID)

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == file_url


def test_directory_preview_missing_as_non_auth(test_client):
    file_url = url_for(
        "share.directory_preview", share_uuid="123")

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 404
    assert response.request.path == file_url


def test_directory_preview_as_non_auth(test_client, with_shared_directory):
    file_url = url_for(
        "share.directory_preview", share_uuid=StorageConsts.SHARED_DIRECTORY_SHARE_UUID)

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == file_url


def test_directory_preview_as_auth(test_client, logged_test_user):
    file_url = url_for(
        "share.directory_preview", share_uuid=StorageConsts.SHARED_DIRECTORY_SHARE_UUID)

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == file_url


def test_directory_download_as_non_auth(test_client):
    file_url = url_for(
        "share.download_directory", share_uuid=StorageConsts.SHARED_DIRECTORY_SHARE_UUID)

    response = test_client.get(file_url, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == file_url


def test_file_download_as_non_auth(test_client):
    file_url = url_for(
        "share.download_file", share_uuid=StorageConsts.SHARED_FILE_SHARE_UUID)

    try:
        test_client.get(file_url, follow_redirects=True)
    except FileNotFoundError:
        pass

