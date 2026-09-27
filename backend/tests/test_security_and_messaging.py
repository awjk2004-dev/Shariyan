from backend.tests.test_api import register_and_login


def register_user(client, email):
    response = client.post("/api/auth/register", json={
        "full_name": "Another User",
        "email": email,
        "password": "StrongPass123",
        "phone": "0511111111",
        "city": "Jeddah",
    })
    assert response.status_code == 201
    login = client.post("/api/auth/login", data={"username": email, "password": "StrongPass123"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_non_admin_cannot_manage_users(client):
    headers = register_and_login(client)
    response = client.get("/api/admin/users", headers=headers)
    assert response.status_code == 403


def test_malformed_token_is_rejected_cleanly(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401


def test_bootstrap_admin_and_manage_users(client):
    register_and_login(client)
    response = client.post("/api/auth/bootstrap-admin", headers={"X-Admin-Bootstrap-Token": "test-bootstrap-token"})
    assert response.status_code == 200
    login = client.post("/api/auth/login", data={"username": "ahmed@example.com", "password": "StrongPass123"})
    admin_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    assert client.get("/api/admin/users", headers=admin_headers).status_code == 200
    assert client.post("/api/auth/bootstrap-admin", headers={"X-Admin-Bootstrap-Token": "test-bootstrap-token"}).status_code == 409


def test_admin_report_covers_request_flow(client):
    headers = register_and_login(client)
    client.post("/api/requests", headers=headers, json={
        "patient_name": "Report Patient",
        "blood_type": "O+",
        "city": "Riyadh",
        "hospital": "Report Hospital",
        "units": 1,
        "urgent": True,
    })
    assert client.get("/api/admin/reports/overview", headers=headers).status_code == 403
    client.post("/api/auth/bootstrap-admin", headers={"X-Admin-Bootstrap-Token": "test-bootstrap-token"})
    login = client.post("/api/auth/login", data={"username": "ahmed@example.com", "password": "StrongPass123"})
    admin_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    report = client.get("/api/admin/reports/overview", headers=admin_headers)
    assert report.status_code == 200
    assert report.json()["totals"]["requests"] == 1
    assert report.json()["urgent_open_requests"] == 1
    assert report.json()["requests_by_blood_type"]["O+"] == 1


def test_internal_messages_are_scoped_to_participants(client):
    first_headers = register_and_login(client)
    second_headers = register_user(client, "second@example.com")
    users = client.get("/api/auth/me", headers=first_headers).json()
    recipient = client.get("/api/auth/me", headers=second_headers).json()
    sent = client.post("/api/messages", headers=first_headers, json={"recipient_id": recipient["id"], "content": "هل ما زال الطلب مفتوحًا؟"})
    assert sent.status_code == 201
    conversation = client.get(f"/api/messages/{users['id']}", headers=second_headers)
    assert conversation.status_code == 200
    assert conversation.json()[0]["content"] == "هل ما زال الطلب مفتوحًا؟"
    notifications = client.get("/api/notifications", headers=second_headers)
    assert notifications.status_code == 200
    assert notifications.json()[0]["title"] == "رسالة جديدة"
    marked = client.patch(f"/api/notifications/{notifications.json()[0]['id']}/read", headers=second_headers)
    assert marked.status_code == 200
    invalid = client.post("/api/messages", headers=first_headers, json={"recipient_id": users["id"], "content": "رسالة لنفسي"})
    assert invalid.status_code == 400


def test_blood_request_notifies_matching_donor(client):
    donor_headers = register_and_login(client)
    client.post("/api/donors/me", headers=donor_headers, json={"blood_type": "A+"})
    client.post("/api/auth/register", json={
        "full_name": "Request Owner",
        "email": "request-owner@example.com",
        "password": "StrongPass123",
        "phone": "0522222222",
        "city": "Riyadh",
    })
    login = client.post("/api/auth/login", data={"username": "request-owner@example.com", "password": "StrongPass123"})
    requester_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    created = client.post("/api/requests", headers=requester_headers, json={
        "patient_name": "Matching Patient",
        "blood_type": "A+",
        "city": "Riyadh",
        "hospital": "Matching Hospital",
        "units": 1,
        "urgent": True,
    })
    assert created.status_code == 201
    notifications = client.get("/api/notifications", headers=donor_headers)
    assert notifications.status_code == 200
    assert notifications.json()[0]["title"] == "طلب دم قريب منك"
