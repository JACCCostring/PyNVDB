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
        temp_concatenated_query: str = str()
        temp_concat_list: list = [str]

        catalog = Datacatalog()

        egenskaper = catalog.especific_record( type_id=self.___roadobjecttype )['props']

        for filt in self.___filters:
            if filt.get('egenskap'):
                for key, value in filt.get('egenskap').items():
                    
                    for egensk in egenskaper:
                        if egensk['name'] == key:
                            
                            #adding egenskaper that has not possible values
                            eg_id_not_val = egensk['id']

                            temp_concat_list.append( f'egenskap({eg_id_not_val}){op}{value}' )

                            #adding egenskaper that has especific possible values
                            possible_values = egensk['possible_values']
                            
                            for values in possible_values:
                                if values['verdi'] == value:
                                    #concatenate
                                    id_egenskap = egensk['id']
                                    id_value = values['id']
                                    
                                    temp_concat_list.append( f'egenskap({id_egenskap}){op}{id_value}' )
        
        counter: int = int()

        for content in temp_concat_list:
            print(content)
        #     space = ''

        #     if counter == 1 and counter <= len( temp_concat_list ) - 2:
        #         space = ' AND '

        #     temp_concatenated_query += str(content) + space

        #     counter += 1
        
        # base_concatenated_query += temp_concatenated_query

        # return base_concatenated_query.replace("<class 'str'>", '')