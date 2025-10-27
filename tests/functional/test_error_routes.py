def test_404_page(test_client):
    response = test_client.get("/404page", follow_redirects=True)

    assert response.status_code == 404
    assert response.request.path == "/404page"
