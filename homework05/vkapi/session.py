import typing as tp

import requests
from requests.adapters import HTTPAdapter, Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = None

    def get(self, url: str, params=None, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        session = self.retry_session()
        response = session.get(
            self.base_url + f"/{url}", *args, **kwargs, timeout=self.timeout, params=params
        )
        if response.status_code == 200:
            return response
        raise requests.exceptions.RetryError

    def post(
        self, url: str, params=None, data=None, *args: tp.Any, **kwargs: tp.Any
    ) -> requests.Response:
        session = self.retry_session()
        response = session.post(
            self.base_url + f"/{url}",
            *args,
            **kwargs,
            timeout=self.timeout,
            params=params,
            data=data,
        )
        if response.status_code == 200:
            return response
        raise requests.exceptions.RetryError

    def retry_session(self):
        if not self.session:
            self.session = requests.Session()
            retries = Retry(
                total=self.max_retries,
                backoff_factor=self.backoff_factor,
                raise_on_status=False,
                status_forcelist=[500, 502, 503, 504],
            )
            self.session.mount("https://", HTTPAdapter(max_retries=retries))
        return self.session
