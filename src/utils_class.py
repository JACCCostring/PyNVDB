import json

class ResourceLoader:

    def __init__(self, filename: str, mode: str) -> None:
        self.__filename = filename
        self.__mode = mode

    def __enter__(self):
        data: dict = {}

        self.file = open(self.__filename, self.__mode)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()
    
class UtilEnviroment:

    def __init__(self, nenv: str = str('test')) -> None:
        self.___current_env: str = nenv
        self.___endpoints: dict[str, str] = ConfigManager().load_config().get('endpoints')

    @property
    def env(self) -> str:
        if self.___current_env == 'test':
            return self.___endpoints.get('test')
        
        if self.___current_env == 'prod':
            return self.___endpoints.get('prod')
        
    @env.setter
    def env(self, new_env: str) -> None:
        self.___current_env = new_env

class ConfigManager:

    def __init__(self) -> None:
        with ResourceLoader('resources/config.json', 'r') as loader:
            self.config_content = json.loads( loader.file.read() )

    def load_config(self) -> dict:
        return self.config_content