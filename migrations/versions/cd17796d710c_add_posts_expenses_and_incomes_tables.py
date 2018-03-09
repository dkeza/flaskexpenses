"""add posts expenses and incomes tables

Revision ID: cd17796d710c
Revises: d85a2e42df9e
Create Date: 2018-03-04 22:13:14.302241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd17796d710c'
down_revision = 'd85a2e42df9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expense_timestamp'), 'expense', ['timestamp'], unique=False)
    op.create_table('income',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_income_timestamp'), 'income', ['timestamp'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('income_id', sa.Integer(), nullable=True),
    sa.Column('expense_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], ),
    sa.ForeignKeyConstraint(['income_id'], ['income.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_income_timestamp'), table_name='income')
    op.drop_table('income')
    op.drop_index(op.f('ix_expense_timestamp'), table_name='expense')
    op.drop_table('expense')
    # ### end Alembic commands ###