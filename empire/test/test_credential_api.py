import copy

import pytest


@pytest.fixture(scope="function")
def base_credential():
    return {
        "credtype": "hash",
        "domain": "the-domain",
        "username": "user",
        "password": "hunter2",
        "host": "host1",
    }


def test_create_credential(client, admin_auth_header, base_credential):
    response = client.post(
        "/api/v2/credentials/", headers=admin_auth_header, json=base_credential
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["credtype"] == "hash"
    assert response.json()["domain"] == "the-domain"
    assert response.json()["username"] == "user"
    assert response.json()["password"] == "hunter2"
    assert response.json()["host"] == "host1"


def test_create_credential_unique_constraint_failure(
    client, admin_auth_header, base_credential
):
    response = client.post(
        "/api/v2/credentials/", headers=admin_auth_header, json=base_credential
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Credential not created. Duplicate detected."


def test_update_credential_not_found(client, admin_auth_header, base_credential):
    response = client.put(
        "/api/v2/credentials/9999", headers=admin_auth_header, json=base_credential
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Credential not found for id 9999"


def test_update_credential_unique_constraint_failure(
    client, admin_auth_header, base_credential
):
    credential_2 = copy.deepcopy(base_credential)
    credential_2["domain"] = "the-domain-2"
    response = client.post(
        "/api/v2/credentials/", headers=admin_auth_header, json=credential_2
    )
    assert response.status_code == 201

    response = client.put(
        "/api/v2/credentials/2", headers=admin_auth_header, json=base_credential
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Credential not updated. Duplicate detected."


def test_update_credential(client, admin_auth_header, base_credential):
    updated_credential = base_credential
    updated_credential["domain"] = "new-domain"
    updated_credential["password"] = "password3"
    response = client.put(
        "/api/v2/credentials/1", headers=admin_auth_header, json=updated_credential
    )

    assert response.status_code == 200
    assert response.json()["domain"] == "new-domain"
    assert response.json()["password"] == "password3"


def test_get_credential_not_found(client, admin_auth_header):
    response = client.get("/api/v2/credentials/9999", headers=admin_auth_header)

    assert response.status_code == 404
    assert response.json()["detail"] == "Credential not found for id 9999"


def test_get_credential(client, admin_auth_header):
    response = client.get("/api/v2/credentials/1", headers=admin_auth_header)

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_credentials(client, admin_auth_header):
    response = client.get("/api/v2/credentials", headers=admin_auth_header)

    assert response.status_code == 200
    assert len(response.json()["records"]) > 0


def test_get_credentials_search(client, admin_auth_header):
    response = client.get("/api/v2/credentials?search=hunt", headers=admin_auth_header)

    assert response.status_code == 200
    assert len(response.json()["records"]) == 1
    assert response.json()["records"][0]["password"] == "hunter2"

    response = client.get(
        "/api/v2/credentials?search=qwerty", headers=admin_auth_header
    )

    assert response.status_code == 200
    assert len(response.json()["records"]) == 0


def test_delete_credential(client, admin_auth_header):
    response = client.delete("/api/v2/credentials/1", headers=admin_auth_header)

    assert response.status_code == 204

    response = client.get("/api/v2/credentials/1", headers=admin_auth_header)

    assert response.status_code == 404
