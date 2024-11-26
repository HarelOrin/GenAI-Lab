# cache_client.py

import logging

import kryon_config_client
import nintex_secrets
import ntx_cache


class CacheClient:
    def __init__(self):
        secrets_provider = nintex_secrets.init()
        self.config_client = kryon_config_client.init(secrets_provider=secrets_provider)

        self.cache_client = ntx_cache.init(config_client=self.config_client)

    async def set_status(self, workflow_id, step, code):
        try:
            value = code.value
            key = f"nintex:cache:lab:{workflow_id}:{step}:status"
            cache_inst = self.cache_client.connect()
            cache_inst.set_async(key=key, value=value)
            cache_inst.expire_async(key=key, timeout=600)
            if value >= 400:
                error_key = f"nintex:cache:lab:{workflow_id}:{step}:error"
                cache_inst.set_async(key=error_key, value=code.error)
                cache_inst.expire_async(key=error_key, timeout=600)
            return True
        except Exception as e:
            logging.error(f"Error uploading to cache: {e}")
            raise (f"Error uploading to cache {e}")

    async def check_status(self, workflow_id, step):
        try:
            key = f"nintex:cache:lab:{workflow_id}:{step}:status"
            cache_inst = self.cache_client.connect(mode="ro")
            value = int(cache_inst.get_async(key=key))
            res = {"code": value}
            if value >= 400:
                error_key = f"nintex:cache:lab:{workflow_id}:{step}:error"
                error = cache_inst.get_async(key=error_key)
                res["error"] = error
            return res

        except Exception as e:
            print(f"Error: {e}")
            return False


# Usage example
if __name__ == "__main__":
    client = CacheClient()
    workflow_id = "123"
    step = "hey"
    client.set_status(workflow_id, step, 200)
    resp = client.check_status(workflow_id, step)
    print(resp)
