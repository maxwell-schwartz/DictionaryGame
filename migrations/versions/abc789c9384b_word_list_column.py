"""word list column

Revision ID: abc789c9384b
Revises: 0e33343f56d8
Create Date: 2023-10-09 22:14:55.018601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abc789c9384b'
down_revision = '0e33343f56d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('words', sa.Text(), nullable=True))
        batch_op.alter_column('game_state',
               existing_type=sa.VARCHAR(length=17),
               type_=sa.Enum('WAITING_FOR_PLAYERS', 'WAITING_FOR_WORD', 'WAITING_FOR_DEFS', 'WAITING_FOR_VOTES', 'RESULTS', name='gamestateenum'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('game_state',
               existing_type=sa.Enum('WAITING_FOR_PLAYERS', 'WAITING_FOR_WORD', 'WAITING_FOR_DEFS', 'WAITING_FOR_VOTES', 'RESULTS', name='gamestateenum'),
               type_=sa.VARCHAR(length=17),
               existing_nullable=True)
        batch_op.drop_column('words')

    # ### end Alembic commands ###
