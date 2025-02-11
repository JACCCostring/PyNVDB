import pytest

from src import UtilEnviroment
from src import Datacatalog
from src import ConfigManager
from src import AreaLocation
from src import EgenskapStrategy

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

def test_catalog_download_to_file_and_resoruces(catalog_instance, config_manager):

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

def test_area_download_and_resoruces(area_instance):

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

    egenskape_strategy.filter({'egenskap': {'Type': 'Radio'}})
    egenskape_strategy.filter({'egenskap': {'DSRC avlesing': 'ITS'}})
    egenskape_strategy.filter({'egenskap': {'Høyde': 0.34}})
    egenskape_strategy.filter({'egenskap': {'Etableringsår': 1997}})

    egenskape_strategy.query('>')