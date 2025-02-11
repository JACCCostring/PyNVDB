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

    def filter(self, filtr: dict) -> None:
        if filtr.get('egenskap'):
            self._filters.append( filtr )
    
    @abstractmethod
    def query(self, op: str) -> str:
        raise NotImplemented

#concreate class
class EgenskapStrategy(Strategy):
    def __init__(self):
        super().__init__()

        pass
    
    def query(self, op: str) -> str:

        base_concatenated_query: str = f'vegobjekter/{self._roadobjecttype}?egenskap='
        temp_concat_href: str = str()
        list_of_codes: set = set()
        
        catalog = Datacatalog()

        record = catalog.especific_record( type_id=self._roadobjecttype ) #a record

        props = record['props'] #a list of props