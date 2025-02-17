from src import UtilEnviroment
from src import Datacatalog
from src import ConfigManager
from src import AreaLocation
from src import EgenskapStrategy
from src import KommuneStrategy
from src import FylkeStrategy
from src import VegrefStrategy
from src import ConsultManager
from src import EgenskapUriGenerator
from src import KommuneUriGenerator
from src import FylkeUriGenerator
from src import VegrefUriGenerator

import pytest

@pytest.fixture
def util_instance():
    return UtilEnviroment('test')

@pytest.fixture
def catalog_instance():
    return Datacatalog()

@pytest.fixture
def config_manager():
    return ConfigManager()

@pytest.fixture
def area_instance():
    return AreaLocation()

@pytest.fixture
def egenskape_strategy():
    return EgenskapStrategy()

@pytest.fixture
def kommune_strategy():
    return KommuneStrategy()

@pytest.fixture
def fylke_strategy():
    return FylkeStrategy()

@pytest.fixture
def vegref_strategy():
    return VegrefStrategy()

@pytest.fixture
def consult_instance():
    return ConsultManager()

@pytest.fixture
def egenskap_uri_inst():
    return EgenskapUriGenerator()

@pytest.fixture
def kommune_uri_inst():
    return KommuneUriGenerator()

@pytest.fixture
def fylke_uri_inst():
    return FylkeUriGenerator()

@pytest.fixture
def vegref_uri_inst():
    return VegrefUriGenerator()

def test_util_enviroment(util_instance):

    # print( util_instance.env )
    assert util_instance.env != ''

def test_config_manager(config_manager):

    #greater o equal to version when test was created version
    assert config_manager.load_config().get('catalog_version') >= 2.39

    assert config_manager.load_config().get('catalog_path') == 'resources/datacatalog.json'

    assert config_manager.load_config().get('test_headers') == {"X-Client": "STDTest-Client"}

    assert config_manager.load_config().get('endpoints') == {
        "prod": "https://nvdbapiles-v3.atlas.vegvesen.no/",
        "test": "https://nvdbapiles-v3.test.atlas.vegvesen.no/"
    }

def test_catalog_download_to_file_and_resources(catalog_instance, config_manager):

    assert catalog_instance.download_to_file(config_manager.load_config().get('catalog_path')) == True
    assert catalog_instance.isDataCatalogResources() == True

def test_check_catalog_version(catalog_instance):

    assert catalog_instance.check_version() == True

def test_get_catalog_records(catalog_instance):
    
    records = catalog_instance.records()

    #at leas 400 and up egenskaper typer
    assert len( records ) >= 400

    assert records[1]['name'] == 'Skjerm'
    assert records[2]['name'] == 'Rekkverk'
    assert records[3]['name'] == 'Gjerde'
    assert records[4]['name'] == 'Kantstein'
    assert records[5]['name'] == 'Nedsenka kantstein'

def test_get_catalog_specific_record(catalog_instance):
    
    assert catalog_instance.especific_record(type_name='Veganlegg')['id'] == 30

def test_area_download_and_resources(area_instance):

    assert area_instance.download_area() == True
    assert area_instance.isAreaResources() == True

def test_area_communities(area_instance):

    assert len( area_instance.communities() ) > 30

def test_area_counties(area_instance):

    assert len( area_instance.counties() ) > 10

def test_area_community_code(area_instance):
    
    assert area_instance.community_code('Haugesund') == 1106 #haugesund
    assert area_instance.community_code('Karmøy') == 1149 #Karmøy
    assert area_instance.community_code('Stavanger') == 1103 #Stavanger

def test_area_comunity_name(area_instance):

    assert area_instance.community_name(1106) == 'Haugesund'
    assert area_instance.community_name(1149) == 'Karmøy'
    assert area_instance.community_name(1103) == 'Stavanger'

def test_area_county_code(area_instance):
    
    assert area_instance.county_code('Rogaland') == 11 #rogaland
    assert area_instance.county_code('Vestland') == 46 #vestland
    assert area_instance.county_code('Møre og Romsdal') == 15 #Møre og Romsdal

def test_area_county_name(area_instance):

    assert area_instance.county_name(11) == 'Rogaland'
    assert area_instance.county_name(46) == 'Vestland'
    assert area_instance.county_name(15) == 'Møre og Romsdal'

def test_egenskap_strategy(egenskape_strategy):

    egenskape_strategy.set_roadobject_type( 470 )

    egenskape_strategy.filter( {'egenskap': 'Type = Radio'} )
    egenskape_strategy.filter( {'egenskap': 'DSRC avlesing != ITS'} )
    egenskape_strategy.filter( {'egenskap': 'Høyde < 0.34'} )
    egenskape_strategy.filter( {'egenskap': 'Etableringsår > 1997'} )

    list_egenkspa = egenskape_strategy.query()

    assert list_egenkspa[1] == {'id': 3779, 'value': 4822, 'operator': '='}
    assert list_egenkspa[2] == {'id': 13072, 'value': 22693, 'operator': '!='}
    assert list_egenkspa[3] == {'id': 3874, 'value': '0.34', 'operator': '<'}
    assert list_egenkspa[4] == {'id': 4072, 'value': '1997', 'operator': '>'}

    assert egenskape_strategy.strategy_type == 'egenskap'

def test_kommune_strategy(kommune_strategy):

    kommune_strategy.filter( {'kommune': 'Haugesund'} )
    kommune_strategy.filter( {'kommune': 'Karmøy'} )
    kommune_strategy.filter( {'kommune': 'Sveio'} )
    kommune_strategy.filter( {'kommune': 'Stavanger'} )
    kommune_strategy.filter( {'kommune': 'Oslo'} )

    kommuner = kommune_strategy.query()

    assert kommuner[1] == 1106
    assert kommuner[2] == 1149
    assert kommuner[3] == 4612
    assert kommuner[4] == 1103
    assert kommuner[5] == 301

    assert kommune_strategy.strategy_type == 'kommune'

def test_fylke_strategy(fylke_strategy):
    
    fylke_strategy.filter( {'fylke': 'Rogaland'} )
    fylke_strategy.filter( {'fylke': 'Vestland'} )
    fylke_strategy.filter( {'fylke': 'Agder'} )

    fylker = fylke_strategy.query()

    assert fylker[1] == 11
    assert fylker[2] == 46
    assert fylker[3] == 42

    assert fylke_strategy.strategy_type == 'fylke'

def test_vegref_strategy(vegref_strategy):
    
    vegref_strategy.filter( {'vegsystemreferanse': 'EV'} )
    vegref_strategy.filter( {'vegsystemreferanse': 'PV'} )
    vegref_strategy.filter( {'vegsystemreferanse': 'RV'} )

    vegrefs = vegref_strategy.query()

    assert vegrefs[1] == 'EV'
    assert vegrefs[2] == 'PV'
    assert vegrefs[3] == 'RV'

    assert vegref_strategy.strategy_type == 'vegsystemreferanse'

def test_uri_egenskap_generator(egenskape_strategy, egenskap_uri_inst):

    egenskape_strategy.set_roadobject_type( 470 )

    egenskape_strategy.filter( {'egenskap': 'Type = Radio'} )
    egenskape_strategy.filter( {'egenskap': 'DSRC avlesing != ITS'} )
    egenskape_strategy.filter( {'egenskap': 'Høyde < 0.34'} )
    egenskape_strategy.filter( {'egenskap': 'Etableringsår > 1997'} )

    uri = egenskap_uri_inst.generate_uri( egenskape_strategy )

    assert uri == 'egenskap(3779)=4822 AND egenskap(13072)!=22693 AND egenskap(3874)<0.34 AND egenskap(4072)>1997'

def test_uri_kommune_generator(kommune_strategy, kommune_uri_inst):

    kommune_strategy.filter( {'kommune': 'Haugesund'} )
    kommune_strategy.filter( {'kommune': 'Karmøy'} )

    uri = kommune_uri_inst.generate_uri( kommune_strategy )

    assert uri == '1106,1149'

def test_uri_fylke_generator(fylke_uri_inst, fylke_strategy):

    fylke_strategy.filter( {'fylke': 'Rogaland'} )
    fylke_strategy.filter( {'fylke': 'Vestland'} )
    fylke_strategy.filter( {'fylke': 'Agder'} )

    uri = fylke_uri_inst.generate_uri( fylke_strategy )

    assert uri == '11,46,42'

def test_uri_vegref_generator(vegref_strategy, vegref_uri_inst):
    
    vegref_strategy.filter( {'vegsystemreferanse': 'EV'} )
    vegref_strategy.filter( {'vegsystemreferanse': 'PV'} )
    vegref_strategy.filter( {'vegsystemreferanse': 'RV'} )

    uri = vegref_uri_inst.generate_uri( vegref_strategy )

    assert uri == 'EV,PV,RV'

def test_consult_manager(consult_instance, egenskape_strategy, kommune_strategy, fylke_strategy, vegref_strategy):

    #it's enaugh for any strategy to set road object just once
    egenskape_strategy.set_roadobject_type( 470 )

    egenskape_strategy.filter( {'egenskap': 'Type = Radio'} )
    egenskape_strategy.filter( {'egenskap': 'DSRC avlesing != ITS'} )
    egenskape_strategy.filter( {'egenskap': 'Høyde < 0.34'} )
    egenskape_strategy.filter( {'egenskap': 'Etableringsår > 1997'} )

    kommune_strategy.filter( {'kommune': 'Haugesund'} )
    kommune_strategy.filter( {'kommune': 'Karmøy'} )

    fylke_strategy.filter( {'fylke': 'Rogaland'} )
    fylke_strategy.filter( {'fylke': 'Vestland'} )
    fylke_strategy.filter( {'fylke': 'Agder'} )

    vegref_strategy.filter( {'vegsystemreferanse': 'FV'} )
    vegref_strategy.filter( {'vegsystemreferanse': 'PV'} )
    vegref_strategy.filter( {'vegsystemreferanse': 'RV'} )


    consult_instance.add_consult( egenskape_strategy )
    consult_instance.add_consult( kommune_strategy )
    consult_instance.add_consult( fylke_strategy )
    consult_instance.add_consult( vegref_strategy )

    consult_instance.execute()

    uri = 'vegobjekter/470?segmentering=true&=egenskap=egenskap(3779)=4822 AND egenskap(13072)!=22693 AND egenskap(3874)<0.34 AND egenskap(4072)>1997&kommune=1106,1149&fylke=11,46,42&vegsystemreferanse=FV,PV,RV&inkluder=alle'
    
    # print(consult_instance.main_uri())
    consult_instance.records()
    assert consult_instance.main_uri() == uri