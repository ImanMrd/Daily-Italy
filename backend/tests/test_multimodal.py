def test_grammar_endpoints(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Unauthenticated should fail
    unauth_res = client.get("/api/grammar/lessons")
    assert unauth_res.status_code == 401

    # Authenticated fetch
    res = client.get("/api/grammar/lessons", headers=headers)
    assert res.status_code == 200
    lessons = res.json()
    assert len(lessons) >= 8
    
    # Detail fetch
    first_id = lessons[0]["id"]
    detail_res = client.get(f"/api/grammar/lesson/{first_id}", headers=headers)
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert "rules_markdown" in detail
    assert "tables_json" in detail


def test_reading_endpoints(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    # Fetch list
    res = client.get("/api/readings", headers=headers)
    assert res.status_code == 200
    passages = res.json()
    assert len(passages) >= 3

    # Fetch detail
    passage_id = passages[0]["id"]
    detail_res = client.get(f"/api/readings/{passage_id}", headers=headers)
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert "content_it" in detail
    assert "questions_json" in detail

    # Submit answers
    submit_res = client.post(
        f"/api/readings/{passage_id}/submit",
        headers=headers,
        json={"answers": {"0": "A Trastevere, a Roma", "1": "Passa dalla cassa per fare lo scontrino"}}
    )
    assert submit_res.status_code == 200
    data = submit_res.json()
    assert data["passage_id"] == passage_id
    assert data["xp_awarded"] > 0


def test_writing_endpoints(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    # Fetch prompts
    res = client.get("/api/writing/prompts", headers=headers)
    assert res.status_code == 200
    prompts = res.json()
    assert len(prompts) >= 5

    prompt_id = prompts[0]["id"]

    # Evaluate submission
    eval_res = client.post(
        "/api/writing/evaluate",
        headers=headers,
        json={
            "prompt_id": prompt_id,
            "user_text": "Ciao! Mi chiamo Marco, sono di Roma e nel tempo libero mi piace molto studiare l'italiano e viaggiare."
        }
    )
    assert eval_res.status_code == 200
    data = eval_res.json()
    assert data["is_perfect"] is True
    assert data["similarity_score"] == 100
    assert data["xp_awarded"] == 25
