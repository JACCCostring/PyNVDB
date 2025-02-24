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
        self.___page_amount: int = int() #will be discovered later after first fetch
        self.___current_amount: int = int() #start amount for pagination after first fetch
        self.___records: list = []

        if self.___start_endpoint != '':
            self.set_endpoint( self.___start_endpoint )

    def set_endpoint(self, endpoint: str) -> None:

        if self.___start_endpoint == '':
            self.___start_endpoint = endpoint
        
        #start pagination, to gather all data need it
        asyncio.run( self.___paginate() )
    
    def ___populate_nvdb_data(self, data: dict) -> None:

        for item in data['objekter']:

            object = RoadObject( nvdbid=item['id'], version=item['metadata']['versjon'], 
                                last_modified=item['metadata']['sist_modifisert'],
                                geometry=item['geometri']['wkt']  )
            
            self.___records.append( object )

    async def ___getandparse_nvdb_data(self, endpoint, session) -> None:

        async with session.get( endpoint, headers=ConfigManager().load_config().get('test_headers') ) as request:
            if request.ok:
                return await request.json()

    async def ___paginate(self) -> None:
        tasks: list = []

        first_pag = await self.___first_pagination()

        self.___page_amount = first_pag['antall']
        # self.___current_amount = 1000 if first_pag['returnert'] <= 1000 else first_pag['returnert']
        self.___current_amount = first_pag['returnert']

        next_endpoint = first_pag['neste']['href']

        '''
            some times return data amount and total data amaount
            if divide it is equal to 1 or 2 then we need to trick to get
            that amount + 1, because of the loop, so we can get enough iterations
            to get all task, so may be next endpoint could be the start point,
            since we dont need to fetch next endpoint because we're only getting
            800 or less amount
        '''
        if self.___current_amount <= 800:
            next_endpoint = self.___start_endpoint

        print()
        print('starting ...')
        print('fetching', self.___page_amount, 'vegobjekter')

        async with aiohttp.ClientSession() as session:
            for _ in range( int( self.___page_amount / self.___current_amount ) ):
                
                print(self.___current_amount, ' of ', self.___page_amount)

                task = asyncio.create_task( self.___getandparse_nvdb_data(next_endpoint, session) )
                tasks.append( task )

                next_pag = await self.___next_pagination(next_endpoint, session)
                next_endpoint = next_pag['neste']['href']

                # self.___current_amount += 1000 if first_pag['returnert'] <= 1000 else first_pag['returnert']
                self.___current_amount += next_pag['returnert']

                # print(next_endpoint)
                
            print('ending fetch ...')
            responses_coro = await asyncio.gather( *tasks )

            print('processing ...')
            for response in responses_coro:
                self.___populate_nvdb_data( response )

        for item in self.___records:
            if item.nvdbid == 460057601:
                print('id:', item.nvdbid, ' wkt:', item.geometry)

    async def ___first_pagination(self) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.get( self.___start_endpoint, headers=ConfigManager().load_config().get('test_headers') )

            if response.ok:
                data = await response.json()
                return data['metadata']
    
    async def ___next_pagination(self, endpoint, session) -> None:
        async with session.get( endpoint, headers=ConfigManager().load_config().get('test_headers') ) as response:

            if response.ok:
                data = await response.json()
                return data['metadata']
        
    def nvdb_data(self) -> list:
        return self.___records