"""add wishlist table and booking coordinates

Revision ID: 5f95a178965d
Revises:
Create Date: 2026-09-02 11:48:13.065764

仅创建 Day17/Day18 新增的 4 张表（travel_bookings / travel_preferences /
travel_todos / travel_wishlists）。不触碰 Day11-Day16 既有表，避免历史漂移。
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f95a178965d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema：仅创建缺失的新表。"""
    # ===== travel_bookings（含 latitude / longitude）=====
    op.create_table(
        'travel_bookings',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('travel_id', sa.BigInteger(), nullable=False),
        sa.Column('booking_type', sa.Enum('HOTEL', 'RESTAURANT', 'FLIGHT', 'TRAIN', 'BUS', 'FERRY', name='bookingtype'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('phone', sa.String(length=30), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('payment_status', sa.Enum('PAID', 'PENDING', 'UNDECIDED', 'CANCELLED', name='paymentstatus'), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('ocr_text', sa.Text(), nullable=True),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # ===== travel_preferences =====
    op.create_table(
        'travel_preferences',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('travel_id', sa.BigInteger(), nullable=False),
        sa.Column('hotel_budget_per_night', sa.Integer(), nullable=True),
        sa.Column('hotel_prompt', sa.Text(), nullable=True),
        sa.Column('food_budget_per_meal', sa.Integer(), nullable=True),
        sa.Column('food_prompt', sa.Text(), nullable=True),
        sa.Column('transport_prompt', sa.Text(), nullable=True),
        sa.Column('local_transport_prompt', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('travel_id'),
    )

    # ===== travel_todos =====
    op.create_table(
        'travel_todos',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('travel_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('day_number', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('TODO', 'DONE', name='todostatus'), nullable=False),
        sa.Column('source', sa.Enum('AI', 'USER', name='todosource'), nullable=False),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # ===== travel_wishlists =====
    op.create_table(
        'travel_wishlists',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('travel_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('category', sa.String(length=30), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_must_visit', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema：仅删除本迁移创建的 4 张表。"""
    op.drop_table('travel_wishlists')
    op.drop_table('travel_todos')
    op.drop_table('travel_preferences')
    op.drop_table('travel_bookings')
