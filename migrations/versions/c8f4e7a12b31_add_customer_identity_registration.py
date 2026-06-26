"""add customer identity registration

Revision ID: c8f4e7a12b31
Revises: 6fb040551fb5
Create Date: 2026-06-26 00:00:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "c8f4e7a12b31"
down_revision: str | None = "6fb040551fb5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SEQUENCE customer_number_seq START WITH 1 INCREMENT BY 1")
    op.execute("CREATE SEQUENCE order_number_seq START WITH 1 INCREMENT BY 1")

    op.add_column("customers", sa.Column("tenant_id", sa.Uuid(), nullable=True))
    op.add_column("customers", sa.Column("customer_number", sa.String(length=32), nullable=True))
    op.add_column("customers", sa.Column("first_name", sa.String(length=120), nullable=True))
    op.add_column("customers", sa.Column("last_name", sa.String(length=120), nullable=True))
    op.add_column("customers", sa.Column("cpf_normalized", sa.String(length=32), nullable=True))
    op.add_column("customers", sa.Column("phone_country_code", sa.String(length=8), nullable=True))
    op.add_column("customers", sa.Column("phone_area_code", sa.String(length=8), nullable=True))
    op.add_column("customers", sa.Column("phone_number", sa.String(length=32), nullable=True))
    op.add_column("customers", sa.Column("phone_e164", sa.String(length=32), nullable=True))
    op.create_index(op.f("ix_customers_tenant_id"), "customers", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_customers_customer_number"), "customers", ["customer_number"], unique=True)
    op.create_index(op.f("ix_customers_cpf_normalized"), "customers", ["cpf_normalized"], unique=False)

    op.add_column("orders", sa.Column("order_number", sa.String(length=32), nullable=True))
    op.add_column("orders", sa.Column("state", sa.String(length=120), nullable=True))
    op.add_column("orders", sa.Column("postal_code", sa.String(length=32), nullable=True))
    op.add_column("orders", sa.Column("country", sa.String(length=120), nullable=True))
    op.create_index(op.f("ix_orders_order_number"), "orders", ["order_number"], unique=True)

    op.execute(
        sa.text(
            """
            UPDATE customers
            SET first_name = NULLIF(split_part(btrim(full_name), ' ', 1), ''),
                last_name = CASE
                    WHEN position(' ' in btrim(full_name)) > 0
                        THEN NULLIF(btrim(substr(btrim(full_name), position(' ' in btrim(full_name)) + 1)), '')
                    ELSE NULL
                END,
                cpf_normalized = NULLIF(regexp_replace(coalesce(cpf, ''), '\\D', '', 'g'), ''),
                email = CASE WHEN email IS NULL THEN NULL ELSE lower(email) END
            """,
        ),
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_orders_order_number"), table_name="orders")
    op.drop_column("orders", "country")
    op.drop_column("orders", "postal_code")
    op.drop_column("orders", "state")
    op.drop_column("orders", "order_number")

    op.drop_index(op.f("ix_customers_cpf_normalized"), table_name="customers")
    op.drop_index(op.f("ix_customers_customer_number"), table_name="customers")
    op.drop_index(op.f("ix_customers_tenant_id"), table_name="customers")
    op.drop_column("customers", "phone_e164")
    op.drop_column("customers", "phone_number")
    op.drop_column("customers", "phone_area_code")
    op.drop_column("customers", "phone_country_code")
    op.drop_column("customers", "cpf_normalized")
    op.drop_column("customers", "last_name")
    op.drop_column("customers", "first_name")
    op.drop_column("customers", "customer_number")
    op.drop_column("customers", "tenant_id")

    op.execute("DROP SEQUENCE order_number_seq")
    op.execute("DROP SEQUENCE customer_number_seq")
