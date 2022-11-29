import math
import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize

from vkapi.exceptions import APIError

from .config import VK_CONFIG
from .session import Session


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    ses = Session(VK_CONFIG["domain"])
    code = """return API.wall.get({
        "owner_id": "%s",
        "domain": "%s",
        "offset": %d,
        "count": "%d",
        "filter": "%s",
        "extended": %d,
        "fields": "%s",
        "v": "%s"
    });"""
    res = []
    for i in range(math.ceil(count / 100)):
        exec_code = code % (
            owner_id,
            domain,
            100 * i,
            100 * (i + 1) if count > 100 else count,
            filter,
            extended,
            fields,
            VK_CONFIG["version"],
        )
        response = ses.post(
            "execute",
            data={
                "code": exec_code,
                "access_token": VK_CONFIG["access_token"],
                "v": VK_CONFIG["version"],
            },
        ).json()
        res.extend(response["response"]["items"])
        if i % 2 == 0:
            time.sleep(1)
    return json_normalize(res)
