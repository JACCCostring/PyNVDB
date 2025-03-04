from .strategies import EgenskapStrategy
from .strategies import KommuneStrategy
from .strategies import VegrefStrategy
from .strategies import FylkeStrategy
from .strategies import Strategy

from typing import List, Dict

class QueryManager:

    def __init__(self, road_objecttype: int = int()) -> None:
        self.___road_objecttype = road_objecttype

        self.___strategies: List[ Strategy ] = []

        self.___entries: Dict[ str, List ]= {}

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

        if not isinstance(new_query, dict):
            raise Exception('Error: Wrong acceptable query {}!'.format( type( new_query ) ))
        
        for key in new_query.keys():
            
            for value in new_query.values():

                self.___acceptable_queries[ key ] = value

        
    def filter(self, query: dict[str, str]) -> None:
        if self.___road_objecttype is 0:
            raise Exception('Error: not road object type assigned yet!')
        
        for accetable_query in self.___acceptable_queries:
            
            # checking if there is a valid query
            if query.get( accetable_query ):
   
                #if not first coincidence then get the list and append new query
                if self.___entries.get( accetable_query ):
                    
                    #collection for new query data to add to list
                    new_query: List = []

                    entry = self.___entries.get( accetable_query )
                    
                    #preparing data
                    for quer in query.values():
                        new_query.append( quer )

                    #extending old list values with new values
                    entry.extend( new_query )
                    
                    self.___entries[ accetable_query ] = entry

                #if first coincidence then just added
                if not self.___entries.get( accetable_query ):

                    #collection for new query data to add to list
                    new_query: List = []
                    
                    #preparing data
                    for qu in query.values():
                        new_query.append( qu )

                    self.___entries[ accetable_query ] = new_query

    def execute(self) -> None:

        #transforming from messy to normal filter querys
        for item_name, item_value in self.___entries.items():
            # then instantiate strategy
            strategy_instance = self.___acceptable_queries.get( item_name )

            #setting road object type just in case
            strategy_instance.set_roadobject_type( self.___road_objecttype )
            
            #filtrering            adding key : list of values
            strategy_instance.filters( { item_name: item_value } )

            #appending new created strat.. to strategy list
            self.___strategies.append( strategy_instance )

    def strategies(self) -> list:
        return self.___strategies