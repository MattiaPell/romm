"""update to 1.8.2

Revision ID: 1.8.2
Revises: 1.8.1
Create Date: 2023-05-09 00:00:19.143526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1.8.2'
down_revision = '1.8.1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("roms") as batch_op:
        batch_op.alter_column('r_slug', type_=sa.String(length=400), existing_type=sa.String(length=100))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("roms") as batch_op:
        batch_op.alter_column('r_slug', type_=sa.String(length=100), existing_type=sa.String(length=400))
    # ### end Alembic commands ###