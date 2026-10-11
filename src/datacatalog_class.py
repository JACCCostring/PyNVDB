from .utils_class import UtilEnviroment, ResourceLoader, ConfigManager
from .utils_class import EndpointDomain
import requests
import json
import os #for path

class CatalogDomain(EndpointDomain):

    def __init__(self):
        super().__init__()

    def set_domain(self, domain) -> None:
        self._domain = domain

    # def get_domain(self):
    #     return self._domain
        

class Datacatalog:

    def __init__(self) -> None:

        self.___environ: UtilEnviroment = UtilEnviroment() #private
        self.___filepath: str = str() #private
        
        self._catalog_domain = CatalogDomain()

        self._catalog_domain.set_domain('datakatalog/api/v1')

    #private method, for internal uses
    def ___get_d(self, endpoint: str, pars: dict = {}) -> requests.Response:
        
        headers = ConfigManager().load_config().get('test_headers')

        return requests.get(endpoint, headers=headers, params=pars if len( pars ) > 0 else {})
    
    #this method will return true if file exist after attemnpt writing
    def download_to_file(self, filename: str = str()) -> bool:

        endpoint = self.___environ.env + 'vegobjekttyper'
        self.___filepath = filename
        temp_list: list = []

        exist_file = os.path.exists( filename )

        params = {'inkluder': 'egenskapstyper'}

        # print('======endpoint: ', endpoint)

        if exist_file == False:
            
            r = self.___get_d( endpoint, params )

            if r.ok:

                with ResourceLoader(filename, 'w') as loader:
                    for item in r.json():

                        temp_list.append( item )
                    
                    loader.file.write( json.dumps( temp_list, indent=4 ) )

        #re-checking again, because exist_file var is already init...
        return os.path.exists(filename)

    #this method return true if catalog version is diff
    def check_version(self) -> bool:

        # endpoint = self.___environ.env + 'status'
        endpoint = self.___environ.env + self._catalog_domain.get_domain() + '/versjon'

        r = self.___get_d( endpoint )

        # print(" ==============: ", r.json())
        # print('endpoint', endpoint)

        if r.ok:

            cat_api_version = r.json()['versjon']

            # print(" ==============: ", cat_api_version)

            if cat_api_version == ConfigManager().load_config().get('catalog_version'):
                return False # if same version
            
            return True #if different version

    def isDataCatalogResources(self) -> bool:

        return os.path.exists( self.___filepath )
    
    def records(self) -> list:

        list_egenskaper_types: list = [dict]

        #laod file
        with ResourceLoader(self.___filepath if self.___filepath else ConfigManager().load_config().get('catalog_path'), 'r') as loader:
            file_content = loader.file.read()

        #loop through file
        if file_content:

            recs = json.loads( file_content )

        #add egenskapstyper to a list
        for item in recs:
            list_egenskaper_types.append( {
                'id': item['id'],
                'name': item['navn'],
                'props': [{
                    'id': content['id'],
                    'name': content['navn'],
                    'possible_values': content['tillatte_verdier'] if content['egenskapstype'] == 'Tekstenum' else {}
                } for content in item['egenskapstyper']]
            } )

        #return egenskaper list
        return list_egenskaper_types

    def especific_record(self, type_name: str = str(), type_id: int = int()) -> list:
        records: list = self.records()

        #if type_name is not None or empty
        if type_name:

            for rec in records:
                if rec['name'] == type_name:
                    return rec
        
        #otherwise
        for rec in records:
                if rec['id'] == type_id:
                    return rec