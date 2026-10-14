from datetime import datetime
from backend.app.models.progress import UserProgress
from backend.app.services.srs_service import calculate_sm2

def test_srs_supermemo2():
    prog = UserProgress(
        user_id=1,
        word_id=1,
        repetition=0,
        interval_days=1,
        ease_factor=2.5,
        mastery_status="learning"
    )

    # First successful recall (Good - 3)
    prog = calculate_sm2(prog, rating=3)
    assert prog.repetition == 1
    assert prog.interval_days >= 1
    assert prog.mastery_status == "learning"

    # Second successful recall (Easy - 4)
    prog = calculate_sm2(prog, rating=4)
    assert prog.repetition == 2
    assert prog.interval_days > 2

    # Failed recall (Again - 1)
    prog = calculate_sm2(prog, rating=1)
    assert prog.repetition == 0
    assert prog.interval_days == 1
    assert prog.mastery_status == "review_needed"
