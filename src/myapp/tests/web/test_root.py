def test_get(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json()['message'] == 'Hello'
