from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class PaymentSettingRead(BaseModel):
    """Public active payment settings for manual Pix instructions."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider: str
    pix_key: str
    pix_key_type: str
    recipient_name: str
    recipient_document: str
    bank_name: str
    payment_instructions: str
    pix_copy_paste_hash: str
    qr_code_image_url: HttpUrl | None
    is_active: bool
