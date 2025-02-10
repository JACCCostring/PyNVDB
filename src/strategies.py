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

        pass
    
    @abstractmethod
    def set_roadobject_type(self, type: int) -> None:
        raise NotImplemented

    @abstractmethod
    def filter(self, filtr: dict) -> None:
        raise NotImplemented
    
    @abstractmethod
    def query(self, op: str) -> str:
        raise NotImplemented

#concreate class
class EgenskapStrategy(Strategy):
    def __init__(self):
        super().__init__()

        self.___filters: list = []
        self.___roadobjecttype: int = int()

    def set_roadobject_type(self, type: int) -> None:
        self.___roadobjecttype = type

    def filter(self, filtr) -> None:
        if filtr.get('egenskap'):
            self.___filters.append( filtr )
    
    def query(self, op: str) -> str:

        base_concatenated_query: str = f'vegobjekter/{self.___roadobjecttype}?egenskap='
        temp_concat_href: str = str()
        list_of_codes: set = set()

        catalog = Datacatalog()

        record = catalog.especific_record( type_id=self.___roadobjecttype ) #a record

        props = record['props'] #a list of props

        def search_code(p: list, name: str):
            for i in p:
                if i['verdi'] == name:
                    return i['id']

        for filt in self.___filters:
            for name, item in filt.items():
                if name == 'egenskap':
                    for k, v in item.items():
                        for prop in props:
                            if prop['name'] == k:

                                search_v_code = search_code(prop['possible_values'], v)
                                value_code = search_v_code if not search_v_code is None else v
                                key_code = prop['id']

                                list_of_codes.add(f'egenskap({key_code}){op}{value_code}')

                                for possi_val in prop['possible_values']:

                                    if possi_val['verdi'] == v:
                                        id = prop['id']
                                        value = possi_val['id']

                                        list_of_codes.add(f'egenskap({id}){op}{value}')
        counter: int = 1
        word: str = str()

        for item in list_of_codes:
            if counter <= len( list_of_codes ) - 1:
                word = ' AND '
            else:
                word = ''

            temp_concat_href += item + word
            counter += 1
        
        full_href = base_concatenated_query + temp_concat_href

        # print( full_href )
        '''
            is passing the minimum test now, but need to be more efficient
            making sure that wahc element in filters collection/data structure
            has it's own operator =>< or !=

            i think a redo of hole method is necesary, because if better aproach
            if we give filter({'egenskap': 'Type = Radio'}) so we can get the operator
            straight from the query instead of passing it as an argument
        '''

        return full_href