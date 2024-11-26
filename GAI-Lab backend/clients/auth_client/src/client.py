import httpx
import kryon_config_client
import nintex_secrets
from jose import jwt
from pydash import get


class AuthClient:
    def __init__(self):
        secrets_provider = nintex_secrets.init()
        config_client = kryon_config_client.init(secrets_provider=secrets_provider)
        aerobase_config = config_client.get_general_config("gai-lab")

        self.AEROBASE_URL = get(aerobase_config, "aerobase.url")
        self.REALM_NAME = get(aerobase_config, "aerobase.realm")
        self.JWKS_URL = f"{self.AEROBASE_URL}/auth/realms/{self.REALM_NAME}/protocol/openid-connect/certs"

    async def get_public_key(self):
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(self.JWKS_URL)
            jwks = response.json()
        return jwks

    async def authenticate(self, token: str):
        try:
            jwks = await self.get_public_key()

            token = token[len("Bearer ") :]
            header = jwt.get_unverified_header(token)
            rsa_key = {}

            for key in jwks["keys"]:
                if key["kid"] == header["kid"]:
                    rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}

            if rsa_key:
                # Verify the token
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience="account",
                    issuer=f"{self.AEROBASE_URL}/auth/realms/{self.REALM_NAME}",
                )
                return payload

        except Exception as e:
            print(e)
            return False
