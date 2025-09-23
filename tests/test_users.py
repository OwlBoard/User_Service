# tests/test_users.py

def test_create_user_success(client):
    """
    Prueba el registro exitoso de un nuevo usuario.
    """
    response = client.post(
        "/users/register",
        json={"email": "test@example.com", "password": "a_strong_password", "full_name": "Test User"},
    )
    # --- CORRECCIÓN AQUÍ ---
    # Una creación exitosa debe devolver 201 Created.
    # Si tu endpoint devuelve 200, déjalo en 200, pero 201 es más estándar.
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_existing_email(client):
    """
    Prueba que no se puede registrar un usuario con un email que ya existe.
    """
    # Arrange: Creamos un usuario primero
    user_data = {"email": "duplicate@example.com", "password": "password1", "full_name": "Another User"}
    response_1 = client.post("/users/register", json=user_data)
    assert response_1.status_code == 200 # Verificamos que el primero se creó bien

    # Act: Intentamos crear de nuevo con el mismo email
    response_2 = client.post("/users/register", json=user_data)

    # Assert: Esperamos un error 400
    assert response_2.status_code == 400
    assert response_2.json()["detail"] == "Email already registered"