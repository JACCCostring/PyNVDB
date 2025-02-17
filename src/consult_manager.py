from .uri_generator import EgenskapUriGenerator, KommuneUriGenerator, FylkeUriGenerator
from .strategies import Strategy

from enum import Enum

#Enum for consult types
class ConsultType(Enum):
    egenskap = 'egenskap'
    relasjon = 'relasjon'
    vegsystemreferanse = 'vegsystemreferanse'
    kommune = 'kommune'
    fylke = 'fylke'

#class Consult Manager for managing consults
class ConsultManager:

    def __init__(self) -> None:
        self.___consults: list[Strategy] = []
        self.___uris_completed: list[dict] = []
        self.___road_object_type_id: int = int()
        self.___main_uri: str = str()

    def add_consult(self, consult: Strategy) -> None:

        if isinstance(consult, Strategy):
            self.___consults.append( consult )

        else:
            raise Exception('error: Wrong strategy type not supported')

    def execute(self) -> None:

        for consult in self.___consults:
            #egenskap
            if consult.strategy_type == ConsultType.egenskap.value:
                #proccessing egenskap consults
                uri = EgenskapUriGenerator().generate_uri( consult )
                #adding it to list of completed URIs
                self.___uris_completed.append( {'uri': uri, 'type': ConsultType.egenskap} )

                #init.. on any iteration, only if it's not set from before on any of the strategy type
                if self.___road_object_type_id == 0:
                    self.___road_object_type_id = consult._roadobjecttype

            #kommune
            if consult.strategy_type == ConsultType.kommune.value:
                #proccessing egenskap consults
                uri = KommuneUriGenerator().generate_uri( consult )
                #adding it to list of completed URIs
                self.___uris_completed.append( {'uri': uri, 'type': ConsultType.kommune} )

                #init.. on any iteration, only if it's not set from before on any of the strategy type
                if self.___road_object_type_id == 0:
                    self.___road_object_type_id = consult._roadobjecttype
            
            #fylke
            if consult.strategy_type == ConsultType.fylke.value:
                #proccessing egenskap consults
                uri = FylkeUriGenerator().generate_uri( consult )
                #adding it to list of completed URIs
                self.___uris_completed.append( {'uri': uri, 'type': ConsultType.fylke} )

                #init.. on any iteration, only if it's not set from before on any of the strategy type
                if self.___road_object_type_id == 0:
                    self.___road_object_type_id = consult._roadobjecttype
                
            #vegref
            if consult.strategy_type == ConsultType.vegsystemreferanse.value:
                #proccessing egenskap consults
                uri = FylkeUriGenerator().generate_uri( consult )
                #adding it to list of completed URIs
                self.___uris_completed.append( {'uri': uri, 'type': ConsultType.vegsystemreferanse} )

                #init.. on any iteration, only if it's not set from before on any of the strategy type
                if self.___road_object_type_id == 0:
                    self.___road_object_type_id = consult._roadobjecttype

        #substract main URI and store it, for later
        self.___main_uri = self.___substract_uri()

    def ___substract_uri(self) -> list:
        
        uris: list[str] = []
        base_url: str = f'vegobjekter/{self.___road_object_type_id}?segmentering=true&='

        if len(self.___uris_completed) > 0:

            for uri in self.___uris_completed:

                if uri.get('type') == ConsultType.egenskap:

                    target = uri.get('uri')

                    base_url += f'egenskap={target}'

                    uris.append( base_url )

                    base_url = ''

                if uri.get('type') == ConsultType.kommune:

                    target = uri.get('uri')

                    base_url += f'kommune={target}'

                    uris.append( base_url )

                    base_url = ''

                if uri.get('type') == ConsultType.fylke:

                    target = uri.get('uri')

                    base_url += f'fylke={target}'

                    uris.append( base_url )

                    base_url = ''
                
                if uri.get('type') == ConsultType.vegsystemreferanse:

                    target = uri.get('uri')

                    base_url += f'vegsystemreferanse={target}'

                    uris.append( base_url )

                    base_url = ''

            uri_result: str = str()

            for uri_item in uris:
                uri_result += uri_item + '&'
            
            return uri_result.rstrip('&') + '&inkluder=alle'
            
        if len(self.___uris_completed) == 0:
            raise Exception('Error: not consult to process!')
    
    def main_uri(self) -> str:
        return self.___main_uri.replace("&=egenskap=egenskap(dict['id'])dict['operator']dict['value']", '')