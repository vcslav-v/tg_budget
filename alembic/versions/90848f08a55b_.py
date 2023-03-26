"""empty message

Revision ID: 90848f08a55b
Revises: 25e297b5fd1b
Create Date: 2023-03-26 15:51:29.933197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90848f08a55b'
down_revision = '25e297b5fd1b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('exchange_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('incomes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users_currencies',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'currency_id')
    )
    op.alter_column('users', 'tg_id',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'tg_id',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_table('users_currencies')
    op.drop_table('incomes')
    op.drop_table('exchange_rates')
    op.drop_table('currencies')
    # ### end Alembic commands ###
