import logging

try:
    from langchain_community.graphs import Neo4jGraph
except ImportError:
    raise ImportError("langchain_community is not installed. Please install it using pip install langchain-community")

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    raise ImportError("rank_bm25 is not installed. Please install it using pip install rank-bm25")

from mem0.graphs.tools import (
    ADD_MEMORY_STRUCT_TOOL_GRAPH,
    ADD_MEMORY_TOOL_GRAPH,
    ADD_MESSAGE_STRUCT_TOOL,
    ADD_MESSAGE_TOOL,
    NOOP_STRUCT_TOOL,
    NOOP_TOOL,
    SEARCH_STRUCT_TOOL,
    SEARCH_TOOL,
    UPDATE_MEMORY_STRUCT_TOOL_GRAPH,
    UPDATE_MEMORY_TOOL_GRAPH,
)
from mem0.graphs.utils_en import EXTRACT_ENTITIES_PROMPT, get_update_memory_messages
from mem0.utils.factory import EmbedderFactory, LlmFactory

logger = logging.getLogger(__name__)


class MemoryGraph:
    def __init__(self, config):
        self.config = config
        self.graph = Neo4jGraph(
            self.config.graph_store.config.url,
            self.config.graph_store.config.username,
            self.config.graph_store.config.password,
        )
        self.embedding_model = EmbedderFactory.create(self.config.embedder.provider, self.config.embedder.config)

        self.llm_provider = "openai_structured"
        if self.config.llm.provider:
            self.llm_provider = self.config.llm.provider
        if self.config.graph_store.llm:
            self.llm_provider = self.config.graph_store.llm.provider

        self.llm = LlmFactory.create(self.llm_provider, self.config.llm.config)
        self.user_id = None
        self.threshold = 0.7

    def add(self, data, filters):
        """
        Adds data to the graph.

        Args:
            data (str): The data to add to the graph.
            filters (dict): A dictionary containing filters to be applied during the addition.
        """

        # retrieve the search results
        search_output = self._search(data, filters)

        if self.config.graph_store.custom_prompt:
            messages = [
                {
                    "role": "system",
                    "content": EXTRACT_ENTITIES_PROMPT.replace("USER_ID", self.user_id).replace(
                        "CUSTOM_PROMPT", f"4. {self.config.graph_store.custom_prompt}"
                    ),
                },
                {"role": "user", "content": data},
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": EXTRACT_ENTITIES_PROMPT.replace("USER_ID", self.user_id),
                },
                {"role": "user", "content": data},
            ]

        _tools = [ADD_MESSAGE_TOOL]
        if self.llm_provider in ["azure_openai_structured", "openai_structured"]:
            _tools = [ADD_MESSAGE_STRUCT_TOOL]

        extracted_entities = self.llm.generate_response(
            messages=messages,
            tools=_tools,
        )

        if extracted_entities["tool_calls"]:
            extracted_entities = extracted_entities["tool_calls"][0]["arguments"]["entities"]
        else:
            extracted_entities = []

        logger.debug(f"Extracted entities: {extracted_entities}")
        logger.debug(f"Search output: {search_output}")
        update_memory_prompt = get_update_memory_messages(search_output, extracted_entities)
        _tools = [UPDATE_MEMORY_TOOL_GRAPH, ADD_MEMORY_TOOL_GRAPH, NOOP_TOOL]
        if self.llm_provider in ["azure_openai_structured", "openai_structured"]:
            _tools = [
                UPDATE_MEMORY_STRUCT_TOOL_GRAPH,
                ADD_MEMORY_STRUCT_TOOL_GRAPH,
                NOOP_STRUCT_TOOL,
            ]
        logger.debug(f"Update memory prompt: {update_memory_prompt}")
        memory_updates = self.llm.generate_response(
            messages=update_memory_prompt,
            tools=_tools,
        )
        logger.debug(f"Memory updates: {memory_updates}")
        to_be_added = []
        updated_entities = []
        for item in memory_updates["tool_calls"]:
            if item["name"] == "add_graph_memory":
                to_be_added.append(item["arguments"])
            elif item["name"] == "update_graph_memory":
                for entity in item["arguments"]["entities"]:
                    updated_entity = self._update_relationship(
                        entity["source"],
                        entity["destination"],
                        entity["relationship"],
                        filters,
                    )
                    updated_entities.append(updated_entity)
            elif item["name"] == "noop":
                continue

        returned_entities = []
        
        for item in to_be_added:
            for entity in item["entities"]:
                source = entity["source"].lower().replace(" ", "_")
                source_type = entity["source_type"].lower().replace(" ", "_")
                relation = entity["relationship"].lower().replace(" ", "_")
                destination = entity["destination"].lower().replace(" ", "_")
                destination_type = entity["destination_type"].lower().replace(" ", "_")

                # 获取外属性
                source_props = entity.get("source_properties", {})
                relation_props = entity.get("relation_properties", {})
                dest_props = entity.get("destination_properties", {})

                # 创建嵌入向量
                source_embedding = self.embedding_model.embed(source)
                dest_embedding = self.embedding_model.embed(destination)

                # 构建基础属性
                base_source_props = {
                    "name": source,
                    "user_id": filters["user_id"],
                    "embedding": source_embedding,
                    "created": "timestamp()"
                }
                base_dest_props = {
                    "name": destination,
                    "user_id": filters["user_id"],
                    "embedding": dest_embedding,
                    "created": "timestamp()"
                }
                base_rel_props = {
                    "created": "timestamp()"
                }

                # 合并属性
                source_props.update(base_source_props)
                dest_props.update(base_dest_props)
                relation_props.update(base_rel_props)

                # 构建属性字符串
                source_props_str = ", ".join(f"{k}: ${k}" for k in source_props.keys())
                dest_props_str = ", ".join(f"{k}: ${k}" for k in dest_props.keys())
                rel_props_str = ", ".join(f"{k}: ${k}" for k in relation_props.keys())

                # 更新 Cypher 查询
                cypher = f"""
                MERGE (n:{source_type} {{name: $source_name, user_id: $user_id}})
                ON CREATE SET n = {{{source_props_str}}}
                ON MATCH SET n.embedding = $source_embedding
                MERGE (m:{destination_type} {{name: $dest_name, user_id: $user_id}})
                ON CREATE SET m = {{{dest_props_str}}}
                ON MATCH SET m.embedding = $dest_embedding
                MERGE (n)-[rel:{relation}]->(m)
                ON CREATE SET rel = {{{rel_props_str}}}
                RETURN n, rel, m
                """

                # 合并所有参数
                params = {
                    **source_props,
                    **dest_props,
                    **relation_props,
                    "source_name": source,
                    "dest_name": destination,
                    "user_id": filters["user_id"],
                    "source_embedding": source_embedding,
                    "dest_embedding": dest_embedding
                }

                _ = self.graph.query(cypher, params=params)

                # 过滤掉 embedding 数据
                filtered_source_props = {k: v for k, v in source_props.items() if k != "embedding"}
                filtered_dest_props = {k: v for k, v in dest_props.items() if k != "embedding"}
                filtered_rel_props = {k: v for k, v in relation_props.items() if k != "embedding"}

                # 添加返回结果中，包含过滤后的属性信息
                returned_entities.append({
                    "source": {
                        "name": source,
                        "type": source_type,
                        "properties": filtered_source_props
                    },
                    "relationship": {
                        "type": relation,
                        "properties": filtered_rel_props
                    },
                    "destination": {
                        "name": destination,
                        "type": destination_type,
                        "properties": filtered_dest_props
                    }
                })

        logger.info(f"Added {len(to_be_added)} new memories to the graph")
        logger.debug(f"Returned entities: {returned_entities}")

        # 返回所有操作的结果
        return {
            "added": returned_entities,
            "updated": updated_entities
        }

    def _search(self, query, filters, limit=100):
        _tools = [SEARCH_TOOL]
        if self.llm_provider in ["azure_openai_structured", "openai_structured"]:
            _tools = [SEARCH_STRUCT_TOOL]
        search_results = self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a smart assistant who understands the entities, their types, and relations in a given text. If user message contains self reference such as 'I', 'me', 'my' etc. then use {filters['user_id']} as the source node. Extract the entities.",
                },
                {"role": "user", "content": query},
            ],
            tools=_tools,
        )
        logger.debug(f"Search results from LLM: {search_results}")

        node_list = []
        relation_list = []
        property_dict = {}  # 新增：存储节点和关系的属性

        for item in search_results["tool_calls"]:
            if item["name"] == "search":
                try:
                    for entity in item["arguments"]["entities"]:
                        # 添加源节点和目标节点
                        node_list.extend([entity["source"], entity["destination"]])
                        # 添加关系
                        relation_list.append(entity["relationship"])
                        
                        # 存储属性信息
                        source_key = entity["source"].lower().replace(" ", "_")
                        dest_key = entity["destination"].lower().replace(" ", "_")
                        
                        # 存储节点属性
                        if "source_properties" in entity:
                            property_dict[source_key] = entity["source_properties"]
                        if "destination_properties" in entity:
                            property_dict[dest_key] = entity["destination_properties"]
                            
                        # 存储关系属性
                        if "relation_properties" in entity:
                            rel_key = f"{source_key}_{entity['relationship']}_{dest_key}"
                            property_dict[rel_key] = entity["relation_properties"]
                            
                except Exception as e:
                    logger.error(f"Error in search tool: {e}")

        # 去重
        node_list = list(set(node_list))
        logger.debug(f"Original node_list: {node_list}")
        logger.debug(f"filters['user_id']: {filters['user_id']}")
        
        # 过滤掉 user_id
        filtered_list = [node for node in node_list if node != filters["user_id"]]
        
        # 格式化
        node_list = [node.lower().replace(" ", "_") for node in filtered_list]
        
        logger.debug(f"Processed node_list (removed user_id): {node_list}")

        relation_list = list(set(relation_list))

        node_list = [node.lower().replace(" ", "_") for node in node_list]
        relation_list = [relation.lower().replace(" ", "_") for relation in relation_list]
        logger.debug(f"Node list for search query : {node_list}")

        result_relations = []

        for node in node_list:
            n_embedding = self.embedding_model.embed(node)
            
            # 更新 Cypher 查询以包含属性
            cypher_query = """
            MATCH (n)
            WHERE n.embedding IS NOT NULL AND n.user_id = $user_id
            WITH n,
                round(reduce(dot = 0.0, i IN range(0, size(n.embedding)-1) | dot + n.embedding[i] * $n_embedding[i]) /
                (sqrt(reduce(l2 = 0.0, i IN range(0, size(n.embedding)-1) | l2 + n.embedding[i] * n.embedding[i])) *
                sqrt(reduce(l2 = 0.0, i IN range(0, size($n_embedding)-1) | l2 + $n_embedding[i] * $n_embedding[i]))), 4) AS similarity
            WHERE similarity >= $threshold
            MATCH (n)-[r]->(m)
            RETURN 
                n.name AS source,
                labels(n)[0] AS source_type,
                type(r) AS relationship_type,
                m.name AS destination,
                labels(m)[0] AS destination_type,
                similarity
            UNION
            MATCH (n)
            WHERE n.embedding IS NOT NULL AND n.user_id = $user_id
            WITH n,
                round(reduce(dot = 0.0, i IN range(0, size(n.embedding)-1) | dot + n.embedding[i] * $n_embedding[i]) /
                (sqrt(reduce(l2 = 0.0, i IN range(0, size(n.embedding)-1) | l2 + n.embedding[i] * n.embedding[i])) *
                sqrt(reduce(l2 = 0.0, i IN range(0, size($n_embedding)-1) | l2 + $n_embedding[i] * $n_embedding[i]))), 4) AS similarity
            WHERE similarity >= $threshold
            MATCH (m)-[r]->(n)
            RETURN 
                m.name AS source,
                labels(m)[0] AS source_type,
                type(r) AS relationship_type,
                n.name AS destination,
                labels(n)[0] AS destination_type,
                similarity
            ORDER BY similarity DESC
            LIMIT $limit
            """
            #LIMIT $limit
            params = {
                "n_embedding": n_embedding,
                "threshold": self.threshold,
                "user_id": filters["user_id"],
                "limit": limit,
            }
                   # 添加详细的查询日志
            logger.debug(f"Executing cypher query for node {node}:")
            logger.debug(f"Query: {cypher_query}") 
            results = self.graph.query(cypher_query, params=params)
            logger.debug(f"Query results: {results}")
            
            for result in results:
                result_relations.append({
                    "source": result["source"],
                    "source_type": result["source_type"],
                    "relation": result["relationship_type"],
                    "destination": result["destination"],
                    "destination_type": result["destination_type"],
                    "similarity": result["similarity"]
                })

        return result_relations

    def search(self, query, filters, limit=100):
        """
        Search for memories and related graph data.

        Args:
            query (str): Query to search for.
            filters (dict): A dictionary containing filters to be applied during the search.
            limit (int): The maximum number of nodes and relationships to retrieve. Defaults to 100.

        Returns:
            dict: A dictionary containing:
                - "contexts": List of search results from the base data store.
                - "entities": List of related graph data based on the query.
        """

        search_output = self._search(query, filters, limit)

        if not search_output:
            return []

        search_outputs_sequence = [[item["source"], item["relation"], item["destination"]] for item in search_output]
        bm25 = BM25Okapi(search_outputs_sequence)

        tokenized_query = query.split(" ")
        reranked_results = bm25.get_top_n(tokenized_query, search_outputs_sequence, n=5)

        search_results = []
        for item in reranked_results:
            search_results.append({"source": item[0], "relationship": item[1], "target": item[2]})

        logger.info(f"Returned {len(search_results)} search results")

        return search_results

    def delete_all(self, filters):
        cypher = """
        MATCH (n {user_id: $user_id})
        DETACH DELETE n
        """
        params = {"user_id": filters["user_id"]}
        self.graph.query(cypher, params=params)

    def get_all(self, filters, limit=100):
        """
        Retrieves all nodes and relationships from the graph database.
        """
        # 更新查询以获取完整的属性信息
        query = """
        MATCH (n {user_id: $user_id})-[r]->(m {user_id: $user_id})
        RETURN n, type(r) as relationship_type, r, m
        LIMIT $limit
        """
        results = self.graph.query(query, params={"user_id": filters["user_id"], "limit": limit})

        final_results = []
        for result in results:
            # 转换节点和关系的所有属性
            source_node = result["n"]
            relationship = result["r"]
            dest_node = result["m"]
            
            final_results.append({
                "source": {
                    "name": source_node["name"],
                    "type": list(source_node.labels)[0],  # Neo4j节点的第一个标签
                    "properties": dict(source_node)
                },
                "relationship": {
                    "type": result["relationship_type"],
                    "properties": dict(relationship)
                },
                "destination": {
                    "name": dest_node["name"],
                    "type": list(dest_node.labels)[0],
                    "properties": dict(dest_node)
                }
            })

        logger.info(f"Retrieved {len(final_results)} relationships")
        return final_results

    def _update_relationship(self, source, target, relationship, filters):
        """
        Update or create a relationship between two nodes in the graph.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.
            relationship (str): The type of the relationship.
            filters (dict): A dictionary containing filters to be applied during the update.

        Raises:
            Exception: If the operation fails.
        """
        logger.info(f"Updating relationship: {source} -{relationship}-> {target}")

        relationship = relationship.lower().replace(" ", "_")

        # Check if nodes exist and create them if they don't
        check_and_create_query = """
        MERGE (n1 {name: $source, user_id: $user_id})
        MERGE (n2 {name: $target, user_id: $user_id})
        """
        self.graph.query(
            check_and_create_query,
            params={"source": source, "target": target, "user_id": filters["user_id"]},
        )

        # Delete any existing relationship between the nodes
        delete_query = """
        MATCH (n1 {name: $source, user_id: $user_id})-[r]->(n2 {name: $target, user_id: $user_id})
        DELETE r
        """
        self.graph.query(
            delete_query,
            params={"source": source, "target": target, "user_id": filters["user_id"]},
        )

        # Create the new relationship
        create_query = f"""
        MATCH (n1 {{name: $source, user_id: $user_id}}), (n2 {{name: $target, user_id: $user_id}})
        CREATE (n1)-[r:{relationship}]->(n2)
        RETURN n1, type(r) as relationship_type, r, n2
        """
        result = self.graph.query(
            create_query,
            params={"source": source, "target": target, "user_id": filters["user_id"]},
        )

        if not result:
            raise Exception(f"Failed to update or create relationship between {source} and {target}")
        
        # 添加返回结果
        updated_entity = {
            "source": {
                "name": source,
                "type": result[0]["n1"].labels[0],
                "properties": dict(result[0]["n1"])
            },
            "relationship": {
                "type": result[0]["relationship_type"],
                "properties": dict(result[0]["r"])
            },
            "destination": {
                "name": target,
                "type": result[0]["n2"].labels[0],
                "properties": dict(result[0]["n2"])
            }
        }
        
        return updated_entity
