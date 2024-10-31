UPDATE_MEMORY_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "update_graph_memory",
        "description": "根据新信息更新已有图形记忆中的关系键。当需要修改知识图谱中的现有关系时应调用此功能。仅当新信息比现有信息更新、更准确或提供更多上下文时才执行更新。关系的源节点和目标节点必须与现有图谱记忆中的节点保持一致；只能更新关系本身。",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "要更新关系中的源节点标识符，必须与图中的现有节点匹配。",
                },
                "destination": {
                    "type": "string",
                    "description": "要更新关系中的目标节点标识符，必须与图中的现有节点匹配。",
                },
                "relationship": {
                    "type": "string",
                    "description": "源节点和目标节点之间的新关系或更新后的关系。应简洁、清晰地描述两个节点之间的连接方式。",
                },
            },
            "required": ["source", "destination", "relationship"],
            "additionalProperties": False,
        },
    },
}

ADD_MEMORY_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "add_graph_memory",
        "description": "向知识图谱添加新的图形记忆。此功能在两个节点之间创建新的关系，可能会创建新节点（如果它们不存在的话）。",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "新关系中的源节点标识符，可以是现有节点，也可以是要创建的新节点。",
                },
                "destination": {
                    "type": "string",
                    "description": "新关系中的目标节点标识符，可以是现有节点，也可以是要创建的新节点。",
                },
                "relationship": {
                    "type": "string",
                    "description": "源节点和目标节点之间的关系类型。应简洁、清晰地描述两个节点之间的连接方式。",
                },
                "source_type": {
                    "type": "string",
                    "description": "源节点的类型或类别，有助于在图中对节点进行分类和组织。",
                },
                "destination_type": {
                    "type": "string",
                    "description": "目标节点的类型或类别，有助于在图中对节点进行分类和组织。",
                },
            },
            "required": [
                "source",
                "destination",
                "relationship",
                "source_type",
                "destination_type",
            ],
            "additionalProperties": False,
        },
    },
}

NOOP_TOOL = {
    "type": "function",
    "function": {
        "name": "noop",
        "description": "不对图形实体执行任何操作。当系统确定根据当前输入或上下文不需要任何更改或添加时调用此功能。它在不需要其他操作时作为占位操作，确保系统在不修改图形的情况下明确确认这种情况。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
}

ADD_MESSAGE_TOOL = {
    "type": "function",
    "function": {
        "name": "add_query",
        "description": "根据提供的查询将新实体和关系添加到图形中。",
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source_node": {"type": "string"},
                            "source_type": {"type": "string"},
                            "relation": {"type": "string"},
                            "destination_node": {"type": "string"},
                            "destination_type": {"type": "string"},
                        },
                        "required": [
                            "source_node",
                            "source_type",
                            "relation",
                            "destination_node",
                            "destination_type",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["entities"],
            "additionalProperties": False,
        },
    },
}

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "在图形中搜索节点和关系。",
        "parameters": {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "要搜索的节点列表。",
                },
                "relations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "要搜索的关系列表。",
                },
            },
            "required": ["nodes", "relations"],
            "additionalProperties": False,
        },
    },
}

UPDATE_MEMORY_STRUCT_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "update_graph_memory",
        "description": "根据新信息更新已有图形记忆中的关系键。当需要修改知识图谱中的现有关系时应调用此功能。仅当新信息比现有信息更新、更准确或提供更多上下文时才执行更新。关系的源节点和目标节点必须与现有图谱记忆中的节点保持一致；只能更新关系本身。",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "要更新关系中的源节点标识符，必须与图中的现有节点匹配。",
                },
                "destination": {
                    "type": "string",
                    "description": "要更新关系中的目标节点标识符，必须与图中的现有节点匹配。",
                },
                "relationship": {
                    "type": "string",
                    "description": "源节点和目标节点之间的新关系或更新后的关系。应简洁、清晰地描述两个节点之间的连接方式。",
                },
            },
            "required": ["source", "destination", "relationship"],
            "additionalProperties": False,
        },
    },
}

ADD_MEMORY_STRUCT_TOOL_GRAPH = {
    "type": "function",
    "function": {
        "name": "add_graph_memory",
        "description": "向知识图谱添加新的图形记忆。此功能在两个节点之间创建新的关系，可能会创建新节点（如果它们不存在的话）。",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "新关系中的源节点标识符，可以是现有节点，也可以是要创建的新节点。",
                },
                "destination": {
                    "type": "string",
                    "description": "新关系中的目标节点标识符，可以是现有节点，也可以是要创建的新节点。",
                },
                "relationship": {
                    "type": "string",
                    "description": "源节点和目标节点之间的关系类型。应简洁、清晰地描述两个节点之间的连接方式。",
                },
                "source_type": {
                    "type": "string",
                    "description": "源节点的类型或类别，有助于在图中对节点进行分类和组织。",
                },
                "destination_type": {
                    "type": "string",
                    "description": "目标节点的类型或类别，有助于在图中对节点进行分类和组织。",
                },
            },
            "required": [
                "source",
                "destination",
                "relationship",
                "source_type",
                "destination_type",
            ],
            "additionalProperties": False,
        },
    },
}

NOOP_STRUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "noop",
        "description": "不对图形实体执行任何操作。当系统确定根据当前输入或上下文不需要任何更改或添加时调用此功能。它在不需要其他操作时作为占位操作，确保系统在不修改图形的情况下明确确认这种情况。",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
}

ADD_MESSAGE_STRUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "add_query",
        "description": "根据提供的查询将新实体和关系添加到图形中。",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source_node": {"type": "string"},
                            "source_type": {"type": "string"},
                            "relation": {"type": "string"},
                            "destination_node": {"type": "string"},
                            "destination_type": {"type": "string"},
                        },
                        "required": [
                            "source_node",
                            "source_type",
                            "relation",
                            "destination_node",
                            "destination_type",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["entities"],
            "additionalProperties": False,
        },
    },
}

SEARCH_STRUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "在图形中搜索节点和关系。",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "要搜索的节点列表。",
                },
                "relations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "要搜索的关系列表。",
                },
            },
            "required": ["nodes", "relations"],
            "additionalProperties": False,
        },
    },
}
