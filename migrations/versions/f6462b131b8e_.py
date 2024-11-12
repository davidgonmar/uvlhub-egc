"""empty message

Revision ID: f6462b131b8e
Revises: f5fba45b876a
Create Date: 2024-11-12 13:34:28.114646

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f6462b131b8e'
down_revision = 'f5fba45b876a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reset_password_verification_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('orcid_id', sa.String(length=19), nullable=True))
        batch_op.add_column(sa.Column('github_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('google_id', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('is_developer', sa.Boolean(), nullable=False))
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
        batch_op.create_unique_constraint(None, ['google_id'])
        batch_op.create_unique_constraint(None, ['orcid_id'])
        batch_op.create_unique_constraint(None, ['github_id'])

    with op.batch_alter_table('user_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('github', sa.String(length=39), nullable=True))
        batch_op.create_unique_constraint(None, ['orcid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profile', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('github')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
        batch_op.drop_column('is_developer')
        batch_op.drop_column('google_id')
        batch_op.drop_column('github_id')
        batch_op.drop_column('orcid_id')

    op.drop_table('reset_password_verification_token')
    # ### end Alembic commands ###