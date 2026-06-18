from fastapi import APIRouter

router = APIRouter()


def health_check() -> dict[str, str]:
    """Return API health status."""

    return {"status": "ok"}


router.get("/health")(health_check)
router.head("/health", include_in_schema=False)(health_check)
