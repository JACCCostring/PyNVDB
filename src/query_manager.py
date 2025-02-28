from .consult_manager import ConsultManager
from .strategies import EgenskapStrategy
from .strategies import KommuneStrategy
from .strategies import VegrefStrategy
from .strategies import FylkeStrategy
from .strategies import Strategy

class QueryManager:

    def __init__(self, road_objecttype: int = int()) -> None:
        self.___road_objecttype = road_objecttype
        self.___consult_manager: ConsultManager = ConsultManager()

        self.___acceptable_queries: dict[str, Strategy] = {
            'egenskap': EgenskapStrategy(),
            'kommune': KommuneStrategy(),
            'fylke': FylkeStrategy(),
            'vegsystemreferanse': VegrefStrategy()
        }

        if self.___road_objecttype is not 0:
            self.set_road_onjecttype( self.___road_objecttype )

    def set_road_onjecttype(self, road_objecttype: int) -> None:
        if road_objecttype is not 0 and self.___road_objecttype is 0:
            self.___road_objecttype = road_objecttype
    
    def add_acceptable_query(self, new_query: dict[str, Strategy]) -> None:
        if not isinstance(new_query, dict[str, Strategy]):
            raise Exception('Error: Wrong acceptable query!')
        
        if new_query not in self.___acceptable_queries:
            self.___acceptable_queries.append( new_query )

    def filter(self, query: dict[str, str]) -> None:
        if self.___road_objecttype is 0:
            raise Exception('Error: not road object type assigned yet!')
        
        for accetable_query in self.___acceptable_queries:
            
            # checking if there is a valid query
            if query.get( accetable_query ):
                print('executing...')

                #then instantiate strategy
                strategy_instance = self.___acceptable_queries.get( accetable_query )

                #assigning road object type
                strategy_instance.set_roadobject_type( self.___road_objecttype )

                #assigning corrsponding filter, until here we are sure that query is valid
                strategy_instance.filter( query )
                
                self.___consult_manager.set_roadobject_type( self.___road_objecttype )
                #adding strategy to consult manager
                self.___consult_manager.add_consult( strategy_instance )

    def records(self) -> list:
        #executing consults
        self.___consult_manager.execute()

        #returning a lits of records
        return self.___consult_manager.records()