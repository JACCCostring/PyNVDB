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
        self.___uris_completed: list[str] = []

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
                self.___uris_completed.append( uri )

            #kommune
            if consult.strategy_type == ConsultType.kommune.value:
                #proccessing egenskap consults
                uri = KommuneUriGenerator().generate_uri( consult )
                #adding it to list of completed URIs
                self.___uris_completed.append( uri )
            
            #fylke
            if consult.strategy_type == ConsultType.fylke.value:
                #proccessing egenskap consults
                uri = FylkeUriGenerator().generate_uri( consult )
                #adding it to list of completed URIs
                self.___uris_completed.append( uri )
    
    def records(self) -> list:

        if len(self.___uris_completed) > 0:
            for uri in self.___uris_completed:
                if uri.startswith('egenskap('):
                    print(uri)

        if len(self.___uris_completed) == 0:
            raise Exception('Error: not consult to process!')