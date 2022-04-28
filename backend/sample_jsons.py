# here are the prototypes of the response json files. I can then modify them on the fly to include my answers

SAMPLE_TEXT_JSON = {
    "fulfillmentText": "Text",
    "dgs_videos": {
        "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
        "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
        "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
    }
}

SAMPLE_CONTEXT_JSON = {
    "fulfillmentText": "Setting Context",
    "outputContexts": [
        {
            "name": "projects/kommkrake-pcsi/locations/global/agent/sessions/session-id/contexts/context-name",
            "lifespanCount": 50,
            "parameters": {}
        }
    ]
}
SAMPLE_CHIP_W_CONTEXT_JSON = {
    "fulfillmentText": "Suggestion Chips",
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    ""
                ]
            }
        },
        {
            "payload": {
                "dgs_videos": {
                    "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
                    "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
                    "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
                },
                "richContent": [
                    [
                        {
                            "options": [
                                {
                                    "text": "Chip1"
                                }
                            ],
                            "type": "chips"
                        }
                    ]
                ]
            }
        }
    ],
    "outputContexts": [
        {
            "name": "projects/kommkrake-pcsi/locations/global/agent/sessions/session-id/contexts/context-name",
            "lifespanCount": 50,
            "parameters": {}
        }
    ]
}

SAMPLE_CHIP_JSON = {
    "fulfillmentText": "Suggestion Chips",
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    ""
                ]
            }
        },
        {
            "payload": {
                "dgs_videos": {
                    "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
                    "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
                    "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
                },
                "richContent": [
                    [
                        {
                            "options": [
                                {
                                    "text": "Chip1"
                                }
                            ],
                            "type": "chips"
                        }
                    ]
                ]
            }
        }
    ]
}

SAMPLE_IMAGE_JSON = {
    "fulfillmentText": "Image",
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    ""
                ]
            }
        },
        {
            "payload": {
                "dgs_videos": {
                    "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
                    "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
                    "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
                },
                "richContent": [
                    [
                        {
                            "type": "image",
                            "rawUrl": "https://upload.wikimedia.org/wikipedia/commons/8/8c/DGS.svg",
                            "accessibilityText": "accessibilityText"
                        },
                        {
                            "type": "info",
                            "title": "",
                            "subtitle": ""
                        },
                        {
                            "type": "chips",
                            "options": [
                                {
                                    "text": "Chip1"
                                },
                            ]
                        }
                    ]
                ]
            }
        }
    ]
}
SAMPLE_EVENT_SCHEDULE_JSON = {
    "fulfillmentText": "Event Schedule",
    "fulfillmentMessages": [
        {"text": {"text": [""]}
         },
        {
            "payload": {
                "dgs_videos": {
                    "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
                    "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
                    "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
                },
                "richContent": [
                    [
                        {
                            "type": "info",
                            "title": "Info item title",
                            "subtitle": "Info item subtitle",
                            "image": {
                                "src": {
                                    "rawUrl": "https://example.com/images/logo.png"
                                }
                            },
                            "actionLink": "https://example.com"
                        }
                    ],
                    [{"type": "chips", "options": [{"text": "Chip1"}]}]
                ],
                "plays": {}
            }
        }
    ]
}
SAMPLE_EVENT_JSON_1 = {
    "fulfillmentText": "Event",
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    ""
                ]
            }
        },
        {
            "payload": {
                "dgs_videos": {
                    "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
                    "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
                    "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
                },
                "richContent": [
                    [
                        {
                            "type": "image",
                            "rawUrl": ""
                        },
                        {
                            "type": "info",
                            "title": "",
                            "subtitle": ""
                        },
                        {
                            "type": "accordion",
                            "title": "",
                            "subtitle": "",
                            "image": {
                                "src": {
                                    "rawUrl": ""
                                }
                            },
                            "text": ""
                        },
                        {
                            "type": "accordion",
                            "title": "",
                            "subtitle": "",
                            "image": {
                                "src": {
                                    "rawUrl": ""
                                }
                            },
                            "text": ""
                        },
                        {
                            "type": "button",
                            "icon": {
                                "type": "chevron_right",
                                "color": "#FF9800"
                            },
                            "text": "Tickets kaufen",
                            "link": "https://sommerblut.de"
                        }
                    ],
                    [
                        {
                            "type": "chips",
                            "options": [
                                {
                                    "text": "Chip1"
                                }
                            ]
                        }
                    ]
                ],
                "event": {}
            }
        }
    ],
    "outputContexts": [
        {
            "name": "projects/kommkrake-pcsi/locations/global/agent/sessions/session-id/contexts/context-name",
            "lifespanCount": 50,
            "parameters": {}
        }
    ]
}

SAMPLE_BUTTON_JSON = {
    "fulfillmentText": "Suggestion Chips",
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    ""
                ]
            }
        },
        {
            "payload": {
                "dgs_videos": {
                    "0": "https://www.youtube.com/watch?v=lyW1kKlPanE",
                    "1": "https://www.youtube.com/watch?v=dCxgF5ISJGg",
                    "2": "https://www.youtube.com/watch?v=e5eblW5mRsU"
                },
                "richContent": [
                    [
                        {
                            "type": "button",
                            "icon": {
                                "type": "chevron_right",
                                "color": "#FF9800"
                            },
                            "text": "Button text",
                            "link": "https://example.com",
                            "event": {
                                "name": "",
                                "languageCode": "",
                                "parameters": {}
                            }
                        },
                        {
                            "options": [
                                {
                                    "text": "Chip1"
                                }
                            ],
                            "type": "chips"
                        }
                    ]
                ]
            }
        }
    ]
}
