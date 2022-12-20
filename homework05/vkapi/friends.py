import dataclasses
import math
import time
import typing as tp

from .config import VK_CONFIG
from .exceptions import APIError
from .session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    ses = Session(VK_CONFIG["domain"])
    params = {
        "user_id": str(user_id),
        "count": str(count),
        "offset": str(offset),
        "fields": fields,
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
    }
    response = ses.get("friends.get", params=params)
    response = response.json()["response"]
    return FriendsResponse(response["response"]["count"], response["response"]["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[tp.Optional[int]]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    if target_uids is None:
        target_uids = [target_uid]

    result = []

    for i in range(0, len(target_uids), 100):
        result += session.get(
            "friends.getMutual",
            source_uid=source_uid,
            target_uids=target_uids,
            order=order,
            count=count,
            offset=offset + i,
            v=config.VK_CONFIG["version"],
            access_token=config.VK_CONFIG["access_token"],
        ).json()["response"]

        if i % 200 == 0:
            time.sleep(1)

    if target_uid is not None:
        return result[0]["common_friends"]

    return result


def get_mutual_with_class(
    target_uids: tp.List[int],
    source_uid: tp.Optional[int] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.List[MutualFriends]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    ses = Session(VK_CONFIG["domain"])
    params = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": str(offset),
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
    }
    result = []

    for i in range(0, len(target_uids), 100):
        result += session.get(
            "friends.getMutual",
            source_uid=source_uid,
            target_uids=target_uids,
            order=order,
            count=count,
            offset=offset + i,
            v=config.VK_CONFIG["version"],
            access_token=config.VK_CONFIG["access_token"],
        ).json()["response"]

        if i % 200 == 0:
            time.sleep(1)

    return result
