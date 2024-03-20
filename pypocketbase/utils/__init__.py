__all__ = ["encode_params", "as_result", "params", "errors"]

import functools
import inspect
from typing import Type, TypeVar
from urllib.parse import quote, urlencode

from result import Err, Ok

from .params import ParamsList, ParamsOne


def encode_params(params: dict) -> str:
    return urlencode(params, safe="~()*!.'\"")


TBE = TypeVar("TBE", bound=BaseException)


def as_result(*exceptions: Type[TBE]):
    """
    Decorator for service methods that should return a Result type if service class has use_result set to True.
    This is a re implementation of the as_result decorator from the result library to support async methods and custom needs.
    """
    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException)
        for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            service_class = args[0] if hasattr(args[0], "use_result") else None
            use_result: bool | None = (
                service_class.use_result if service_class else None
            )
            try:
                if use_result is False:
                    return await func(*args, **kwargs)

                return Ok(await func(*args, **kwargs))
            except exceptions as exc:
                if use_result is False:
                    raise exc
                return Err(exc)

        return wrapped

    return wrapper
