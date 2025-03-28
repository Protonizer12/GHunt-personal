from ghunt.objects.base import GHuntCreds
from ghunt.errors import *
import ghunt.globals as gb
from ghunt.objects.apis import GAPI, EndpointConfig
from ghunt.parsers.clientauthconfig import CacBrand

import httpx

from typing import *
import inspect
import json


class ClientAuthConfigHttp(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        
        if not headers:
            headers = gb.config.headers

        base_headers = {}

        headers = {**headers, **base_headers}

        self.hostname = "clientauthconfig.googleapis.com"
        self.scheme = "https"

        self._load_api(creds, headers)

    async def get_brand(self, as_client: httpx.AsyncClient, project_number: int) -> Tuple[bool, CacBrand]:
        endpoint = EndpointConfig(
            name = inspect.currentframe().f_code.co_name,
            verb = "GET",
            data_type = None, # json, data or None
            authentication_mode = None, # sapisidhash, cookies_only, oauth or None
            require_key = "pantheon", # key name, or None
        )
        self._load_endpoint(endpoint)

        base_url = f"/v1/brands/lookupkey/brand/{project_number}"

        params = {
            "readMask": "*",
            "$outputDefaults": True
        }

        req = await self._query(endpoint.name, as_client, base_url, params=params)

        # Parsing
        data = json.loads(req.text)

        brand = CacBrand()
        if "error" in data:
            return False, brand
        
        brand._scrape(data)

        return True, brand