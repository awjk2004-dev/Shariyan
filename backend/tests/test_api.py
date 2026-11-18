def register_and_login(client):
    response = client.post("/api/auth/register", json={
        "full_name": "Ahmed Donor",
        "email": "ahmed@example.com",
        "password": "StrongPass123",
        "phone": "0500000000",
        "city": "Riyadh",
    })
    assert response.status_code == 201
    login = client.post("/api/auth/login", data={"username": "ahmed@example.com", "password": "StrongPass123"})
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_registration_donor_and_blood_request(client):
    headers = register_and_login(client)
    donor = client.post("/api/donors/me", headers=headers, json={"blood_type": "O+"})
    assert donor.status_code == 201
    assert donor.json()["blood_type"] == "O+"

    request = client.post("/api/requests", headers=headers, json={
        "patient_name": "Sara",
        "blood_type": "O+",
        "city": "Riyadh",
        "hospital": "Central Hospital",
        "units": 2,
        "urgent": True,
    })
    assert request.status_code == 201
    assert request.json()["status"] == "open"

    public_request = client.get("/api/requests")
    assert public_request.status_code == 200
    assert "patient_name" not in public_request.json()[0]
    assert "notes" not in public_request.json()[0]


def test_registration_with_blood_type_creates_donor_profile(client):
    registered = client.post("/api/auth/register", json={
        "full_name": "Amina Donor",
        "email": "amina@example.com",
        "password": "StrongPass123",
        "phone": "0500000001",
        "city": "Riyadh",
        "blood_type": "AB+",
    })
    assert registered.status_code == 201
    login = client.post("/api/auth/login", data={
        "username": "amina@example.com",
        "password": "StrongPass123",
    })
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    profile = client.get("/api/donors/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["blood_type"] == "AB+"


def test_donor_profile_is_null_for_registered_user_without_blood_type(client):
    headers = register_and_login(client)

    profile = client.get("/api/donors/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json() is None


def test_donor_search_by_type_and_city(client):
    headers = register_and_login(client)
    client.post("/api/donors/me", headers=headers, json={"blood_type": "A-"})
    response = client.get("/api/donors?blood_type=A-&city=Riyadh")
    assert response.status_code == 200
    assert len(response.json()) == 1
