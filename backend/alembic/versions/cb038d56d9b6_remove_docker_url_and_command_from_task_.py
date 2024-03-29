"""remove docker_url and command from task, since those are contaiener params

Revision ID: cb038d56d9b6
Revises: 1b76078a6c67
Create Date: 2023-02-28 04:33:12.021952

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cb038d56d9b6'
down_revision = '1b76078a6c67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'docker_url')
    op.drop_column('task', 'command')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('command', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('task', sa.Column('docker_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
