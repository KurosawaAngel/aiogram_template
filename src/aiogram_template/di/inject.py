from typing import Awaitable, Callable

from dishka.integrations.aiogram import CONTAINER_NAME
from dishka.integrations.base import wrap_injection


def inject_getter(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda _, p: p[CONTAINER_NAME],
        is_async=True,
        remove_depends=True,
    )


def inject_handler(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda p, _: p[2].middleware_data[CONTAINER_NAME],
        is_async=True,
        remove_depends=True,
    )


def inject_on_dialog_event(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda p, _: p[1].middleware_data[CONTAINER_NAME],
        is_async=True,
        remove_depends=True,
    )
