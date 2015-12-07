"""Add Full Text Search

Revision ID: 488e3dae5a17
Revises: 34fa673d7905
Create Date: 2015-12-07 10:49:44.124657

"""

# revision identifiers, used by Alembic.
revision = '488e3dae5a17'
down_revision = '34fa673d7905'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    op.drop_table('sections')
    op.add_column('notes', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_notes_search_vector', 'notes', ['search_vector'], unique=False, postgresql_using='gin')
    ### end Alembic commands ###
    sync_trigger(conn, 'notes', 'search_vector', ['title', 'body'])

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_notes_search_vector', table_name='notes')
    op.drop_column('notes', 'search_vector')
    op.create_table('sections',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('notebook_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['notebook_id'], [u'notebooks.id'], name=u'sections_notebook_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'sections_pkey')
    )
    ### end Alembic commands ###
