import aiohttp
from loguru import logger


class AsyncAPIClient:
    """Класс реализует подключение к REST API сервисов"""

    def __init__(self, url, user, password):
        self.__url = url
        self.__user = user
        self.__password = password

    def auth(self):
        return aiohttp.BasicAuth(login=self.__user, password=self.__password)

    async def get(self, uri):
        """
        Функция содержит в себе basic авторизацию
        Имеет сессионное подключение, на протяжении итерации
        имеет один контекст.

        :param uri: URI (path + query_param)
        :return: ClientResponse List[{}]
        """

        ssl = aiohttp.TCPConnector(verify_ssl=False)

        async with aiohttp.ClientSession(auth=self.auth(), connector=ssl) as client:
            response = await client.get(self.__url + uri)
            logger.info(response.url)
            return await response.json()
