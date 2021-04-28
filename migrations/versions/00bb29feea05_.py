"""empty message

Revision ID: 89a6b2ef7470
Revises: 
Create Date: 2021-04-28 23:51:57.023898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a6b2ef7470'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('companyuser', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('dateofstablish', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('facilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('facilitycode', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('location', sa.String(length=120), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('facilitycode')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=False),
    sa.Column('lastname', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('separators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('facility_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['facility_id'], ['facilities.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag')
    )
    op.create_table('user_facilities',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('facility_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['facility_id'], ['facilities.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('separators_inputs_data_fluids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('operatingpressure', sa.Float(), nullable=False),
    sa.Column('operatingtemperature', sa.Float(), nullable=False),
    sa.Column('oildensity', sa.Float(), nullable=False),
    sa.Column('gasdensity', sa.Float(), nullable=False),
    sa.Column('mixturedensity', sa.Float(), nullable=False),
    sa.Column('waterdensity', sa.Float(), nullable=False),
    sa.Column('feedbsw', sa.Float(), nullable=False),
    sa.Column('liquidviscosity', sa.Float(), nullable=False),
    sa.Column('gasviscosity', sa.Float(), nullable=False),
    sa.Column('gasmw', sa.Float(), nullable=False),
    sa.Column('liqmw', sa.Float(), nullable=False),
    sa.Column('gascomprz', sa.Float(), nullable=False),
    sa.Column('kcp', sa.Float(), nullable=False),
    sa.Column('especificheatratio', sa.Float(), nullable=False),
    sa.Column('liquidsurfacetension', sa.Float(), nullable=False),
    sa.Column('liquidvaporpressure', sa.Float(), nullable=False),
    sa.Column('liquidcriticalpressure', sa.Float(), nullable=False),
    sa.Column('standardgasflow', sa.Float(), nullable=False),
    sa.Column('standardliquidflow', sa.Float(), nullable=False),
    sa.Column('actualgasflow', sa.Float(), nullable=False),
    sa.Column('actualliquidflow', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_inputs_data_level_control_valves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('lcvtag', sa.String(length=80), nullable=False),
    sa.Column('lcvcv', sa.Float(), nullable=False),
    sa.Column('lcvdiameter', sa.Float(), nullable=False),
    sa.Column('inletlcvpipingdiameter', sa.Float(), nullable=False),
    sa.Column('outletlcvpipingdiameter', sa.Float(), nullable=False),
    sa.Column('lcvfactorfl', sa.Float(), nullable=False),
    sa.Column('lcvfactorfp', sa.Float(), nullable=False),
    sa.Column('lcvinletpressure', sa.Float(), nullable=False),
    sa.Column('lcvoutletpressure', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_inputs_data_relief_valves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('rvtag', sa.String(length=80), nullable=False),
    sa.Column('rvsetpressure', sa.Float(), nullable=False),
    sa.Column('rvorificearea', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_inputs_data_separators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('internaldiameter', sa.Float(), nullable=False),
    sa.Column('ttlength', sa.Float(), nullable=False),
    sa.Column('highleveltrip', sa.Float(), nullable=False),
    sa.Column('highlevelalarm', sa.Float(), nullable=False),
    sa.Column('normalliquidlevel', sa.Float(), nullable=False),
    sa.Column('lowlevelalarm', sa.Float(), nullable=False),
    sa.Column('inletnozzle', sa.Float(), nullable=False),
    sa.Column('gasoutletnozzle', sa.Float(), nullable=False),
    sa.Column('liquidoutletnozzle', sa.Float(), nullable=False),
    sa.Column('inletdevicetype', sa.String(length=80), nullable=False),
    sa.Column('demistertype', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_gas_and_liquid_areas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('separatorcrosssectionalarearatio', sa.Float(), nullable=False),
    sa.Column('separatorcrosssectionalarea', sa.Float(), nullable=False),
    sa.Column('inletnozzlearea', sa.Float(), nullable=False),
    sa.Column('gasnozzlearea', sa.Float(), nullable=False),
    sa.Column('liquidnozzlearea', sa.Float(), nullable=False),
    sa.Column('highleveltripgasarea', sa.Float(), nullable=False),
    sa.Column('normallevelgasarea', sa.Float(), nullable=False),
    sa.Column('lowlevelgasarea', sa.Float(), nullable=False),
    sa.Column('highleveltripliquidarea', sa.Float(), nullable=False),
    sa.Column('normalleveltriparea', sa.Float(), nullable=False),
    sa.Column('lowleveltripliquidarea', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_gas_nozzle_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('gasnozzlevelocity', sa.Float(), nullable=False),
    sa.Column('gasnozzlemomentum', sa.Float(), nullable=False),
    sa.Column('maximumgasnozzlevelocity', sa.Float(), nullable=False),
    sa.Column('maximumgasnozzlemomentum', sa.Float(), nullable=False),
    sa.Column('maximumgasnozzleflow', sa.Float(), nullable=False),
    sa.Column('statusgasnozzle', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_inlet_nozzle_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('mixtureinletnozzlevelocity', sa.Float(), nullable=False),
    sa.Column('inletnozzlemomentum', sa.Float(), nullable=False),
    sa.Column('maximummixtureinletnozzlevelocity', sa.Float(), nullable=False),
    sa.Column('maximuminletnozzlemomentum', sa.Float(), nullable=False),
    sa.Column('maximumliquidflowinletnozzle', sa.Float(), nullable=False),
    sa.Column('maximumgasflowinletnozzle', sa.Float(), nullable=False),
    sa.Column('statusinletnozzle', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_level_control_valve_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('lcvliquidflowcapacity', sa.Float(), nullable=False),
    sa.Column('levelvalverequiredcv', sa.Float(), nullable=False),
    sa.Column('levelcontrolvalvestatus', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_liquid_nozzle_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('liquidnozzlevelocity', sa.Float(), nullable=False),
    sa.Column('maximumliquidnozzlevelocity', sa.Float(), nullable=False),
    sa.Column('maximumliquidnozzleflow', sa.Float(), nullable=False),
    sa.Column('statusliquidnozzle', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_relief_valve_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('reliefvalvecapacity', sa.Float(), nullable=False),
    sa.Column('reliefvalvecapacitystatus', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_vessel_gas_capacity_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('gasloadfactor', sa.Float(), nullable=False),
    sa.Column('maximumgasflowathhlevel', sa.Float(), nullable=False),
    sa.Column('maximumgasflowatnormallevel', sa.Float(), nullable=False),
    sa.Column('statusgascapacityathighlevel', sa.String(length=80), nullable=False),
    sa.Column('statusgascapacityatnormallevel', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('separators_outputs_vessel_liquid_capacity_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('separator_tag', sa.String(), nullable=False),
    sa.Column('maximumvesselliquidflowcapacityatnormallevel', sa.Float(), nullable=False),
    sa.Column('statusvesselliquidcapacity', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['separator_tag'], ['separators.tag'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('separators_outputs_vessel_liquid_capacity_parameters')
    op.drop_table('separators_outputs_vessel_gas_capacity_parameters')
    op.drop_table('separators_outputs_relief_valve_parameters')
    op.drop_table('separators_outputs_liquid_nozzle_parameters')
    op.drop_table('separators_outputs_level_control_valve_parameters')
    op.drop_table('separators_outputs_inlet_nozzle_parameters')
    op.drop_table('separators_outputs_gas_nozzle_parameters')
    op.drop_table('separators_outputs_gas_and_liquid_areas')
    op.drop_table('separators_inputs_data_separators')
    op.drop_table('separators_inputs_data_relief_valves')
    op.drop_table('separators_inputs_data_level_control_valves')
    op.drop_table('separators_inputs_data_fluids')
    op.drop_table('user_facilities')
    op.drop_table('separators')
    op.drop_table('users')
    op.drop_table('facilities')
    op.drop_table('companies')
    # ### end Alembic commands ###