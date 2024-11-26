PRESENT_SCHEMA = {
    "schemaType": "mutation",
    "buttons": [
        {
            "type": "manipulation",
            "funcName": "update_schema",
            "name": "Regenerate Schema",
        },
        {
            "type": "output",
            "funcName": "generate_app",
        },
    ],
    "input": {
        "type": "object",
        "title": "Input",
        "objectType": {"first": True},
        "properties": {
            "invisSection": {"type": "object", "objectType": {"invisible": True}, "properties": {}},
            "appSchema": {
                "type": "Text-Long",
                "title": "Regenerate Schema",
                "description": "Describe the desired changes for the app's schema (This option will override manual changes!)",
            },
        },
    },
}
