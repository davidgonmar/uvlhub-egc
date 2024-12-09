"""empty message

Revision ID: 22295a2a5d13
Revises: 5a20679d5b3f
Create Date: 2024-12-05 12:30:41.908209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22295a2a5d13'
down_revision = '5a20679d5b3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fakenodo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doi', sa.String(length=255), nullable=False),
    sa.Column('dep_metadata', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doi')
    )
    op.create_table('ds_rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['data_set.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'dataset_id', name='unique_user_dataset_rating')
    )
    op.create_table('fm_rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('feature_model_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['feature_model_id'], ['feature_model.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'feature_model_id', name='_user_feature_model_uc')
    )
    with op.batch_alter_table('ds_meta_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_draft_mode', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ds_meta_data', schema=None) as batch_op:
        batch_op.drop_column('is_draft_mode')

    op.drop_table('fm_rating')
    op.drop_table('ds_rating')
    op.drop_table('fakenodo')
    # ### end Alembic commands ###
