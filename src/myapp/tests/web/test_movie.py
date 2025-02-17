def test_get(client):
    resp = client.get('/movies')
    assert resp.status_code == 200
    assert len(resp.json()) == 5
