from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.baskets import BasketRepository
from apps.api.app.schemas.products import BasketTypeRead

router = APIRouter()


@router.get("", response_model=list[BasketTypeRead])
def list_basket_types(db: Session = Depends(get_db)) -> list[BasketTypeRead]:
    """List active basket types for the public order form."""

    return BasketRepository(db).list_active()
