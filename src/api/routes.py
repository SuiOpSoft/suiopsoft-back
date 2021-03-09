"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Company, User, Facility, Separator, SeparatorInputDataFluid, SeparatorInputDataSeparator, SeparatorInputDataReliefValve,SeparatorInputDataLevelControlValve, SeparatorOutputGasAndLiquidAreas, SeparatorOutputInletNozzleParameters, SeparatorOutputGasNozzleParameters, SeparatorOutputLiquidNozzleParameters, SeparatorOutputVesselGasCapacityParameters, SeparatorOutputVesselLiquidCapacityParameters, SeparatorOutputReliefValveParameters, SeparatorOutputLevelControlValveParameters
from api.utils import generate_sitemap, APIException
from api.calculations.separators.gasAndLiquidAreas import gas_and_liquid_areas_calc
from api.calculations.separators.inletNozzleParameters import inlet_nozzle_parameters_calc
from api.calculations.separators.gasNozzle import gas_nozzle_calc
from api.calculations.separators.liquidNozzle import liquid_nozzle_calc
from api.calculations.separators.vesselGasCapacity import vessel_gas_capacity_calc
from api.calculations.separators.vesselLiquidCapacity import vessel_liquid_capacity_calc
from api.calculations.separators.reliefValve import relief_valve_calc
from api.calculations.separators.levelControlValve import level_control_calc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Creación de token
@api.route("/signIn", methods=["POST"])
def sign_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong email or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user.serialize())
    return jsonify(access_token=access_token)

# Rellenar tabla de companies
@api.route('/seedData', methods=['GET'])
def handle_data():

    company1 = Company(id="1", name="Shell", dateofstablish="1968", description="Petroleum Company", address="Holland")
    user1 = User(id="1", firstname="SuiOp", lastname="Soft", email="fran@gmail.com", password="suiop12345", company_id="1")
    facility1 = Facility(id="1", name="PDO Camp", location="Oman", company_id="1", user_id="1")
    separator1 = Separator(tag="v-3108", description="Separator V", facility_id="1")
    separatorDataFluid1 = SeparatorInputDataFluid(separator_tag="v-3108", operatingpressure="5536.33", operatingtemperature="37", oildensity="794.08", gasdensity="52.18", mixturedensity="197.76", waterdensity="1001", feedbsw="0.1", 
                                                    liquidviscosity="2.1065", gasviscosity="0.013385", gasmw="20.80", liqmw="155.53", gascomprz="0.8558", especificheatratio="1.4913", liquidsurfacetension="15.49", liquidvaporpressure="5536.3",
                                                    liquidcriticalpressure="12541.9", standardgasflow="25835.9", standardliquidflow="103.9", actualgasflow="435.5", actualliquidflow="106.33", kcp="1.49")
    
    separatorLevelControlValve1 = SeparatorInputDataLevelControlValve(separator_tag="v-3108", lcvtag="5536.33", lcvcv="5536.33", 
                                                    lcvdiameter="5536.33", inletlcvpipingdiameter="5536.33", outletlcvpipingdiameter="5536.33", lcvfactorfl="5536.33", lcvfactorfi="5536.33", 
                                                    lcvfactorfp="5536.33", lcvinletpressure="5536.33", lcvoutletpressure="5536.33")

    separatorDataReliefValve1 = SeparatorInputDataReliefValve(separator_tag="v-3108", rvtag="5536.33", rvsetpressure="5536.33", 
                                                    rvorificearea="5536.33")

    separatorInputSeparators1 = SeparatorInputDataSeparator(separator_tag="v-3108", internaldiameter="5536.33", ttlength="5536.33", 
                                                    highleveltrip="5536.33", highlevelalarm="5536.33", normalliquidlevel="5536.33", lowlevelalarm="5536.33", inletnozzle="5536.33", 
                                                    gasoutletnozzle="5536.33", liquidoutletnozzle="5536.33", inletdevicetype="5536.33", demistertype="5536.33")

    db.session.add(company1)
    db.session.add(user1)
    db.session.add(facility1)
    db.session.add(separator1)
    db.session.add(separatorDataFluid1)          
    db.session.add(separatorLevelControlValve1)
    db.session.add(separatorDataReliefValve1)
    db.session.add(separatorInputSeparators1)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200
## Companies resources ##
# Seleccionar todas las compañias
@api.route('/companies', methods=['GET'])
def handle_get_companies():

    companies_query = Company.query.all()
    all_companies = list(map(lambda x: x.serialize(), companies_query))
    return jsonify(all_companies), 200

# Seleccionar una compañia por name
@api.route('/companies/<string:company_name>', methods=['GET'])
def handle_get_company(company_name):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(name=company_name)
    company = list(map(lambda x: x.serialize(), company_query))
    return jsonify(company), 200

## Users resources ##
# Seleccionar usuarios
@api.route('/users', methods=['GET'])
def handle_get_users():

    users_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users_query))
    return jsonify(all_users), 200

# Seleccionar un usuario por email
@api.route('/users/<string:user_email>', methods=['GET'])
def handle_get_user_by_email(user_email):

    #  user1 = Company.query.get(company_id)
    user_query = User.query.filter_by(email=user_email)
    user = list(map(lambda x: x.serialize(), user_query))
    return jsonify(user), 200

# Seleccionar usuarios por compañia
@api.route('/users/<int:company_id>', methods=['GET'])
def handle_get_user_by_company_id(company_id):

    #  user1 = Company.query.get(company_id)
    user_query = User.query.filter_by(company_id=company_id)
    user = list(map(lambda x: x.serialize(), user_query))
    return jsonify(user), 200

## Separators resources ##
# Seleccionar separadores
@api.route('/separators', methods=['GET'])
def handle_get_separators():

    separator_query = Separator.query.all()
    all_separators = list(map(lambda x: x.serialize(), separator_query))
    return jsonify(all_separators), 200

# Insertar separador
@api.route('/separators', methods=['POST'])
def handle_insert_separator():
    separator = request.get_json()
    print(separator)

    ## Separator params
    separator_tag = separator["tag"]
    facility_id = separator["facility_id"] ## Falta coger la facility del front (Escogerla en la pantalla del usuario)

    ## Cración del separador en la tabla separators
    separator = Separator(tag=separator_tag, facility_id=facility_id)

    ## Inputs 
    separatorDataFluid = SeparatorInputDataFluid(separator_tag=separator_tag, operatingpressure="-", operatingtemperature="-", 
                                                    oildensity="-", gasdensity="-", mixturedensity="-", waterdensity="-", feedbsw="-", 
                                                    liquidviscosity="-", gasviscosity="-", gasmw="-", liqmw="-", gascomprz="-", especificheatratio="-", 
                                                    liquidsurfacetension="-", liquidvaporpressure="-", liquidcriticalpressure="-", standardgasflow="-", 
                                                    standardliquidflow="-", actualgasflow="-", actualliquidflow="-", kcp="-")

    separatorLevelControlValve = SeparatorInputDataLevelControlValve(separator_tag=separator_tag, lcvtag="-", lcvcv="-", 
                                                    lcvdiameter="-", inletlcvpipingdiameter="-", outletlcvpipingdiameter="-", lcvfactorfl="-", lcvfactorfi="-", 
                                                    lcvfactorfp="-", lcvinletpressure="-", lcvoutletpressure="-")

    separatorDataReliefValve = SeparatorInputDataReliefValve(separator_tag=separator_tag, rvtag="-", rvsetpressure="-", 
                                                    rvorificearea="-")
    
    separatorInputSeparators = SeparatorInputDataSeparator(separator_tag=separator_tag, internaldiameter="-", ttlength="-", 
                                                    highleveltrip="-", highlevelalarm="-", normalliquidlevel="-", lowlevelalarm="-", inletnozzle="-", 
                                                    gasoutletnozzle="-", liquidoutletnozzle="-", inletdevicetype="-", demistertype="-")


    db.session.add(separator)
    db.session.add(separatorDataFluid)
    db.session.add(separatorLevelControlValve)
    db.session.add(separatorDataReliefValve)
    db.session.add(separatorInputSeparators)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


## Inputs resources ##
# Seleccionar inputs data fluids
@api.route('/datafluids', methods=['GET'])
def handle_get_data_fluids():

    data_fluids_query = SeparatorInputDataFluid.query.all()
    all_data_fluids = list(map(lambda x: x.serialize(), data_fluids_query))
    return jsonify(all_data_fluids), 200

# Insertar datos en  tabla data fluids
@api.route('/datafluids', methods=['POST'])
def handle_insert_data_fluids():
    datafluids = request.get_json()

    id = datafluids["id"]
    separator_id = datafluids["separator_id"]
    operatingpressure = datafluids["operatingpressure"]
    operatingtemperature = datafluids["operatingtemperature"]
    oildensity = datafluids["oildensity"]
    gasdensity = datafluids["gasdensity"]
    mixturedensity = datafluids["mixturedensity"]
    waterdensity = datafluids["waterdensity"]
    feedbsw = datafluids["feedbsw"]
    liquidviscosity = datafluids["liquidviscosity"]
    gasviscosity = datafluids["gasviscosity"]
    gasmw = datafluids["gasmw"]
    liqmw = datafluids["liqmw"]
    gascomprz = datafluids["gascomprz"]
    especificheatratio = datafluids["especificheatratio"]
    liquidsurfacetension = datafluids["liquidsurfacetension"]
    liquidvaporpressure = datafluids["liquidvaporpressure"]
    liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    standardgasflow = datafluids["standardgasflow"]
    standardliquidflow = datafluids["standardliquidflow"]
    actualgasflow = datafluids["actualgasflow"]
    actualliquidflow = datafluids["actualliquidflow"]

    separatorDataFluid = SeparatorInputDataFluid(id=id, separator_id=separator_id, operatingpressure=operatingpressure, operatingtemperature=operatingtemperature, 
                                                    oildensity=oildensity, gasdensity=gasdensity, mixturedensity=mixturedensity, waterdensity=waterdensity, feedbsw=feedbsw, 
                                                    liquidviscosity=liquidviscosity, gasviscosity=gasviscosity, gasmw=gasmw, liqmw=liqmw, gascomprz=gascomprz, especificheatratio=especificheatratio, 
                                                    liquidsurfacetension=liquidsurfacetension, liquidvaporpressure=liquidvaporpressure, liquidcriticalpressure=liquidcriticalpressure, standardgasflow=standardgasflow, 
                                                    standardliquidflow=standardliquidflow, actualgasflow=actualgasflow, actualliquidflow=actualliquidflow)

    db.session.add(separatorDataFluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar datos en tabla datafluids
@api.route('/datafluids', methods=['PUT'])
def handle_update_data_fluids():
    datafluids = request.get_json()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datafluids["separator_tag"]).first()

    datafluid.separator_tag = datafluids["separator_tag"]
    datafluid.operatingpressure = datafluids["operatingpressure"]
    datafluid.operatingtemperature = datafluids["operatingtemperature"]
    datafluid.oildensity = datafluids["oildensity"]
    datafluid.gasdensity = datafluids["gasdensity"]
    datafluid.mixturedensity = datafluids["mixturedensity"]
    datafluid.waterdensity = datafluids["waterdensity"]
    datafluid.feedbsw = datafluids["feedbsw"]
    datafluid.liquidviscosity = datafluids["liquidviscosity"]
    datafluid.gasviscosity = datafluids["gasviscosity"]
    datafluid.gasmw = datafluids["gasmw"]
    datafluid.liqmw = datafluids["liqmw"]
    datafluid.gascomprz = datafluids["gascomprz"]
    datafluid.especificheatratio = datafluids["especificheatratio"]
    datafluid.liquidsurfacetension = datafluids["liquidsurfacetension"]
    datafluid.liquidvaporpressure = datafluids["liquidvaporpressure"]
    datafluid.liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    datafluid.standardgasflow = datafluids["standardgasflow"]
    datafluid.standardliquidflow = datafluids["standardliquidflow"]
    datafluid.actualgasflow = datafluids["actualgasflow"]
    datafluid.actualliquidflow = datafluids["actualliquidflow"]

    db.session.add(datafluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Eliminar datos en tabla datafluids
@api.route('/datafluids', methods=['DELETE'])
def handle_delete_data_fluids():
    datafluids = request.get_json()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datafluids["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = datafluids["separator_tag"]).first()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datafluids["separator_tag"]).first()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datafluids["separator_tag"]).first()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = datafluids["separator_tag"]).first()

    datafluid.separator_tag = datafluids["separator_tag"]
    dataseparator.separator_tag = datafluids["separator_tag"]
    datalevelcontrolvalve.separator_tag = datafluids["separator_tag"]
    datareliefvalve.separator_tag = datafluids["separator_tag"]
    separator.tag = datafluids["separator_tag"]

    db.session.delete(datafluid)
    db.session.delete(dataseparator)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(datareliefvalve)
    db.session.delete(separator)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar inputs data fluids
@api.route('/dataseparators', methods=['GET'])
def handle_get_data_separators():

    data_separators_query = SeparatorInputDataSeparator.query.all()
    all_data_separators = list(map(lambda x: x.serialize(), data_separators_query))
    return jsonify(all_data_separators), 200

# Insertar datos en  tabla data separators
@api.route('/dataseparators', methods=['POST'])
def handle_insert_data_separators():
    dataseparators = request.get_json()

    id = dataseparators["id"]
    separator_id = dataseparators["separator_id"]
    internaldiameter = dataseparators["internaldiameter"]
    ttlength = dataseparators["ttlength"]
    highleveltrip = dataseparators["highleveltrip"]
    highlevelalarm = dataseparators["highlevelalarm"]
    normalliquidlevel = dataseparators["normalliquidlevel"]
    lowlevelalarm = dataseparators["lowlevelalarm"]
    inletnozzle = dataseparators["inletnozzle"]
    gasoutletnozzle = dataseparators["gasoutletnozzle"]
    liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    inletdevicetype = dataseparators["inletdevicetype"]
    demistertype = dataseparators["demistertype"]


    separatorInputSeparators = SeparatorInputDataSeparator(id=id, separator_id=separator_id, internaldiameter=internaldiameter, ttlength=ttlength, 
                                                    highleveltrip=highleveltrip, highlevelalarm=highlevelalarm, normalliquidlevel=normalliquidlevel, lowlevelalarm=lowlevelalarm, inletnozzle=inletnozzle, 
                                                    gasoutletnozzle=gasoutletnozzle, liquidoutletnozzle=liquidoutletnozzle, inletdevicetype=inletdevicetype, demistertype=demistertype)

    db.session.add(separatorInputSeparators)
    db.session.commit()
    

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar datos en  tabla data separators
@api.route('/dataseparators', methods=['PUT'])
def handle_update_data_separators():
    dataseparators = request.get_json()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()

    dataseparator.separator_tag = dataseparators["separator_tag"]
    dataseparator.internaldiameter = dataseparators["internaldiameter"]
    dataseparator.ttlength = dataseparators["ttlength"]
    dataseparator.highleveltrip = dataseparators["highleveltrip"]
    dataseparator.highlevelalarm = dataseparators["highlevelalarm"]
    dataseparator.normalliquidlevel = dataseparators["normalliquidlevel"]
    dataseparator.lowlevelalarm = dataseparators["lowlevelalarm"]
    dataseparator.inletnozzle = dataseparators["inletnozzle"]
    dataseparator.gasoutletnozzle = dataseparators["gasoutletnozzle"]
    dataseparator.liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    dataseparator.inletdevicetype = dataseparators["inletdevicetype"]
    dataseparator.demistertype = dataseparators["demistertype"]


    # separatorInputSeparators = SeparatorInputDataSeparator(id=id, separator_id=separator_id, internaldiameter=internaldiameter, ttlength=ttlength, 
    #                                                 highleveltrip=highleveltrip, highlevelalarm=highlevelalarm, normalliquidlevel=normalliquidlevel, lowlevelalarm=lowlevelalarm, inletnozzle=inletnozzle, 
    #                                                 gasoutletnozzle=gasoutletnozzle, liquidoutletnozzle=liquidoutletnozzle, inletdevicetype=inletdevicetype, demistertype=demistertype)

    db.session.add(dataseparator)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Eliminar datos en tabla datafluids
@api.route('/dataseparators', methods=['DELETE'])
def handle_delete_data_separators():
    dataseparators = request.get_json()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = dataseparators["separator_tag"]).first()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()

    dataseparator.separator_tag = dataseparators["separator_tag"]
    datafluid.separator_tag = dataseparators["separator_tag"]
    datalevelcontrolvalve.separator_tag = dataseparators["separator_tag"]
    datareliefvalve.separator_tag = dataseparators["separator_tag"]
    separator.tag = dataseparators["separator_tag"]

    db.session.delete(dataseparator)
    db.session.delete(datafluid)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(datareliefvalve)
    db.session.delete(separator)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200    

# Seleccionar inputs data fluids
@api.route('/datareliefvalve', methods=['GET'])
def handle_get_data_relief_valve():

    data_reliefvalve_query = SeparatorInputDataReliefValve.query.all()
    all_data_reliefvalve = list(map(lambda x: x.serialize(), data_reliefvalve_query))
    return jsonify(all_data_reliefvalve), 200

# Insertar datos en  tabla data relief valve
@api.route('/datareliefvalve', methods=['POST'])
def handle_insert_data_relief_valve():
    datareliefvalves = request.get_json()

    id = datareliefvalves["id"]
    separator_id = datareliefvalves["separator_id"]
    rvtag = datareliefvalves["rvtag"]
    rvsetpressure = datareliefvalves["rvsetpressure"]
    rvorificearea = datareliefvalves["rvorificearea"]


    separatorReliefValve = SeparatorInputDataReliefValve(id=id, separator_id=separator_id, rvtag=rvtag, rvsetpressure=rvsetpressure, 
                                                    rvorificearea=rvorificearea)

    db.session.add(separatorReliefValve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar datos en  tabla data relief valve
@api.route('/datareliefvalve', methods=['PUT'])
def handle_update_data_relief_valve():
    datareliefvalves = request.get_json()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()

    datareliefvalve.separator_tag = datareliefvalves["separator_tag"]
    datareliefvalve.rvtag = datareliefvalves["rvtag"]
    datareliefvalve.rvsetpressure = datareliefvalves["rvsetpressure"]
    datareliefvalve.rvorificearea = datareliefvalves["rvorificearea"]


    # separatorReliefValve = SeparatorInputDataReliefValve(id=id, separator_id=separator_id, rvtag=rvtag, rvsetpressure=rvsetpressure, 
    #                                                 rvorificearea=rvorificearea)
    db.session.add(datareliefvalve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

@api.route('/datareliefvalve', methods=['DELETE'])
def handle_delete_data_relief_valve():
    datareliefvalves = request.get_json()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = datareliefvalves["separator_tag"]).first()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()

    separator.tag = datareliefvalves["separator_tag"]
    datareliefvalve.separator_tag = datareliefvalves["separator_tag"]
    datalevelcontrolvalve.separator_tag = datareliefvalves["separator_tag"]
    datafluid.separator_tag = datareliefvalves["separator_tag"]
    dataseparator.separator_tag = datareliefvalves["separator_tag"]
    

    db.session.delete(datareliefvalve)
    db.session.delete(datafluid)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(dataseparator)
    db.session.delete(separator)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar inputs data fluids
@api.route('/datalevelcontrolvalve', methods=['GET'])
def handle_get_data_level_control_valve():

    data_levelcontrolvalve_query = SeparatorInputDataLevelControlValve.query.all()
    all_data_levelcontrolvalve = list(map(lambda x: x.serialize(), data_levelcontrolvalve_query))
    return jsonify(all_data_levelcontrolvalve), 200

# Insertar datos en  tabla data level control valve
@api.route('/datalevelcontrolvalve', methods=['POST'])
def handle_insert_data_level_control_valve():
    datalevelcontrolvalves = request.get_json()

    id = datalevelcontrolvalves["id"]
    separator_id = datalevelcontrolvalves["separator_id"]
    lcvtag = datalevelcontrolvalves["lcvtag"]
    lcvcv = datalevelcontrolvalves["lcvcv"]
    lcvdiameter = datalevelcontrolvalves["lcvdiameter"]
    inletlcvpipingdiameter = datalevelcontrolvalves["inletlcvpipingdiameter"]
    outletlcvpipingdiameter = datalevelcontrolvalves["outletlcvpipingdiameter"]
    lcvfactorfl = datalevelcontrolvalves["lcvfactorfl"]
    lcvfactorfi = datalevelcontrolvalves["lcvfactorfi"]
    lcvfactorfp = datalevelcontrolvalves["lcvfactorfp"]
    lcvinletpressure = datalevelcontrolvalves["lcvinletpressure"]
    lcvoutletpressure = datalevelcontrolvalves["lcvoutletpressure"]


    separatorLevelControlValve = SeparatorInputDataLevelControlValve(id=id, separator_id=separator_id, lcvtag=lcvtag, lcvcv=lcvcv, 
                                                    lcvdiameter=lcvdiameter, inletlcvpipingdiameter=inletlcvpipingdiameter, outletlcvpipingdiameter=outletlcvpipingdiameter, lcvfactorfl=lcvfactorfl, lcvfactorfi=lcvfactorfi, 
                                                    lcvfactorfp=lcvfactorfp, lcvinletpressure=lcvinletpressure, lcvoutletpressure=lcvoutletpressure)

    db.session.add(separatorLevelControlValve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Insertar datos en  tabla data level control valve
@api.route('/datalevelcontrolvalve', methods=['PUT'])
def handle_update_data_level_control_valve():
    datalevelcontrolvalves = request.get_json()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    
    datalevelcontrolvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    datalevelcontrolvalve.lcvtag = datalevelcontrolvalves["lcvtag"]
    datalevelcontrolvalve.lcvcv = datalevelcontrolvalves["lcvcv"]
    #datalevelcontrolvalve.lcvdiameter = datalevelcontrolvalves["lcvdiameter"]
    #datalevelcontrolvalve.inletlcvpipingdiameter = datalevelcontrolvalves["inletlcvpipingdiameter"]
    #datalevelcontrolvalve.outletlcvpipingdiameter = datalevelcontrolvalves["outletlcvpipingdiameter"]
    datalevelcontrolvalve.lcvfactorfl = datalevelcontrolvalves["lcvfactorfl"]
    datalevelcontrolvalve.lcvfactorfi = datalevelcontrolvalves["lcvfactorfi"]
    datalevelcontrolvalve.lcvfactorfp = datalevelcontrolvalves["lcvfactorfp"]
    datalevelcontrolvalve.lcvinletpressure = datalevelcontrolvalves["lcvinletpressure"]
    datalevelcontrolvalve.lcvoutletpressure = datalevelcontrolvalves["lcvoutletpressure"]

    db.session.add(datalevelcontrolvalve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Eliminar datos en tabla datafluids
@api.route('/datalevelcontrolvalve', methods=['DELETE'])
def handle_delete_data_level_control_valve():
    datalevelcontrolvalves = request.get_json()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = datalevelcontrolvalves["separator_tag"]).first()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()

    separator.tag = datalevelcontrolvalves["separator_tag"]
    datalevelcontrolvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    datafluid.separator_tag = datalevelcontrolvalves["separator_tag"]
    datareliefvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    dataseparator.separator_tag = datalevelcontrolvalves["separator_tag"]
    

    db.session.delete(datafluid)
    db.session.delete(dataseparator)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(datareliefvalve)
    db.session.delete(separator)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


# Seleccionar separadores por usuario
# Seleccionar inputs de separadores por usuario
# Seleccionar outputs de separadores por usuario

## Outputs resources ##
## Calcular SeparatorOutputGasAndLiquidAreas
@api.route('/gasandliquidareascalc', methods=['POST'])
def handle_calc_gas_liquid_areas():

    gas_and_liquid_areas_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


# Seleccionar SeparatorOutputGasAndLiquidAreas
@api.route('/gasandliquidareascalc', methods=['GET'])
def handle_get_gas_liquid_areas():

    gas_liquid_query = SeparatorOutputGasAndLiquidAreas.query.all()
    all_gas_liquid = list(map(lambda x: x.serialize(), gas_liquid_query))
    return jsonify(all_gas_liquid), 200


## Calcular SeparatorOutputInletNozzleParameters
@api.route('/inletnozzleparameterscalc', methods=['POST'])
def handle_calc_inlet_nozzle_parameters():

    inlet_nozzle_parameters_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputInletNozzleParameters
@api.route('/inletnozzleparameterscalc', methods=['GET'])
def handle_get_inlet_nozzle_parameters():

    inlet_nozzle_query = SeparatorOutputInletNozzleParameters.query.all()
    all_inlet_nozzle = list(map(lambda x: x.serialize(), inlet_nozzle_query))
    return jsonify(all_inlet_nozzle), 200

## Calcular SeparatorOutputGasNozzleParameters
@api.route('/gasnozzleparameterscalc', methods=['POST'])
def handle_calc_gas_nozzle_parameters():

    gas_nozzle_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputGasNozzleParameters
@api.route('/gasnozzleparameterscalc', methods=['GET'])
def handle_get_gas_nozzle_parameters():

    gas_nozzle_query = SeparatorOutputGasNozzleParameters.query.all()
    all_gas_nozzle = list(map(lambda x: x.serialize(), gas_nozzle_query))
    return jsonify(all_gas_nozzle), 200

## Calcular SeparatorOutputLiquidNozzleParameters
@api.route('/liquidnozzleparameterscalc', methods=['POST'])
def handle_calc_liquid_nozzle_parameters():

    liquid_nozzle_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputLiquidNozzleParameters
@api.route('/liquidnozzleparameterscalc', methods=['GET'])
def handle_get_liquid_nozzle_parameters():

    liquid_nozzle_query = SeparatorOutputLiquidNozzleParameters.query.all()
    all_liquid_nozzle = list(map(lambda x: x.serialize(), liquid_nozzle_query))
    return jsonify(all_liquid_nozzle), 200

## Calcular SeparatorOutputVesselGasCapacityParameters
@api.route('/vesselgascapacitycalc', methods=['POST'])
def handle_calc_vessel_gas_parameters():

    vessel_gas_capacity_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputVesselGasCapacityParameters
@api.route('/vesselgascapacitycalc', methods=['GET'])
def handle_get_vessel_gas_parameters():

    vessel_gas_query = SeparatorOutputVesselGasCapacityParameters.query.all()
    all_vessel_gas = list(map(lambda x: x.serialize(), vessel_gas_query))
    return jsonify(all_vessel_gas), 200

## Calcular SeparatorOutputVesselLiquidCapacityParameters
@api.route('/vesselliquidcapacitycalc', methods=['POST'])
def handle_calc_vessel_liquid_parameters():

    vessel_liquid_capacity_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputVesselLiquidCapacityParameters
@api.route('/vesselliquidcapacitycalc', methods=['GET'])
def handle_get_vessel_liquid_parameters():

    vessel_liquid_query = SeparatorOutputVesselLiquidCapacityParameters.query.all()
    all_vessel_liquid = list(map(lambda x: x.serialize(), vessel_liquid_query))
    return jsonify(all_vessel_liquid), 200

## Calcular SeparatorOutputReliefValveParameters
@api.route('/reliefvalvecalc', methods=['POST'])
def handle_calc_relief_valve_parameters():

    relief_valve_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputReliefValveParameters
@api.route('/reliefvalvecalc', methods=['GET'])
def handle_get_relief_valve_parameters():

    relief_valve_query = SeparatorOutputReliefValveParameters.query.all()
    all_relief_valves = list(map(lambda x: x.serialize(), relief_valve_query))
    return jsonify(all_relief_valves), 200

## Calcular SeparatorOutputReliefValveParameters
@api.route('/levelcontrolcalc', methods=['POST'])
def handle_calc_level_control_valve_parameters():

    level_control_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputReliefValveParameters
@api.route('/levelcontrolcalc', methods=['GET'])
def handle_get_level_control_valve_parameters():

    level_control_valve_query = SeparatorOutputLevelControlValveParameters.query.all()
    all_level_control_valves = list(map(lambda x: x.serialize(), level_control_valve_query))
    return jsonify(all_level_control_valves), 200


