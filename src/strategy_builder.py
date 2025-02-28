from .uri_generator import EgenskapUriGenerator
from .uri_generator import KommuneUriGenerator
from .uri_generator import VegrefUriGenerator
from .uri_generator import FylkeUriGenerator
from .uri_generator import UriGenerator
from .strategies import Strategy

from typing import List

class StrategyBuilder:
    def __init__(self) -> None:
        self.___strategies: List[Strategy] = []
        self.___strategies_promotion: List[dict[str, UriGenerator]] = []

        #defining default promotions
        default_promotions: dict[str, UriGenerator] = {
            'egenskap': EgenskapUriGenerator(),
            'fylke': FylkeUriGenerator(),
            'kommune': KommuneUriGenerator(),
            'vegsystemreferanse': VegrefUriGenerator()
        }
        
        #adding default promotions
        self.___strategies_promotion.append( default_promotions )
    
    def promote_strategy(self, new_promotion: dict[str, UriGenerator]) -> None:
        if new_promotion in self.___strategies_promotion:
            raise Exception('Error: promotion already exist!')
        
        if isinstance( new_promotion, dict[str, UriGenerator] ):
            raise Exception('Error: wrong promotion type!')
        # only added if new_promotion is a promotion expected type
        self.___strategies_promotion.append( new_promotion )

    def add_strategy(self, strategy: Strategy) -> None:

        if not isinstance(strategy, Strategy):
            raise Exception('error: wrong type, strategy type required!')
        
        self.___strategies.append( strategy )

    def get_strategy_uri(self, target_strategy: Strategy) -> str:

        if not isinstance(target_strategy, Strategy):
            raise Exception('error: wrong type, strategy type required!')
        
        #only if there is one or more strategies
        if len( self.___strategies ) > 0:

            for strategy in self.___strategies:
                if strategy.strategy_type == target_strategy.strategy_type:
                    #make generator instance
                    for promotion in self.___strategies_promotion:
                        uri_generator = promotion.get( strategy.strategy_type )
                        return uri_generator.generate_uri( strategy )
        
        raise Exception('Error: not any strategy added!')