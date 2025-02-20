from .utils_class import ConfigManager
from dataclasses import dataclass
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
        self.___nvdb_records: list = []

        if self.___start_endpoint != '':
            self.set_endpoint( self.___start_endpoint )

    def set_endpoint(self, endpoint: str) -> None:

        if self.___start_endpoint != '':
            self.___start_endpoint = endpoint
        
        #start pagination, to gather all data need it
        asyncio.run( self.___paginate() )
    
    def ___populate_list(self, data: list) -> None:

        for item in data['objekter']:
            object = RoadObject( nvdbid=item['id'], version=item['metadata']['versjon'], 
                                last_modified=item['metadata']['sist_modifisert'],
                                geometry=item['geometri']['wkt']  )
            
            self.___nvdb_records.append( object )

    async def ___paginate(self) -> None:
        data = await self.___get_pagination_data()

        metadata = data['metadata']

        self.___page_amount = metadata['antall']
        self.___current_amount = metadata['returnert']
        next_endpoint = '&start=' + metadata['neste']['start']
        
        starturl = self.___start_endpoint
        starturl += next_endpoint

        self.___populate_list( data )

        tasks: list = []

        '''
            if total amount is return in one fetch, then not need to fetch more
            otherwise, fetch the rest
        '''
        async def fetch_more(session, endpoint) -> list:
            async with session.get(endpoint, headers=ConfigManager().load_config().get('test_headers')) as request:
                if request.ok:
                    return await request.json()

        if self.___current_amount < self.___page_amount:
            for _ in range(int(self.___page_amount / self.___current_amount)):
                async with aiohttp.ClientSession() as session:
                        
                    data_next = await asyncio.create_task( fetch_more(session, starturl) )

                    self.___populate_list( data_next )

                    self.___current_amount += data_next['metadata']['returnert']

                    starturl = self.___start_endpoint +'&start=' + data_next['metadata']['neste']['start']

    async def ___get_pagination_data(self) -> dict:

        #sub async method, first call
        async def subcall_get_first(session, endpoint):
            async with session.get(endpoint, headers=ConfigManager().load_config().get('test_headers')) as request:
                if request.ok:
                    return await request.json()
            
        async with aiohttp.ClientSession() as session:
            return await subcall_get_first(session, self.___start_endpoint)
    
    def nvdb_data(self) -> list:
        return self.___nvdb_records