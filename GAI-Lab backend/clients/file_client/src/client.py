# file_client.py

import base64

import kryon_config_client
import nintex_secrets
import nintex_storage


class FileClient:
    def __init__(self):
        secrets_provider = nintex_secrets.init()
        self.config_client = kryon_config_client.init(secrets_provider=secrets_provider)

        self.file_client = nintex_storage.init(config_client=self.config_client, provider_name="aws_s3")

    def upload(self, encoded_file, key, doc_type, tenant_id):
        resp = self.file_client.upload(tenant_id=tenant_id, base64_data=encoded_file, key=key, doc_type=doc_type)
        return f"{tenant_id}/{key}.{doc_type}"

    def download(self, key, doc_type, tenant_id):
        resp = self.file_client.download(tenant_id=tenant_id, key=key, doc_type=doc_type, is_file=False)
        return resp

    def get_base64_file(self, file_path):
        with open(file_path, "rb") as file:
            base64_bytes = base64.b64encode(file.read())
            base64_string = base64_bytes.decode("utf-8")
        return base64_string


# Usage example
if __name__ == "__main__":
    input_path = r"C:\Users\OrinH\Downloads\Postman-win64-Setup.exe"
    key = "big_file"
    doc_type = "exe"
    tenant_id = "GenAiLabTesting"

    client = FileClient()

    encoded_file = client.get_base64_file(input_path)
    resp = client.upload(encoded_file, key, doc_type, tenant_id)
    # resp = client.download(key, doc_type, tenant_id)

    # decoded_resp = base64.b64decode(resp)
    # decoded_resp = decoded_resp.decode("utf-8")

    # output_path = r"C:\Users\OrinH\Downloads\proc-test.json"
    # with open(output_path, "w") as file:
    #     file.write(decoded_resp)

    print(resp)
