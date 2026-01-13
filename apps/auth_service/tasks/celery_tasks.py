"""
Celery tasks for auth service (e.g., sending emails, background jobs).
"""
# Example: Email sending task
# from celery import Celery
# from core.config import settings

# celery_app = Celery(
#     "auth_service",
#     broker=settings.CELERY_BROKER_URL,
#     backend=settings.CELERY_RESULT_BACKEND
# )

# @celery_app.task
# def send_verification_email(user_email: str, token: str):
#     """Send verification email to user."""
#     # Implementation here
#     pass
