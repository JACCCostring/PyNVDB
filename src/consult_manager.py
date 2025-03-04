from .nvdb_rest_paginator import NVDB_REST_Paginator
from .strategy_builder import StrategyBuilder
from .query_manager import QueryManager
from .utils_class import UtilEnviroment
from .strategies import Strategy

#class Consult Manager for managing consults
class ConsultManager:

    def __init__(self) -> None:

        self.___consults: list[Strategy] = []
        self.___uris_completed: list[dict] = []
        self.___road_object_type_id: int = int()
        self.___main_uri: str = str('')
        self.___environ: UtilEnviroment = UtilEnviroment() #test env by default

    def add_consult(self, consult: Strategy) -> None:

        if isinstance(consult, Strategy):
            self.___consults.append( consult )

        else:
            raise Exception('error: Wrong strategy type not supported')
    
    def add_query(self, query_manager: QueryManager) -> None:
        #executing all queries to generate strategies
        query_manager.execute()

        #getting list of strategies
        strategies = query_manager.strategies()

        #looping through
        for strategy in strategies:
            #adding strategy
            self.add_consult( strategy )

    def set_roadobject_type(self, type: int) -> None:

        if self.___road_object_type_id == 0:

            self.___road_object_type_id = type

            '''
            making sure that main_uri has a value or valid endpoint, in case
            of non strategy consult is especified and object type was set from
            consult manager and not from a strategy
            '''
            if self.___main_uri == '':
            
                self.___main_uri: str = f'vegobjekter/{self.___road_object_type_id}?segmentering=true&inkluder=alle,geometri'

    def main_uri(self) -> str:
        
        return self.___main_uri.replace("&=egenskap=egenskap(dict['id'])dict['operator']dict['value']", '')
    
    def execute(self) -> None:

        for consult in self.___consults:
            #egenskap
            '''
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
                    self.___road_object_type_id = consult._roadobjecttype '''

            #new strategy builder improvements
            builder = StrategyBuilder()

            builder.add_strategy( consult )

            uri = builder.get_strategy_uri( consult )

            self.___uris_completed.append( {'uri': uri, 'type': consult.strategy_type } )

            if self.___road_object_type_id == 0:

                self.___road_object_type_id = consult._roadobjecttype

        '''
            substract main URI and store it, for later and making
            sure that self.___main_uri will be only filled if
            there are consults to make
        '''
        if len( self.___consults ) > 0:
            self.___main_uri = self.___substract_uri()

        #otherwise then just add vegobjekt, segmentering og inkluder
        if len( self.___consults ) == 0:

            self.___main_uri: str = f'vegobjekter/{self.___road_object_type_id}?segmentering=true&inkluder=alle,geometri'

    def ___substract_uri(self) -> list:

        uris: list[str] = []

        #base url segments are True by default, it can changes later
        base_url: str = f'vegobjekter/{self.___road_object_type_id}?segmentering=true&'
        
        if self.___road_object_type_id == 0:
            raise Exception('Error: road object type must be set in one of the strategies or in Consult Manager')
        
        #if it has uris
        if len(self.___uris_completed) > 0:

            for uri in self.___uris_completed:

                # type = uri.get('type').value #enum type and access value
                type = uri.get('type')
                value = uri.get('uri')

                base_url += f'{type}={value}'

                uris.append( base_url )

                base_url = ''

            uri_result: str = str()

            for uri_item in uris:

                uri_result += uri_item + '&'
            
            return uri_result.rstrip('&') + '&inkluder=metadata,geometri' #including metadata and geometry
        
        #if not then raise exception
        if len(self.___uris_completed) and self.___road_object_type_id == 0:
            raise Exception('Error: not consult to process!')

    def records(self) -> list:

        if self.___main_uri != '':

            endpoint: str = self.___environ.env + self.___main_uri

            nvdb_paginator = NVDB_REST_Paginator( endpoint )
            
            return nvdb_paginator.nvdb_data()
        
        if self.___main_uri == '':
            raise Exception('Error: Consult is not populated yet!')