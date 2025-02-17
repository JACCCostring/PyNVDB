from .datacatalog_class import Datacatalog
from .area_class import AreaLocation
from abc import ABC, abstractmethod
from typing import Protocol

#protocol for types
class StrategyType(Protocol):
    def __init__(self) -> None:
        super().__init__()

        pass

    def set_roadobject_type(self, type: int) -> None:
        raise NotImplemented
    
    def _check_sign_operator(self, str_check: str) -> str:
        raise NotImplemented
    
    def filter(self, filtr: dict) -> None:
        raise NotImplemented

    def query(self, op: str) -> list:
        raise NotImplemented

#abstract/interface class
class Strategy(ABC):
    def __init__(self) -> None:
        super().__init__()

        #protected variables because of inheritance
        self._filters: list = []
        self._roadobjecttype: int = int()
        self._strategy_type: str = str()
    
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
            self.strategy_type = 'egenskap'
        
        if filtr.get('relasjon'):
            self._filters.append( filtr )
            self.strategy_type = 'relasjon'
        
        if filtr.get('vegsystemreferanse'):
            self._filters.append( filtr )
            self.strategy_type = 'vegsystemreferanse'
        
        if filtr.get('kommune'):
            self._filters.append( filtr )
            self.strategy_type = 'kommune'
        
        if filtr.get('fylke'):
            self._filters.append( filtr )
            self.strategy_type = 'fylke'
    
    def strategy_type(self) -> str:
        if len( self._filters ) > 0:
            return self.strategy_type
        
    @abstractmethod
    def query(self, op: str) -> list:
        raise NotImplemented

#concreate class for egenskaper
class EgenskapStrategy(Strategy):
    def __init__(self):
        super().__init__()

        pass
    
    def query(self) -> list[ dict ]:

        list_of_egenskaper_codes: list = [ dict ]
        value_id: str = str()

        if self._roadobjecttype == 0:
            raise Exception(f'Error: road object type unknown {self._roadobjecttype}')
        
        catalog = Datacatalog()

        record = catalog.especific_record( type_id=self._roadobjecttype ) #a record

        props = record['props'] #a list of props
            
        for egenskap in self._filters:

            if egenskap.get('egenskap'):

                chunk: dict = egenskap.get('egenskap')

                operator: str = self._check_sign_operator( chunk )

                '''
                in the case of a ! operator, then concatenate =
                to avoid more splits and more code overheads
                '''
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
    
#concrete class for kommune
class KommuneStrategy(Strategy):
    def __init__(self):
        super().__init__()

        pass
    
    def query(self) -> list:

        list_of_kommuner_codes: list = [ dict ]
        value_id: str = str()

        location = AreaLocation() #area location class for omroader
            
        for kommuner in self._filters:

            if kommuner.get('kommune'):

                kommune_name: dict = kommuner.get('kommune')

                kommune_code = location.community_code( kommune_name )

                list_of_kommuner_codes.append( kommune_code )

        return list_of_kommuner_codes
    
#concrete class for fylke
class FylkeStrategy(Strategy):
    def __init__(self):
        super().__init__()

        pass
    
    def query(self) -> list:

        list_of_fylker_codes: list = [ dict ]
        value_id: str = str()

        location = AreaLocation() #area location class for omroader
            
        for fylker in self._filters:

            if fylker.get('fylke'):

                fylke_name: dict = fylker.get('fylke')

                fylke_code = location.county_code( fylke_name )

                list_of_fylker_codes.append( fylke_code )

        return list_of_fylker_codes

#concrete class for vegref
class VegrefStrategy(Strategy):
    def __init__(self):
        super().__init__()

        pass
    
    def query(self) -> list:

        list_of_vegref: list = [ dict ]
        value_id: str = str()
            
        for vegref in self._filters:

            if vegref.get('vegsystemreferanse'):

                vegref_name: dict = vegref.get('vegsystemreferanse')

                if 'EV' or 'PV' or 'FV' or 'KV' 'RV' in vegref_name:
                    list_of_vegref.append( vegref_name )

        return list_of_vegref