def test_exercise_check_and_submission(client, user_token):
    # 1. Fetch exercises for Lesson 1
    res = client.get("/api/exercises/lesson/1")
    assert res.status_code == 200
    exercises = res.json()
    assert len(exercises) > 0
    first_ex = exercises[0]

    # 2. Test instant check-answer with correct answer ("abitare")
    res_check_correct = client.post("/api/exercises/check-answer", json={
        "exercise_id": first_ex["id"],
        "user_answer": "abitare"
    })
    assert res_check_correct.status_code == 200
    assert res_check_correct.json()["correct"] is True

    # 3. Test instant check-answer with wrong answer ("amare")
    res_check_wrong = client.post("/api/exercises/check-answer", json={
        "exercise_id": first_ex["id"],
        "user_answer": "amare"
    })
    assert res_check_wrong.status_code == 200
    assert res_check_wrong.json()["correct"] is False
    assert res_check_wrong.json()["correct_answer"] == "abitare"

    # 4. Test submitting full lesson quiz
    submissions = [{"exercise_id": ex["id"], "user_answer": "abitare"} for ex in exercises]
    res_submit = client.post(
        "/api/exercises/submit",
        json={"lesson_id": 1, "submissions": submissions},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res_submit.status_code == 200
    result = res_submit.json()
    assert result["total"] == len(exercises)
    assert result["xp_awarded"] > 0
