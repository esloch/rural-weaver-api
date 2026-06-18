from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.products import ProductRepository
from apps.api.app.schemas.products import ProductRead

router = APIRouter()


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[ProductRead]:
    """List active products for public order forms."""

    return ProductRepository(db).list_active()
