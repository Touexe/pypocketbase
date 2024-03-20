from enum import StrEnum, auto

from aiohttp.client_reqrep import ClientResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: int
    message: str
    data: dict | None = None
    headers: dict | None = None
    url: str


class PocketbaseException(Exception):
    def __init__(
        self, message: str, response: ErrorResponse, input: dict | None = None
    ) -> None:
        self.message = message
        self.response = response
        self.input = input
        super().__init__(self.message)


class FailedAuthentication(PocketbaseException):
    pass


class PermissionError(PocketbaseException):
    pass


class RecordNotFound(PocketbaseException):
    pass


class RecordNotCreate(PocketbaseException):
    pass


class RecordNotUpdate(PocketbaseException):
    pass


class RecordNotDelete(PocketbaseException):
    pass


class BadRequest(PocketbaseException):
    pass


class UnknownError(PocketbaseException):
    pass


class NotImplementError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


async def raise_error_from_response(
    response: ClientResponse,
    known_codes: tuple[int, ...],
    exception_code: dict[int, PocketbaseException],
    input: dict | None = None,
) -> None:
    """
    This function is used to raise an error from a response object. Return nothing if the response is successful.
    """
    json_response = (
        await response.json() if response.content or response.status != 204 else {}
    )

    if response.status not in known_codes:
        raise UnknownError(
            message="Unknown error",
            response=ErrorResponse(
                code=response.status,
                message="Unknown error",
                url=str(response.url),
                headers=response.headers,
            ),
        )

    if (exception := exception_code.get(response.status)) is not None:
        error_response = ErrorResponse(
            code=response.status,
            message=json_response.get("message"),
            url=str(response.url),
            data=json_response.get("data"),
            headers=response.headers,
        )
        raise exception(
            message=error_response.message,
            response=error_response,
            input=input,
        )
