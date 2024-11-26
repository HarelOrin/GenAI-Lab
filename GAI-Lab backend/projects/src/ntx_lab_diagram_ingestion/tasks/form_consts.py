TAG_METRICS = {
    "schemaType": "mutation",
    "buttons": [{"name": "Convert", "funcName": "convert_visio_to_bpmn", "type": "primary"}],
    "input": {
        "type": "object",
        "title": "Input",
        "objectType": {"first": True},
        "properties": {
            "invisSection": {
                "type": "object",
                "title": "invisSection",
                "objectType": {"invisible": True},
                "properties": {"VisioDiagram": {}},
            }
        },
    },
}

METRIC_CHOICES = [
    "textAnnotation",
    "sequenceFlow",
    "dataObjectReference",
    "dataStoreReference",
    "group",
    "lane",
    "laneSet",
    "participant",
    "subProcess",
    "task",
    "serviceTask",
    "sendTask",
    "receiveTask",
    "manualTask",
    "businessRuleTask",
    "userTask",
    "scriptTask",
    "startEvent",
    "endEvent",
    "intermediateCatchEvent",
    "intermediateThrowEvent",
    "start_or_end_event",
    "exclusiveGateway",
    "parallelGateway",
    "inclusiveGateway",
    "complexGateway",
    "eventBasedGateway",
]
