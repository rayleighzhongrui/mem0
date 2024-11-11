UPDATE_MEMORY_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "update_graph_memory",
        "description": "更新知识图谱中已存在的关系",
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ]
                    }
                }
            },
            "required": ["entities"]
        }
    }
}

ADD_MEMORY_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "add_graph_memory",
        "description": "添加新的实体和关系到知识图谱中",
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ]
                    }
                }
            },
            "required": ["entities"]
        }
    }
}

NOOP_TOOL = {
    "type": "function",
    "function": {
        "name": "noop",
        "description": "不需要对知识图谱进行任何操作",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                }
            },
            "required": ["entities"]
        }
    }
}

ADD_MESSAGE_TOOL = {
    "type": "function",
    "function": {
        "name": "add_query",
        "description": "添加新的实体和关系到图谱中",
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ]
                    }
                }
            },
            "required": ["entities"]
        }
    }
}

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "在知识图谱中搜索节点和关系",
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["entities"],
            "additionalProperties": False
        }
    }
}

ADD_MEMORY_STRUCT_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "add_graph_memory",
        "description": "添加新的实体和关系到知识图谱中",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["entities"],
            "additionalProperties": False
        }
    }
}

UPDATE_MEMORY_STRUCT_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "update_graph_memory",
        "description": "更新知识图谱中已存在的关系",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["entities"],
            "additionalProperties": False
        }
    }
}

NOOP_STRUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "noop",
        "description": "Do nothing when no updates are needed",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "skipped_entities": {
                    "type": "array",
                    "description": "List of entities that were skipped",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["skipped_entities"],
            "additionalProperties": False
        }
    }
}

ADD_MESSAGE_STRUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "add_query",
        "description": "添加新的实体和关系到图谱中",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ],
                        "additionalProperties": False,
                    }
                }
            },
            "required": ["entities"],
            "additionalProperties": False
        }
    }
}

SEARCH_STRUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "在知识图谱中搜索节点和关系",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "source_type": {"type": "string"},
                            "source_properties": {
                                "type": "object",
                                "description": "源节点的附加属性",
                                "additionalProperties": True
                            },
                            "relationship": {"type": "string"},
                            "relation_properties": {
                                "type": "object",
                                "description": "关系的附加属性",
                                "additionalProperties": True
                            },
                            "destination": {"type": "string"},
                            "destination_type": {"type": "string"},
                            "destination_properties": {
                                "type": "object",
                                "description": "目标节点的附加属性",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "source",
                            "source_type",
                            "relationship",
                            "destination",
                            "destination_type"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["entities"],
            "additionalProperties": False
        }
    }
}
