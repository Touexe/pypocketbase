import aiohttp
from result import Result
from yarl import URL

from pypocketbase.models.auth import AdminAuthResponse, UserAuthResponse
from pypocketbase.services.admin import AdminService
from pypocketbase.services.record import RecordService
from pypocketbase.utils import as_result
from pypocketbase.utils.errors import (
    FailedAuthentication,
    NotImplementError,
    UnknownError,
)


class Client:
    def __init__(
        self,
        url: str = "http://127.0.0.1:8090",
        token: str | None = None,
        use_result: bool = False,
    ) -> None:
        self.BASE_URL = url
        self.TOKEN = token or ""
        self.HEADERS = {"Authorization": self.TOKEN}
        self.session = self.get_session()
        self.use_result = use_result

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
        self.session = None

    async def close(self):
        await self.session.close()
        self.session = None

    def set_token(self, token: str):
        self.TOKEN = token
        self.HEADERS.update({"Authorization": self.TOKEN})
        self.session = self.get_session()

    def get_session(self) -> aiohttp.ClientSession:
        """
        Starts new session
        """
        return aiohttp.ClientSession(base_url=URL(self.BASE_URL), headers=self.HEADERS)

    def collection(
        self, collection_id_or_name: str, session: aiohttp.ClientSession | None = None
    ) -> RecordService:
        return RecordService(
            session=session or self.session,
            collection_id_or_name=collection_id_or_name,
            use_result=self.use_result,
        )

    @property
    def users(self) -> RecordService:
        return self.collection("users")

    @property
    def admins(self) -> AdminService:
        return AdminService(session=self.session, use_result=self.use_result)

    async def auth_with_password(
        self, username_or_email: str, password: str, as_admin: bool = False
    ) -> UserAuthResponse | Result[
        UserAuthResponse, FailedAuthentication | UnknownError
    ]:
        auth = (
            self.admins.auth_with_password
            if as_admin
            else self.users.auth_with_password
        )
        result = await auth(username_or_email=username_or_email, password=password)

        self.TOKEN = self.session.headers.get("Authorization")
        self.HEADERS.update({"Authorization": self.TOKEN})

        # Note : This is not needed since the session already has been, but worth to be here anyway
        # self.HEADERS.update({"Authorization": self.TOKEN})
        # self.session = self.get_session()

        return result

    @as_result(NotImplementError)
    async def me(
        self,
    ) -> UserAuthResponse | AdminAuthResponse | Result[
        UserAuthResponse | AdminAuthResponse, NotImplementError
    ]:
        """
        This method depends on custom implementation js hook of the /api/me endpoint on Pocketbase
        routerAdd("GET", "/api/me", (c) => {
            const token = c.request().header.get("Authorization")
            const info   = $apis.requestInfo(c);
            const admin  = info.admin;
            const record = info.authRecord;

            const isGuest = !admin && !record
            return c.json(200, { "token": token, "admin": admin, "record": record, "isGuest": isGuest })

        });
        """

        url = "/api/me"
        async with self.session.get(url) as response:
            json_response: dict = await response.json()

            if response.status == 404:
                raise NotImplementError(
                    "LMAO the /api/me endpoint is not implemented on the pocketbase server. Add the hook!"
                )

            record = json_response.get("record")
            admin = json_response.get("admin")

            if record:
                return UserAuthResponse(**json_response)
            if admin:
                return AdminAuthResponse(**json_response)
