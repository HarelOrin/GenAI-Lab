DESCRIBE_PROCESS_ACTIVITIES = {
    "schemaType": "mutation",
    "buttons": [
        {
            "type": "output",
            "funcName": "generate_process_text",
            "output": {"fileType": "txt", "previewType": "text"},
        }
    ],
    "input": {
        "type": "object",
        "title": "Process Activities",
        "objectType": {"first": True},
        "properties": {
            "invisSection": {},
            "Input Guide": {
                "type": "object",
                "objectType": {"horizontal": True},
                "properties": {
                    "Activity Name": {
                        "type": "Text-Display",
                        "title": "Activity Name",
                        "description": "If the name of the activity is incorrect, type the correct name.",
                    },
                    "Activity Relevance": {
                        "type": "Text-Display",
                        "title": "Activity Relevance",
                        "description": "If ticked, the activity is relevant",
                    },
                },
            },
        },
    },
}
