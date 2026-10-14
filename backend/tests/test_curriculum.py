def test_public_curriculum_access(client):
    # Visitors can browse stages without logging in
    res = client.get("/api/curriculum/stages")
    assert res.status_code == 200
    stages = res.json()
    assert len(stages) >= 4
    assert stages[0]["level"] == "A1"
    assert len(stages[0]["units"]) > 0

    # Visitors can see unit grammar tips and lessons
    unit1 = stages[0]["units"][0]
    assert "grammar_tip" in unit1
    assert "nouns" in unit1["grammar_tip"].lower()
    lesson1_id = unit1["lessons"][0]["id"]

    # Visitors can inspect lesson details
    res_lesson = client.get(f"/api/curriculum/lesson/{lesson1_id}")
    assert res_lesson.status_code == 200
    lesson_data = res_lesson.json()
    assert lesson_data["word_count"] == 15
    assert len(lesson_data["words"]) == 15
