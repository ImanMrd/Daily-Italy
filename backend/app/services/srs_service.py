from datetime import datetime, timedelta
from backend.app.models.progress import UserProgress

def calculate_sm2(progress: UserProgress, rating: int) -> UserProgress:
    """
    SuperMemo-2 (SM-2) algorithm adapted for vocabulary learning.
    Rating:
      1: Again (Complete blackout / incorrect)
      2: Hard (Correct response with significant difficulty)
      3: Good (Correct response after some hesitation)
      4: Easy (Perfect response immediately)
    """
    now = datetime.utcnow()
    progress.last_reviewed = now

    # Map rating (1-4) to SM-2 quality (0-5)
    # 1 -> 1, 2 -> 3, 3 -> 4, 4 -> 5
    quality_map = {1: 1, 2: 3, 3: 4, 4: 5}
    q = quality_map.get(rating, 3)

    if q < 3:
        # Failed recall
        progress.repetition = 0
        progress.interval_days = 1
        progress.times_incorrect = (progress.times_incorrect or 0) + 1
        progress.mastery_status = "review_needed"
    else:
        # Successful recall
        progress.times_correct = (progress.times_correct or 0) + 1
        if progress.repetition == 0:
            progress.interval_days = 1
        elif progress.repetition == 1:
            progress.interval_days = 4 if rating == 3 else (6 if rating == 4 else 2)
        else:
            factor = progress.ease_factor
            if rating == 4:
                factor *= 1.2
            elif rating == 2:
                factor *= 0.85
            progress.interval_days = max(1, int(progress.interval_days * factor))

        progress.repetition += 1

        # Calculate new ease factor (SM-2 formula)
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        progress.ease_factor = max(
            1.3,
            progress.ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        )

        if progress.repetition >= 4 and progress.interval_days >= 14:
            progress.mastery_status = "mastered"
        else:
            progress.mastery_status = "learning"

    progress.next_review = now + timedelta(days=progress.interval_days)
    return progress
