import os
import openai
from celery import shared_task
from django.conf import settings

from .models import ScanEvent
from points.services import add_points

openai.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")

# Fixed reward table (pts per category)
POINTS_BY_TYPE = {
    "plastic":   100,
    "metal":     50,
    "glass":     70,
    "paper":     20,
    "unsorted":  20,
}

_PROMPT = (
    "You are an image classifier for recycling. "
    "Return exactly one word from this list: plastic, metal, glass, paper, unsorted."
)

@shared_task
def classify_scan_event(scan_id: int):
    scan = ScanEvent.objects.get(pk=scan_id)

    with open(scan.image.path, "rb") as fp:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _PROMPT},
                {"role": "user",   "content": {"image": fp}},
            ],
        )

    label       = resp.choices[0].message.content.strip().lower()
    confidence  = float(resp.choices[0].message.confidence)

    # Fallback to “unsorted” if label not expected
    label = label if label in POINTS_BY_TYPE else "unsorted"

    scan.trash_type = label
    scan.confidence = confidence
    scan.save(update_fields=["trash_type", "confidence"])

    pts = POINTS_BY_TYPE[label]
    if pts:
        add_points(scan.user_id, pts, related_scan=scan)