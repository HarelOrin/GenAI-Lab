import argparse
import base64
import io
import json
import os
import re
import sys
import tempfile
import zipfile
from urllib.parse import quote

import ntx_llm_proc_capt
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__)))
from kryon_pd_deepalgo.dataimport.import_sqlite import SqliteClass
from PIL import Image

from projects.src.BaseTask import BaseTask

from .form_consts import DESCRIBE_PROCESS_ACTIVITIES


class describe_process_activities(BaseTask):
    def __init__(self, process_capture_config: dict):
        """
        Initializes the describe_process_activities task.
        Dependencies:
            process_capture_config (dict): The configuration for the process capture project.
                Inputs:
                    RecordingFile (str): The base64 encoded string of SQLite recording from PDDR or Robot+.
                    RoleName (str): The role name of the user.
                    ProcessName (str): The process name.
                    AnalysisMethod (str): The analysis method to use.
                Outputs:
                    process_activities (dict): The activities object output.
                    relevant_actions (dict): The action description dict.
                Forwarded Data:
                    actions_metadata (dict): The metadata of the actions.
                    RoleName (str): The role name of the user.
                    ProcessName (str): The process name.
        """
        super().__init__(
            task_name="describe_process_activities",
            project_name="process_capture",
            output_type="form",
            data_type="tuple",
            is_raw_output_file=False,
        )

        self.config = process_capture_config

    async def execute(
        self, RecordingFile: str, RoleName: str, ProcessName: str, AnalysisMethod: str
    ) -> tuple[dict, dict, dict, str, str]:
        """
        Executes the describe_process_activities task.
        Args:
            RecordingFile (str): The base64 encoded string of SQLite recording from PDDR or Robot+.
            RoleName (str): The role name of the user.
            ProcessName (str): The process name.
            AnalysisMethod (str): The analysis method to use.
        Returns:
            tuple[dict, dict, dict, str, str]: A tuple containing the process_activities, relevant_actions, actions_metadata, RoleName, and ProcessName.
        """
        describer_provider = {
            "Simple": "metadata",
            "EasyOCR": "ocr",
            "Vision LLM": "v_llm",
        }
        self.config["actions_describer_provider"] = describer_provider[AnalysisMethod]

        client = ntx_llm_proc_capt.init(config=self.config)

        kwargs = self._extract_sqlite(RecordingFile)

        relevant_actions, actions_metadata = await client.async_describe_process_actions(
            self._get_images_batch_impl, **kwargs
        )

        process_activities: dict = await client.async_activities_and_tag(
            actions=relevant_actions, process_name=ProcessName
        )

        return process_activities, relevant_actions, actions_metadata, RoleName, ProcessName

    def build_dynamic_form(
        self,
        process_activities: dict,
        relevant_actions: dict,
        actions_metadata: dict,
        RoleName: str,
        ProcessName: str,
    ) -> dict:
        process_activities_encoded = base64.b64encode(json.dumps(process_activities).encode()).decode("utf-8")
        relevant_actions_encoded = base64.b64encode(json.dumps(relevant_actions).encode()).decode("utf-8")
        actions_metadata_encoded = base64.b64encode(json.dumps(actions_metadata).encode()).decode("utf-8")

        # Format raw output
        raw_output = {
            "process_activities": {
                "value": process_activities_encoded,
                "is_file": True,
                "data_type": "json",
            },
            "relevant_actions": {
                "value": relevant_actions_encoded,
                "is_file": True,
                "data_type": "json",
            },
            "actions_count": {
                "value": len(relevant_actions),
                "is_file": False,
                "data_type": "int",
            },
        }

        # Build form sections
        invis_section = {
            "type": "object",
            "objectType": {"invisible": True},
            "properties": {
                "process_activities": {
                    "type": "General-Object",
                    "name": "ProcessActivities",
                    "value": process_activities_encoded,
                },
                "Process Name": {
                    "type": "Text-Short",
                    "name": "ProcessName",
                    "value": ProcessName,
                },
                "Role Name": {
                    "type": "Text-Short",
                    "name": "RoleName",
                    "value": RoleName,
                },
                "ActionsMetadata": {
                    "type": "General-Object",
                    "name": "ActionsMetadata",
                    "value": actions_metadata_encoded,
                },
            },
        }
        activity_tag_section = {}
        for i, activity in enumerate(process_activities):
            activity_tag_section[f"activity_{i}"] = {
                "type": "object",
                "objectType": {"horizontal": True},
                "properties": {
                    f"{i} Name": {
                        "type": "Text-Short",
                        "title": f"{i} Name",
                        "description": activity["activity_desc"],
                        "value": activity["activity_name"],
                    },
                    f"{i} Relevance": {
                        "type": "Boolean",
                        "title": f"{i} Relevance",
                        "value": activity["relevant"],
                    },
                },
            }

        full_form = DESCRIBE_PROCESS_ACTIVITIES
        form = full_form["input"]["properties"]
        form["invis_section"] = invis_section
        for key, value in activity_tag_section.items():
            form[key] = value

        return raw_output, full_form

    def _extract_sqlite(self, sql_byte_data: bytes) -> tuple:
        with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
            temp_input_file.write(sql_byte_data)
            temp_input_file_path = temp_input_file.name

            with tempfile.TemporaryDirectory() as temp_dir_output:

                sqlitepath = temp_input_file_path
                savepath = temp_dir_output
                save_images = True

                parser = argparse.ArgumentParser()
                parser.add_argument("--sqlite_data_path", nargs="?")
                parser.add_argument("--save_path", nargs="?")
                parser.add_argument("--parse_images", nargs="?")

                args = parser.parse_args()

                if args.sqlite_data_path is None:
                    args.sqlite_data_path = sqlitepath

                if args.save_path is None:
                    args.save_path = savepath

                if args.parse_images is None:
                    args.parse_images = save_images

                sqlite_class = SqliteClass()
                _ = sqlite_class.extract_sqlite(args.sqlite_data_path, args.save_path, {})

                output_dir = os.listdir(args.save_path)[0]
                output_dir_path = os.path.join(args.save_path, output_dir)

                # Generate zip file containing images if "png_org" directory exists
                zip_buffer = io.BytesIO()
                if os.path.exists(os.path.join(output_dir_path, "png_org")):
                    with zipfile.ZipFile(zip_buffer, "w") as zipf:
                        png_org_dir = os.path.join(output_dir_path, "png_org")
                        if os.path.exists(png_org_dir):
                            for root, dirs, files in os.walk(png_org_dir):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    zipf.write(
                                        file_path,
                                        os.path.relpath(file_path, png_org_dir),
                                    )

                        # Find the CSV file in the output directory
                        csv_file = [file for file in os.listdir(output_dir_path) if file.endswith(".csv")]
                        if csv_file:
                            csv_path = os.path.join(output_dir_path, csv_file[0])
                            with open(csv_path, "rb") as csv_file:
                                csv_bytes = csv_file.read()
                        else:
                            csv_bytes = b""  # If no CSV file found, return empty bytes
                return {
                    "recording_file": csv_bytes,
                    "actions_images": zip_buffer.getvalue(),
                }

    def _get_images_batch_impl(self, batch_num, batch_size, **kwargs):
        # get data
        recording_file, actions_images = (
            kwargs["recording_file"],
            kwargs["actions_images"],
        )

        data = []
        recording_file_df = pd.read_csv(io.BytesIO(recording_file))
        if "KeyCombinations" in recording_file_df.columns or "Combinations" in recording_file_df.columns:
            # Column 'KeyCombinations' is the name of 'Combinations' in older versions of the PDDR
            recording_file_df.rename(
                columns={"KeyCombinations": "Combinations"},
                inplace=True,
                errors="ignore",
            )
            recording_file_df.set_index("UserActionIndex", inplace=True, drop=False)

            # Formatting of the content of 'Combinations' Old -> New:
            def to_singleton_list(s: str):
                if pd.isna(s):
                    return s
                # If true robot+ if false PDDR
                if ":" in s:
                    items = re.split(r"(?<=\}),(?=\{)", s)
                    output = [
                        json.loads(re.sub(r"'", '"', item).replace("False", "false").replace("True", "true"))
                        for item in items
                    ]
                    return [output]
                else:
                    return [[int(integer)] for integer in s.split(",")]

            recording_file_df["Combinations"] = recording_file_df["Combinations"].apply(lambda s: to_singleton_list(s))
        image_arrays = {}
        # Assume zip_bytes contains the bytes of the zip file
        with zipfile.ZipFile(io.BytesIO(actions_images), "r") as zip_ref:
            for file_name in zip_ref.namelist():
                # Assuming the images are in PNG format
                if file_name.lower().endswith(".png"):
                    with zip_ref.open(file_name) as file:
                        file_idx = file_name.replace(".png", "")
                        img = Image.open(file)
                        img_array = np.array(img)
                        image_arrays[file_idx] = img_array
        for _, row in recording_file_df.iterrows():
            index = int(row["UserActionIndex"])
            if f"{index:06}" in image_arrays.keys():
                row_dict = row.to_dict()
                data.append(
                    {
                        "image": image_arrays[f"{index:06}"],
                        "userAction": row_dict,
                        "actionId": index,
                    }
                )

        start = batch_num * batch_size
        end = min(((batch_num + 1) * batch_size), len(data))
        return data[start:end]
