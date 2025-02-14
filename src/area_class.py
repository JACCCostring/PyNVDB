from .utils_class import UtilEnviroment, ConfigManager, ResourceLoader
from typing import Protocol
import requests
import json
import os

class AreaLocationType(Protocol):
    def __init__(self) -> None:
        super().__init__()
        
        raise NotImplemented

    def ___get_data(self, endpoint: str, headers: dict = {}) -> requests.Response:
        raise NotImplemented

    def download_area(self) -> bool:
        raise NotImplemented

    def isAreaResources(self):
        raise NotImplemented

    def communities(self) -> list:
        raise NotImplemented

    def counties(self) -> list:
        raise NotImplemented
    
    def community_name(self, conde: int) -> str:
        raise NotImplemented
    
    def community_code(self, name: str) -> int:
        raise NotImplemented
    
    def county_name(self, conde: int) -> str:
        raise NotImplemented
    
    def county_code(self, name: str) -> int:
        raise NotImplemented
    
class AreaLocation:
    def __init__(self) -> None:
        self.___environ: UtilEnviroment = UtilEnviroment() #private

    def ___get_data(self, endpoint: str, headers: dict = {}) -> requests.Response:
        
        return requests.get(endpoint, headers=headers)
    
    def download_area(self) -> bool:
        endpoint_c = self.___environ.env + 'omrader/kommuner'
        endpoint_co = self.___environ.env + 'omrader/fylker'

        headers = ConfigManager().load_config().get('test_headers')

        exist_file_com = os.path.exists( ConfigManager().load_config().get('communities_path') )
        exist_file_coun = os.path.exists( ConfigManager().load_config().get('counties_path') )

        if not exist_file_com and not exist_file_coun:

            c = self.___get_data(endpoint_c, headers)
            co = self.___get_data(endpoint_co, headers)

            if c.ok and co.ok:
                with ResourceLoader(ConfigManager().load_config().get('communities_path'), 'w') as resource:
                    resource.file.write( json.dumps( c.json(), indent=4 ) )
                
                with ResourceLoader(ConfigManager().load_config().get('counties_path'), 'w') as resource:
                    resource.file.write( json.dumps( co.json(), indent=4 ) )
        
        recheck_file_com = os.path.exists( ConfigManager().load_config().get('communities_path') )
        recheck_file_coun = os.path.exists( ConfigManager().load_config().get('counties_path') )

        return recheck_file_com and recheck_file_coun

    def isAreaResources(self) -> bool:

        recheck_file_com = os.path.exists( ConfigManager().load_config().get('communities_path') )
        recheck_file_coun = os.path.exists( ConfigManager().load_config().get('counties_path') )

        return recheck_file_com and recheck_file_coun
    
    def communities(self) -> list:
        with ResourceLoader(ConfigManager().load_config().get('communities_path'), 'r') as resource:
            return json.loads( resource.file.read() )

    def counties(self) -> list:
        with ResourceLoader(ConfigManager().load_config().get('counties_path'), 'r') as resource:
            return json.loads( resource.file.read() )
    
    def community_name(self, code_community: int) -> str:
        communities = self.communities()

        for community in communities:
            if community['nummer'] == code_community:
                return community['navn']

    def community_code(self, name_community: str) -> int:
        communities = self.communities()

        for county in communities:
            if county['navn'] == name_community:
                return county['nummer']
    
    def county_name(self, code_county: int) -> str:
        counties = self.counties()

        for county in counties:
            if county['nummer'] == code_county:
                return county['navn']

    def county_code(self, name_county: str) -> int:
        counties = self.counties()

        for county in counties:
            if county['navn'] == name_county:
                return county['nummer']