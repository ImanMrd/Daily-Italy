def test_rbac_admin_enforcement(client, user_token, admin_token):
    # 1. Unauthenticated request -> 401
    res_anon = client.get("/api/admin/overview")
    assert res_anon.status_code == 401

    # 2. Regular user request -> 403 Forbidden
    res_user = client.get(
        "/api/admin/overview",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res_user.status_code == 403
    assert "Admin privileges required" in res_user.json()["detail"]

    # 3. Admin request -> 200 OK
    res_admin = client.get(
        "/api/admin/overview",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res_admin.status_code == 200
    data = res_admin.json()
    assert "total_users" in data
    assert "total_words" in data

    # 4. Admin listing users
    res_users = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res_users.status_code == 200
    assert len(res_users.json()) > 0
