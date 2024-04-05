import aiohttp
from result import Result

from pypocketbase.models.auth import AdminAuthResponse
from pypocketbase.models.list_result import ListResult
from pypocketbase.models.record import Record
from pypocketbase.utils import as_result, encode_params
from pypocketbase.utils.errors import (
    BadRequest,
    ErrorResponse,
    FailedAuthentication,
    RecordNotCreate,
    RecordNotDelete,
    RecordNotFound,
    RecordNotUpdate,
    UnknownError,
    raise_error_from_response,
)
from pypocketbase.utils.params import ParamsList, ParamsOne


class AdminService:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        use_result: bool = False,
    ) -> None:
        self.session = session
        self.use_result = use_result

    def base_crud_path(self) -> str:
        return "/api/admins"

    @as_result(UnknownError, FailedAuthentication)
    async def auth_with_password(
        self,
        username_or_email: str,
        password: str,
        body: dict | None = None,
        params: ParamsOne | None = None,
    ) -> AdminAuthResponse | Result[
        AdminAuthResponse, FailedAuthentication | UnknownError
    ]:
        exception_code = {400: FailedAuthentication}
        known_codes = (200, 400)
        dict_params = params.model_dump() if params else {}
        body = body if body is not None else {}
        body.update({"identity": username_or_email, "password": password})
        url = (
            self.base_crud_path()
            + "/auth-with-password"
            + "?"
            + encode_params(dict_params)
        )
        headers = {"Authorization": ""}
        async with self.session.post(url, json=body, headers=headers) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=body,
            )
            json_response = await response.json()

        self.session.headers.update({"Authorization": json_response["token"]})
        auth_response = AdminAuthResponse(**json_response)
        return auth_response
