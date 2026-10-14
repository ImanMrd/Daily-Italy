import uuid
import pytest

def test_chapters_overview_structure(client):
    uname = f"fresh_learner_{uuid.uuid4().hex[:6]}"
    reg = client.post("/api/auth/register", json={"username": uname, "password": "password123"})
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/api/chapters/overview", headers=headers)
    assert res.status_code == 200
    levels = res.json()
    assert len(levels) == 4
    
    # A1 has 10 chapters
    a1 = next(l for l in levels if l["level"] == "A1")
    assert a1["total_chapters"] == 10
    assert len(a1["chapters"]) == 10
    assert a1["is_unlocked"] is True
    # Chapter 1 of A1 is unlocked by default
    assert a1["chapters"][0]["is_unlocked"] is True
    # Chapter 2 of A1 is locked initially
    assert a1["chapters"][1]["is_unlocked"] is False

    # A2 has 10 chapters
    a2 = next(l for l in levels if l["level"] == "A2")
    assert a2["total_chapters"] == 10
    assert len(a2["chapters"]) == 10

    # B1 has 20 chapters
    b1 = next(l for l in levels if l["level"] == "B1")
    assert b1["total_chapters"] == 20
    assert len(b1["chapters"]) == 20

    # B2 has 20 chapters
    b2 = next(l for l in levels if l["level"] == "B2")
    assert b2["total_chapters"] == 20
    assert len(b2["chapters"]) == 20


def test_chapter_detail_and_part_completion(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Get overview to find chapter 1
    res = client.get("/api/chapters/overview", headers=headers)
    ch1_id = res.json()[0]["chapters"][0]["id"]

    # Fetch detail of chapter 1
    ch_res = client.get(f"/api/chapters/chapter/{ch1_id}", headers=headers)
    assert ch_res.status_code == 200
    data = ch_res.json()
    assert data["chapter_number"] == 1
    assert data["level"] == "A1"
    assert len(data["words"]) > 0
    assert data["grammar_rules"] is not None
    assert data["reading_it"] is not None
    assert data["writing_prompt"] is not None

    # Complete parts: test validation on reading
    fail_reading_empty = client.post(
        f"/api/chapters/chapter/{ch1_id}/complete-part",
        headers=headers,
        json={"part": "reading", "answers": {}}
    )
    assert fail_reading_empty.status_code == 400

    fail_reading_wrong = client.post(
        f"/api/chapters/chapter/{ch1_id}/complete-part",
        headers=headers,
        json={"part": "reading", "answers": {"0": "Sbagliato"}}
    )
    assert fail_reading_wrong.status_code == 400

    # Correct reading submission
    rq_list = data["reading_questions"]
    valid_rq_answers = {str(idx): q["correct_answer"] for idx, q in enumerate(rq_list)}
    pass_reading = client.post(
        f"/api/chapters/chapter/{ch1_id}/complete-part",
        headers=headers,
        json={"part": "reading", "answers": valid_rq_answers}
    )
    assert pass_reading.status_code == 200
    assert pass_reading.json()["reading_done"] is True

    # Test validation on writing: empty or too short fails
    fail_writing_empty = client.post(
        f"/api/chapters/chapter/{ch1_id}/complete-part",
        headers=headers,
        json={"part": "writing", "writing_text": ""}
    )
    assert fail_writing_empty.status_code == 400

    pass_writing = client.post(
        f"/api/chapters/chapter/{ch1_id}/complete-part",
        headers=headers,
        json={"part": "writing", "writing_text": "Ciao, mi chiamo Alex e abito a Roma."}
    )
    assert pass_writing.status_code == 200
    assert pass_writing.json()["writing_done"] is True

    # Complete all parts to finish Chapter 1
    comp_all = client.post(
        f"/api/chapters/chapter/{ch1_id}/complete-part",
        headers=headers,
        json={"part": "all"}
    )
    assert comp_all.status_code == 200
    assert comp_all.json()["chapter_completed"] is True

    # Now Chapter 2 should be unlocked!
    res_after = client.get("/api/chapters/overview", headers=headers)
    a1_chapters = res_after.json()[0]["chapters"]
    assert a1_chapters[1]["is_unlocked"] is True


def test_placement_test_progression(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    # Fetch A2 placement test
    pt_res = client.get("/api/chapters/placement/A2", headers=headers)
    assert pt_res.status_code == 200
    pt_data = pt_res.json()
    assert pt_data["target_level"] == "A2"
    assert pt_data["passing_score"] == 70
    assert len(pt_data["questions"]) == 10

    # Submit failing score (less than 70%)
    fail_sub = client.post(
        "/api/chapters/placement/A2/submit",
        headers=headers,
        json={"answers": {"0": "wrong", "1": "wrong"}}
    )
    assert fail_sub.status_code == 200
    assert fail_sub.json()["passed"] is False
    assert fail_sub.json()["score"] < 70

    # Submit passing score (at least 7/10 = 70%)
    pass_answers = {
        "0": "Buonasera",
        "1": "siamo",
        "2": "ha",
        "3": "lo",
        "4": "Vorrei un caffè",
        "5": "piacciono",
        "6": "vado",
        "7": "a / di"
    }
    pass_sub = client.post(
        "/api/chapters/placement/A2/submit",
        headers=headers,
        json={"answers": pass_answers}
    )
    assert pass_sub.status_code == 200
    res_json = pass_sub.json()
    assert res_json["passed"] is True
    assert res_json["score"] >= 70

    # Verify A2 is now unlocked in overview!
    ov_res = client.get("/api/chapters/overview", headers=headers)
    a2_level = next(l for l in ov_res.json() if l["level"] == "A2")
    assert a2_level["is_unlocked"] is True
    assert a2_level["chapters"][0]["is_unlocked"] is True


def test_unique_username_enforcement(client):
    # Try registering an already taken username (case-insensitive)
    res = client.post(
        "/api/auth/register",
        json={"username": "ADMIN", "password": "password123"}
    )
    assert res.status_code == 400
    assert "already taken" in res.json()["detail"].lower()
