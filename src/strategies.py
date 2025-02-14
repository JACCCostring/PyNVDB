from .datacatalog_class import Datacatalog
# from .utils_class import ConfigManager
from abc import ABC, abstractmethod
from typing import Protocol

#protocol for types
class StrategyType(Protocol):
    def __init__(self) -> None:
        super().__init__()

        pass

    def set_roadobject_type(self, type: int) -> None:
        raise NotImplemented
    
    def filter(self, filtr: dict) -> None:
        raise NotImplemented

    def query(self, op: str) -> str:
        raise NotImplemented

#abstract/interface class
class Strategy(ABC):
    def __init__(self) -> None:
        super().__init__()

        #protected variables because of inheritance
        self._filters: list = []
        self._roadobjecttype: int = int()
    
    def set_roadobject_type(self, type: int) -> None:
        self._roadobjecttype = type
    
    def _check_sign_operator(self, str_check: str) -> str:
        for check in str_check:
            if '=' in check:
                return check;
            if '!' in check:
                return check;
            if '>' in check:
                return check;
            if '<' in check:
                return check;

    def filter(self, filtr: dict) -> None:
        if filtr.get('egenskap'):
            self._filters.append( filtr )
        
        if filtr.get('relasjon'):
            self._filters.append( filtr )
        
        if filtr.get('vegreferanse'):
            self._filters.append( filtr )
        
        if filtr.get('kommune'):
            self._filters.append( filtr )
        
        if filtr.get('fylke'):
            self._filters.append( filtr )
    
    @abstractmethod
    def query(self, op: str) -> str:
        raise NotImplemented

#concreate class
class EgenskapStrategy(Strategy):
    def __init__(self):
        super().__init__()

        pass
    
    def query(self) -> list[ dict ]:

        # base_concatenated_query: str = f'vegobjekter/{self._roadobjecttype}?egenskap='
        list_of_egenskaper_codes: list = [ dict ]
        value_id: str = str()

        catalog = Datacatalog()

        record = catalog.especific_record( type_id=self._roadobjecttype ) #a record

        props = record['props'] #a list of props
            
        for egenskap in self._filters:

            if egenskap.get('egenskap'):

                chunk: dict = egenskap.get('egenskap')

                operator: str = self._check_sign_operator( chunk )

                if operator == '!':
                    operator += '='

                split_chunk: list = chunk.split( operator )

                egenskap_type_name: str = split_chunk[0].strip()
                egenskap_type_value: str = split_chunk[1].strip()

                #find egenskap name
                for prop_itr in props:
                    if prop_itr['name'] == egenskap_type_name:

                        #get id of that egenskap, but first find possible values
                        if prop_itr['possible_values']:

                            for p in prop_itr['possible_values']:

                                if p['verdi'] == egenskap_type_value:

                                    value_id = p['id']

                        #get id only when props does not has possible values
                        if not prop_itr['possible_values']:
                            
                            value_id = egenskap_type_value

                        list_of_egenskaper_codes.append( 
                        {
                            'id': prop_itr['id'], #id for egenskaper type
                            'value': value_id, #value of that egenskap id
                            'operator': operator
                        })

        return list_of_egenskaper_codes