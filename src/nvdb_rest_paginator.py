from .utils_class import ConfigManager
from dataclasses import dataclass
import asyncio.format_helpers
import asyncio
import aiohttp

@dataclass
class RoadObject:
    nvdbid: int
    version: int
    last_modified: str
    geometry: str

class NVDB_REST_Paginator:

    def __init__(self, start_endpoint: str) -> None:

        self.___start_endpoint: str = start_endpoint
        self.___page_amount: int = int()
        self.___current_amount: int = int()
        self.___records: list = []
        self.___hrefs: set = set()

        if self.___start_endpoint != '':
            self.set_endpoint( self.___start_endpoint )

    def set_endpoint(self, endpoint: str) -> None:

        if self.___start_endpoint != '':
            self.___start_endpoint = endpoint
        
        #start pagination, to gather all data need it
        asyncio.run( self.___paginate() )
    
    def ___populate_href(self, data: list) -> None:

        for item in data['objekter']:

            self.___hrefs.add( item['href'] )
    
    def ___populate_nvdb_data(self, data: dict) -> None:

        object = RoadObject( nvdbid=data['id'], version=data['metadata']['versjon'], 
                            last_modified=data['metadata']['sist_modifisert'],
                            geometry=data['geometri']['wkt']  )
            
        self.___records.append( object )

    async def ___paginate(self) -> None:
        #getting first endpoint to get first pagination
        endpoint = self.___start_endpoint
        #until now, we dont know so 1 is ok it changes after frist pagination fetch
        async with aiohttp.ClientSession() as session:

            first_fetched = await self.___get_pagination_data(session, endpoint)

            first_pagination = first_fetched['metadata']

            self.___page_amount = first_pagination['antall']
            self.___current_amount = first_pagination['returnert']

            #getting next endpoint, after being done with first
            endpoint = self.___start_endpoint + '&start=' + first_pagination['neste']['start']

            #add start of href
            self.___populate_href( first_fetched )

        async with aiohttp.ClientSession() as session:

            for _ in range(int(self.___page_amount / self.___current_amount)):
                
                result = await self.___get_pagination_data(session, endpoint)

                pagination = result['metadata']

                endpoint = pagination['neste']['href']

                self.___current_amount += pagination['returnert']
                    
                print( self.___current_amount, ' of ', self.___page_amount)

                self.___populate_href( result )
        
        '''
            now that we have a list of href of paginated road objects
            then we preceed to fetch all the road objects corresponding
            to those href, only if href list is populated
        '''
        if len( self.___hrefs ) > 0:
            print('preparing nvdb data')
            await self.___prepare_nvdb_data()
        
    async def ___get_pagination_data(self, session, endpoint) -> dict:

        response = await session.get(endpoint, headers=ConfigManager().load_config().get('test_headers'))

        if response.ok:
            return await response.json()
    
    async def ___prepare_nvdb_data(self) -> None:
        tasks: list = []

        async with aiohttp.ClientSession() as session:
            for href in self.___hrefs:

                task = asyncio.create_task( session.get( href, headers=ConfigManager().load_config().get('test_headers') ) )
                tasks.append( task )
            
            print('done preparing!')

            print('start executing task ...')

            responses_coro = await asyncio.gather( *tasks )
            
            for response in responses_coro:
                
                if response.ok:
        
                    self.___populate_nvdb_data( await response.json() )
            
            print( 'size href pagination:', len(self.___hrefs) )
            print( 'size nvdb records:', len(self.___records) )

    
    def nvdb_data(self) -> list:
        return self.___records