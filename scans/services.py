from datetime import timedelta
from django.db import transaction

from .models import ScanEvent
from .tasks import classify_scan_event

SCAN_WINDOW = timedelta(minutes=1)


def create_scan_with_photo(*, user_id: int, bin_id: str, image_file) -> ScanEvent:
    """
    Store the raw photo; classification happens asynchronously.
    """
    with transaction.atomic():
        event = ScanEvent.objects.create(
            user_id=user_id,
            bin_id=bin_id,
            image=image_file,
        )
        classify_scan_event.delay(event.id)
    return event