from abc import ABC, abstractmethod

from .strategies import Strategy

class UriGenerator(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def generate_uri(self, strategy: Strategy) -> str:
        raise NotImplemented

#uri generator for egenskap
class EgenskapUriGenerator(UriGenerator):
    def __init__(self) -> None:
        super().__init__()

        pass

    def generate_uri(self, consult: Strategy) -> str:
        
        temp_url: str = str()

        for egenskap in consult.query():

            temp_id = egenskap['id']
            temp_op = egenskap['operator']
            temp_value = egenskap['value']

            temp_str = f'egenskap({temp_id}){temp_op}{temp_value} AND '

            temp_url += temp_str
        
        garbage = "egenskap(dict['id'])dict['operator']dict['value'] AND"

        finalurl = temp_url.rstrip( ' AND ' ).replace(garbage, '')

        return finalurl.lstrip(' AND ')

#uri generator for kommune
class KommuneUriGenerator(UriGenerator):
    def __init__(self) -> None:
        super().__init__()

        pass

    def generate_uri(self, consult: Strategy) -> str:
        
        temp_url: str = str()

        for kommune in consult.query():

            temp_str = str(kommune) + ','

            temp_url += temp_str

        #removing , at the begining 
        temp_url = temp_url.replace("<class 'dict'>", '').lstrip(',')
        
        final_url = temp_url

        #removing , at the and, replacing class dict, etc.
        return final_url.rstrip(',').replace("<class 'dict'>", '')
    
#uri generator for fylke
class FylkeUriGenerator(UriGenerator):
    def __init__(self) -> None:
        super().__init__()

        pass

    def generate_uri(self, consult: Strategy) -> str:
        
        temp_url: str = str()

        for fylke in consult.query():

            temp_str = str(fylke) + ','

            temp_url += temp_str

        #removing , at the begining 
        temp_url = temp_url.replace("<class 'dict'>", '').lstrip(',')
        
        final_url = temp_url

        #removing , at the and, replacing class dict, etc.
        return final_url.rstrip(',').replace("<class 'dict'>", '')
    
#uri generator for vegreferanse
class VegrefUriGenerator(UriGenerator):
    def __init__(self) -> None:
        super().__init__()

        pass

    def generate_uri(self, consult: Strategy) -> str:
        
        temp_url: str = str()

        for vegref in consult.query():

            temp_str = str(vegref) + ','

            temp_url += temp_str

        #removing , at the begining 
        temp_url = temp_url.replace("<class 'dict'>", '').lstrip(',')
        
        final_url = temp_url

        #removing , at the and, replacing class dict, etc.
        return final_url.rstrip(',').replace("<class 'dict'>", '')