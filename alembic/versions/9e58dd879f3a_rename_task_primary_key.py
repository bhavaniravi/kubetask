"""rename task primary key

Revision ID: 9e58dd879f3a
Revises: 
Create Date: 2020-12-29 08:22:34.539282

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '9e58dd879f3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_name', sa.String(), nullable=True),
    sa.Column('schedule_at', sa.String(), nullable=True),
    sa.Column('docker_url', sa.String(), nullable=True),
    sa.Column('command', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('start_at', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Enum('NOT_STARTED', 'STARTED', 'SCHEDULED', 'DEFERRED', 'COMPLETED', 'STOPPED', name='state'), nullable=True),
    sa.Column('priority', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'HIGHEST', name='priority'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_instance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('start_ts', sa.DateTime(), nullable=True),
    sa.Column('end_ts', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Enum('NOT_STARTED', 'STARTED', 'SCHEDULED', 'DEFERRED', 'COMPLETED', 'STOPPED', name='state'), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_instance')
    op.drop_table('task')
    # ### end Alembic commands ###
