FIRST_TASK = {
    "schemaType": "mutation",
    "buttons": [{"name": "Next", "funcName": "second_task", "type": "primary"}],
    "input": {
        "type": "object",
        "title": "Input",
        "objectType": {"first": True},
        "properties": {
            "invisible": {
                "type": "object",
                "title": "Invisible section",
                "objectType": {"invisible": True},
                "properties": {"InputForSecondTask": {}},
            }
        },
    },
}
