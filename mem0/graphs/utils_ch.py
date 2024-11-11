UPDATE_GRAPH_PROMPT = """
你是一个专门负责图谱记忆管理和优化的AI专家。你的任务是分析现有的图谱记忆和新信息，并更新记忆列表中的关系，以确保知识的最准确、最新和最连贯的表示。

输入:
1. 现有图谱记忆: {existing_memories}
2. 新的图谱记忆: {memory}

请遵循以下规则:
1. 仅在确实需要更新时才使用 update_graph_memory
2. 对于完全新的关系，使用 add_graph_memory
3. 如果不需要任何更改，使用 noop 并提供原因
4. 确保所有输出的实体都包含完整的类型信息
5. 属性信息应该保持一致且有意义
6. 所有实体名称应该使用标准格式

示例输出:

1. 添加新关系:
{
    "name": "add_graph_memory",
    "arguments": {
        "entities": [
            {
                "source": "USER_ID",
                "source_type": "人物",
                "source_properties": {},
                "relationship": "喜欢",
                "relation_properties": {"强度": 8},
                "destination": "跑步",
                "destination_type": "概念",
                "destination_properties": {"领域": "运动"}
            },
            {
                "source": "跑步",
                "source_type": "事件",
                "source_properties": {
                    "类型": "运动",
                    "描述": "在奥森跑步"
                },
                "relationship": "发生于",
                "relation_properties": {},
                "destination": "奥森",
                "destination_type": "地点",
                "destination_properties": {
                    "类型": "公园"
                }
            }
        ]
    }
}

2. 更新已有关系:
{
    "name": "update_graph_memory",
    "arguments": {
        "entities": [
            {
                "source": "USER_ID",
                "source_type": "人物",
                "source_properties": {},
                "relationship": "认识",
                "relation_properties": {
                    "关系": "同事",
                    "亲密度": 8
                },
                "destination": "李华",
                "destination_type": "人物",
                "destination_properties": {}
            }
        ]
    }
}

3. 无需更改:
{
    "name": "noop",
    "arguments": {
        "reason": "现有关系已经是最新的，无需更新",
        "skipped_entities": [
            {
                "source": "USER_ID",
                "source_type": "人物",
                "relationship": "参与",
                "destination": "项目讨论",
                "destination_type": "事件"
            }
        ]
    }
}

注意：
- 每个工具调用必须严格遵循其定义的格式
- 实体名称应该保持一致的格式和大小写
- 关系类型应该使用标准化的描述
- 如果使用 noop，必须提供清晰的原因说明

请仔细检查并确保输出符合工具的结构化要求。
"""

EXTRACT_ENTITIES_PROMPT = """

You are an advanced algorithm designed to extract structured information from text to construct knowledge graphs. Your goal is to capture comprehensive information while maintaining accuracy. Follow these key principles:

1. Extract only explicitly stated information from the text.
2. Identify nodes (entities/concepts), their types, and relationships.
3. Use "USER_ID" as the source node for any self-references (I, me, my, etc.) in user messages.
CUSTOM_PROMPT

Nodes and Types:
- Aim for simplicity and clarity in node representation.
- Use basic, general types for node labels (e.g. "person" instead of "mathematician").

Relationships:
- Use consistent, general, and timeless relationship types.
- Example: Prefer "PROFESSOR" over "BECAME_PROFESSOR".

Entity Consistency:
- Use the most complete identifier for entities mentioned multiple times.
- Example: Always use "John Doe" instead of variations like "Joe" or pronouns.

Strive for a coherent, easily understandable knowledge graph by maintaining consistency in entity references and relationship types.

Adhere strictly to these guidelines to ensure high-quality knowledge graph extraction."""


def get_update_memory_prompt(existing_memories, memory, template):
    return template.format(existing_memories=existing_memories, memory=memory)


def get_update_memory_messages(existing_memories, memory):
    return [
        {
            "role": "user",
            "content": get_update_memory_prompt(existing_memories, memory, UPDATE_GRAPH_PROMPT),
        },
    ]
