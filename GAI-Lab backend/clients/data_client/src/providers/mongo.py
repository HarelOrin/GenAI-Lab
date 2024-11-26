import http
import logging
import os

import motor.motor_asyncio

from .base import DbBaseProvider

logger = logging.getLogger()


class MongoProvider(DbBaseProvider):

    def __init__(self, config: dict):
        self.client = None
        # Specify the database and collection for file uploads
        self.database_name = config.get("db_name")
        self.project_name = config.get("collections")["projects"]
        self.result_name = config.get("collections")["results"]
        self.entries_name = config.get("collections")["entries"]
        self.temp_input_name = "temp_proc_capt_input"
        host = config.get("host")
        port = config.get("port")
        username = config.get("username")
        password = config.get("password")
        file_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(file_path)
        tsa_path = os.path.join(script_dir, "mongo_certificate.pem")
        self.connection_dict = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "tls": True,
            "tlsCAFile": tsa_path,
            "retryWrites": False,
            "serverSelectionTimeoutMS": 5000,
        }

    async def get_client(self) -> motor.motor_asyncio.AsyncIOMotorClient:
        if not self.client:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(**self.connection_dict)
            # Send a ping to confirm a successful connection
            try:
                self.client.admin.command("ping")

                logger.info("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                logger.error(f"Error when connecting to mongo: {e}")
                raise
        return self.client

    async def get_output(self, workflow_id: str, step: str) -> dict:
        try:
            client_instance = await self.get_client()
            file_collection = client_instance[self.database_name][self.entries_name]
            result = await file_collection.find_one(
                filter={"workflow_id": workflow_id, "step": step}, projection={"_id": 0}
            )
            response = result["output"]
            response["output_type"] = result["output_type"]
            return response
        except Exception as e:
            logger.error(f"Error when getting output from mongo: {e}")
            raise

    async def upload_entry(self, data: dict, code: http.HTTPStatus):
        try:
            client_instance = await self.get_client()
            file_collection = client_instance[self.database_name][self.entries_name]
            unique_id = f"{data['workflow_id']}_{data['step']}"
            await file_collection.update_one({"_id": unique_id}, {"$set": data}, upsert=True)
            return code
        except Exception as e:
            logger.error(f"Error while uploading project: {e}")
            return {"value": http.HTTPStatus.SERVICE_UNAVAILABLE, "error": f"Error while uploading project: {e}"}

    async def upload_project(self, data: dict):
        client_instance = await self.get_client()
        file_collection = client_instance[self.database_name][self.project_name]
        await file_collection.insert_one(data)

    async def get_project(self, id: str = None) -> list[dict]:
        client_instance = await self.get_client()
        file_collection = client_instance[self.database_name][self.project_name]
        cursor = file_collection.find(filter={"id": id} if id else {}, projection={"_id": 0})
        data = await cursor.to_list(length=None)
        return data

    async def send_feedback(
        self,
        requestId: str,
        feedbackType: str,
        description: str = None,
        email: str = None,
    ):
        client_instance = await self.get_client()
        file_collection = client_instance[self.database_name][self.result_name]

        input_feedback = {"feedbackType": feedbackType}
        if description:
            input_feedback["description"] = description
        if email:
            input_feedback["email"] = email

        await file_collection.update_one(
            {"requestID": requestId},
            {"$set": {"feedback": input_feedback}},
            upsert=False,
        )

        return {"status": "success"}

    async def upload_result(self, data: dict):
        try:
            client_instance = await self.get_client()
            file_collection = client_instance[self.database_name][self.result_name]
            await file_collection.insert_one(data)
        except Exception as e:
            logger.error(f"Error when uploading result to mongo: {e}")

    async def upload_input(self, data: dict):
        try:
            client_instance = await self.get_client()
            file_collection = client_instance[self.database_name][self.temp_input_name]
            await file_collection.insert_one(data)
        except Exception as e:
            logger.error(f"Error when uploading input to mongo: {e}")

    async def get_result(self, request_id: str) -> dict:
        client_instance = await self.get_client()
        file_collection = client_instance[self.database_name][self.result_name]
        result = await file_collection.find_one(filter={"requestID": request_id}, projection={"_id": 0})
        return result or {}


def init(config: dict):
    return MongoProvider(config=config)
