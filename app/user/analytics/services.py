from core.models import StrengthExerciseLog


def get_user_log_analytics(user):
    """
    Calculate and return analytics for the given user's exercise logs.
    """
    logs = StrengthExerciseLog.objects.filter(user=user)

    total_reps = sum(log.reps for log in logs)
    total_sets = sum(log.sets for log in logs)
    total_calories_burned = sum(log.calories_burned for log in logs)

    analytics = {
        'total_reps': total_reps,
        'total_sets': total_sets,
        'total_calories_burned': total_calories_burned,
    }

    return analytics
