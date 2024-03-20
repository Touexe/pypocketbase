from urllib.parse import quote

import aiohttp
from result import Result

from pypocketbase.models.auth import UserAuthResponse
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


class RecordService:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        collection_id_or_name: str,
        use_result: bool = False,
    ) -> None:
        self.session = session
        self.collection_id_or_name = collection_id_or_name
        self.use_result = use_result

    def base_crud_path(self) -> str:
        return self.base_collection_path() + "/records"

    def base_collection_path(self) -> str:
        """Returns the current collection service base path."""
        return "/api/collections/" + quote(self.collection_id_or_name)

    @as_result(UnknownError, RecordNotFound)
    async def get_one(
        self, id: str, params: ParamsOne | None = None
    ) -> Record | Result[Record, RecordNotFound | UnknownError]:
        exception_code = {404: RecordNotFound}
        known_codes = (200, 404)
        params = params.model_dump() if params else {}
        url = self.base_crud_path() + "/" + id + "?" + encode_params(params)

        async with self.session.get(url=url) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=params,
            )
            json_response = await response.json()

        return Record(**json_response)

    @as_result(UnknownError, BadRequest)
    async def list(
        self, params_list: ParamsList | None = None
    ) -> ListResult | Result[ListResult, UnknownError | BadRequest]:
        exception_code = {400: BadRequest}
        known_codes = (200, 400)
        params = params_list.model_dump() if params_list else {}
        url = self.base_crud_path() + "?" + encode_params(params)

        async with self.session.get(url=url) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=params,
            )
            json_response = await response.json()

        return ListResult(**json_response)

    @as_result(UnknownError, RecordNotCreate)
    async def create(
        self, body: dict = {}, params: ParamsOne | None = None
    ) -> Record | Result[Record, RecordNotCreate | UnknownError]:
        exception_code = {400: RecordNotCreate, 403: PermissionError}
        known_codes = (200, 400, 403)
        params = params.model_dump() if params else {}
        url = self.base_crud_path() + "?" + encode_params(params)
        async with self.session.post(url, json=body) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=body,
            )
            json_response = await response.json()

        return Record(**json_response)

    @as_result(UnknownError, RecordNotUpdate)
    async def update(
        self, record_id: str, body: dict, params: ParamsOne | None = None
    ) -> Record | Result[Record, RecordNotUpdate | UnknownError]:
        exception_code = {
            400: RecordNotUpdate,
            403: PermissionError,
            404: RecordNotFound,
        }
        known_codes = (200, 400, 403, 404)
        params = params.model_dump() if params else {}
        url = self.base_crud_path() + "/" + record_id + "?" + encode_params(params)

        async with self.session.patch(url, json=body) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=body,
            )
            json_response = await response.json()

        return Record(**json_response)

    @as_result(UnknownError, RecordNotDelete)
    async def delete(self, id: str, params: ParamsOne | None = None) -> True:
        exception_code = {
            400: RecordNotDelete,
            403: PermissionError,
            404: RecordNotFound,
        }
        known_codes = (204, 400, 403, 404)
        params = params.model_dump() if params else {}
        url = self.base_crud_path() + "/" + id + "?" + encode_params(params)
        async with self.session.delete(url) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=params,
            )

        return True

    @as_result(UnknownError, FailedAuthentication)
    async def auth_with_password(
        self,
        username_or_email: str,
        password: str,
        body: dict | None = None,
        params: ParamsOne | None = None,
    ) -> UserAuthResponse | Result[
        UserAuthResponse, FailedAuthentication | UnknownError
    ]:
        exception_code = {400: FailedAuthentication}
        known_codes = (200, 400)
        params = params.model_dump() if params else {}
        body = body if body is not None else {}
        body.update({"identity": username_or_email, "password": password})
        url = (
            self.base_collection_path()
            + "/auth-with-password"
            + "?"
            + encode_params(params)
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
        auth_response = UserAuthResponse(**json_response)
        return auth_response

    @as_result(UnknownError, BadRequest)
    async def request_verification(
        self, email: str, body: dict | None = None, params: dict | None = None
    ) -> bool:
        """Sends email verification request."""
        exception_code = {400: BadRequest}
        known_codes = (204, 400)
        body = body if body is not None else {}
        params = params if params is not None else {}

        body.update({"email": email})
        url = self.base_collection_path() + "/request-verification" "?" + encode_params(
            params
        )

        async with self.session.post(url, json=body) as response:
            await raise_error_from_response(
                response=response,
                known_codes=known_codes,
                exception_code=exception_code,
                input=body,
            )

        return True
