from celery import shared_task
from chat.consumers import save_message  # Import the save_message function


@shared_task
def save_message_task(sender_id, content, room_id):
    """
    Celery task for efficient message persistence.
    This version allows using the same save_message function
    from consumers.py for both background processing and in-sync execution.
    """
    save_message(sender_id, content, room_id)
