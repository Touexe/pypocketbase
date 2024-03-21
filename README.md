# pypocketbase

About
Unofficial Async PocketBase client for python. Built on top of aiohttp and pydantic.

This is early development which I've made to to suit my needs with only basic functionalities :

- user and admin auth
- record crud operation
- More coming soon....

## Installation

Latest GitHub main branch version:

```bash
pip install git+https://github.com/Touexe/pypocketbase
```

## Usage
You would likely find this similar to the js sdk. You are right! Just a bit change

```python
import asyncio

from pypocketbase import Pocketbase
from pypocketbase.utils import ParamsList, ParamsOne
from pypocketbase.models import ListResult


async def _main():
    async with Pocketbase(url="http://127.0.0.1:8090") as client:
        # authenticate as normal user
        user_data = await client.auth_with_password("test", "test")
        # or maybe this as well
        # user_data = await client.users.auth_with_password("test", "test")

        # or as admin
        admin_data = await client.auth_with_password(
            "test@example.com", "0123456789", as_admin=True
        )
        # or maybe this one
        # admin_data = client.admins.auth_with_password("test@example.com", "0123456789")

        # list and filter "invoices" collection records
        list_result : ListResult = await client.collection("invoices").list(
            ParamsList(
                page=1,
                size=10,
                filter='status = "pending" && created > "2024-02-08 06:00:00"',
            )
        )
        print(list_result)
        
        # get one record from "invoices" collection
        one_result = await client.collection("invoices").get_one(id= "xdjbc7odieru6b2")
        print(one_result)
        
        # create a record in "invoices" collection
        created_result = await client.collection("invoices").create({
            "amount": 1000,
            "status": "pending",
            "issuer":"Person A",
            "recipient":"Person B",
        })
        
        print(created_result)


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    main()

```

You can use Rust like `Result` type,So you can have nice error return without `exception` thrown at you. Thanks to [result](https://github.com/rustedpy/result) ✨ 

Learn more at : [https://github.com/rustedpy/result](https://github.com/rustedpy/result)
```python
async with Pocketbase(url="http://127.0.0.1:8090", use_result=True) as client:
        result = await client.collection("invoices").list(
            ParamsList(
                page=1,
                size=10,
                filter='status = "pending" && created > "2024-02-08 06:00:00"',
            )
        )
        print(result.ok_value)
        print(result.err_value)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/Touexe/pypocketbase/blob/main/LICENSE)
