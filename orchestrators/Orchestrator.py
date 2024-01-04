from abc import ABC, abstractmethod
import os
import json
import logging
import requests
import copy
from dotenv import load_dotenv

class Orchestrator(ABC):
    load_dotenv()

    DEBUG = os.environ.get("DEBUG", "false")
    DEBUG_LOGGING = DEBUG.lower() == "true"

    @abstractmethod
    def conversation_with_data(self, request_body):
        pass

    @abstractmethod
    def conversation_without_data(self, request_body):
        pass

    # initialize variables
    DATASOURCE_TYPE = os.environ.get("DATASOURCE_TYPE", "AzureCognitiveSearch")
    SEARCH_TOP_K = os.environ.get("SEARCH_TOP_K", 5)
    SEARCH_STRICTNESS = os.environ.get("SEARCH_STRICTNESS", 3)
    SEARCH_ENABLE_IN_DOMAIN = os.environ.get("SEARCH_ENABLE_IN_DOMAIN", "true")

    AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE", 0)
    AZURE_OPENAI_EMBEDDING_ENDPOINT = os.environ.get("AZURE_OPENAI_EMBEDDING_ENDPOINT")
    AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS", 1000)
    AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
    AZURE_OPENAI_TOP_P = os.environ.get("AZURE_OPENAI_TOP_P", 1.0)
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_STOP_SEQUENCE = os.environ.get("AZURE_OPENAI_STOP_SEQUENCE")
    AZURE_OPENAI_STREAM = os.environ.get("AZURE_OPENAI_STREAM", "true")
    AZURE_OPENAI_EMBEDDING_KEY = os.environ.get("AZURE_OPENAI_EMBEDDING_KEY")
    AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
    AZURE_OPENAI_EMBEDDING_NAME = os.environ.get("AZURE_OPENAI_EMBEDDING_NAME", "")
    AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
    AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION", "2023-08-01-preview")
    AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get("AZURE_OPENAI_SYSTEM_MESSAGE", "You are an AI assistant that helps people find information.")

    AZURE_SEARCH_QUERY_TYPE = os.environ.get("AZURE_SEARCH_QUERY_TYPE")
    AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH", "false")
    AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
    AZURE_SEARCH_PERMITTED_GROUPS_COLUMN = os.environ.get("AZURE_SEARCH_PERMITTED_GROUPS_COLUMN")
    AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
    AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
    AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
    AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
    AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
    AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")
    AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
    AZURE_SEARCH_VECTOR_COLUMNS = os.environ.get("AZURE_SEARCH_VECTOR_COLUMNS")
    AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN)
    AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", SEARCH_TOP_K)
    AZURE_SEARCH_STRICTNESS = os.environ.get("AZURE_SEARCH_STRICTNESS", SEARCH_STRICTNESS)

    # CosmosDB Mongo vcore vector db Settings
    AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING")  #This has to be secure string
    AZURE_COSMOSDB_MONGO_VCORE_DATABASE = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_DATABASE")
    AZURE_COSMOSDB_MONGO_VCORE_CONTAINER = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_CONTAINER")
    AZURE_COSMOSDB_MONGO_VCORE_INDEX = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_INDEX")
    AZURE_COSMOSDB_MONGO_VCORE_TOP_K = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_TOP_K", AZURE_SEARCH_TOP_K)
    AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS", AZURE_SEARCH_STRICTNESS)  
    AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN", AZURE_SEARCH_ENABLE_IN_DOMAIN)
    AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS", "")
    AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN")
    AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN")
    AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN")
    AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS")

    # Elasticsearch Integration Settings
    ELASTICSEARCH_ENDPOINT = os.environ.get("ELASTICSEARCH_ENDPOINT")
    ELASTICSEARCH_ENCODED_API_KEY = os.environ.get("ELASTICSEARCH_ENCODED_API_KEY")
    ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX")
    ELASTICSEARCH_QUERY_TYPE = os.environ.get("ELASTICSEARCH_QUERY_TYPE", "simple")
    ELASTICSEARCH_TOP_K = os.environ.get("ELASTICSEARCH_TOP_K", SEARCH_TOP_K)
    ELASTICSEARCH_ENABLE_IN_DOMAIN = os.environ.get("ELASTICSEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN)
    ELASTICSEARCH_CONTENT_COLUMNS = os.environ.get("ELASTICSEARCH_CONTENT_COLUMNS")
    ELASTICSEARCH_FILENAME_COLUMN = os.environ.get("ELASTICSEARCH_FILENAME_COLUMN")
    ELASTICSEARCH_TITLE_COLUMN = os.environ.get("ELASTICSEARCH_TITLE_COLUMN")
    ELASTICSEARCH_URL_COLUMN = os.environ.get("ELASTICSEARCH_URL_COLUMN")
    ELASTICSEARCH_VECTOR_COLUMNS = os.environ.get("ELASTICSEARCH_VECTOR_COLUMNS")
    ELASTICSEARCH_STRICTNESS = os.environ.get("ELASTICSEARCH_STRICTNESS", SEARCH_STRICTNESS)
    ELASTICSEARCH_EMBEDDING_MODEL_ID = os.environ.get("ELASTICSEARCH_EMBEDDING_MODEL_ID")

    SHOULD_STREAM = True if AZURE_OPENAI_STREAM.lower() == "true" else False


    # methods to implement in orchestrator
    def fetchUserGroups(self, userToken, nextLink=None):
    # Recursively fetch group membership
        if nextLink:
            endpoint = nextLink
        else:
            endpoint = "https://graph.microsoft.com/v1.0/me/transitiveMemberOf?$select=id"
        
        headers = {
            'Authorization': "bearer " + userToken
        }
        try :
            r = requests.get(endpoint, headers=headers)
            if r.status_code != 200:
                if self.DEBUG_LOGGING:
                    logging.error(f"Error fetching user groups: {r.status_code} {r.text}")
                return []
            
            r = r.json()
            if "@odata.nextLink" in r:
                nextLinkData = self.fetchUserGroups(userToken, r["@odata.nextLink"])
                r['value'].extend(nextLinkData)
            
            return r['value']
        except Exception as e:
            logging.error(f"Exception in fetchUserGroups: {e}")
            return []
        
    def generateFilterString(self, userToken):
        # Get list of groups user is a member of
        userGroups = self.fetchUserGroups(userToken)

        # Construct filter string
        if not userGroups:
            logging.debug("No user groups found")

        group_ids = ", ".join([obj['id'] for obj in userGroups])
        return f"{AZURE_SEARCH_PERMITTED_GROUPS_COLUMN}/any(g:search.in(g, '{group_ids}'))"

    def format_as_ndjson(obj: dict) -> str:
        return json.dumps(obj, ensure_ascii=False) + "\n"

    def prepare_body_headers_with_data(request):
        request_messages = request.json["messages"]

        body = {
            "messages": request_messages,
            "temperature": float(AZURE_OPENAI_TEMPERATURE),
            "max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
            "top_p": float(AZURE_OPENAI_TOP_P),
            "stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
            "stream": SHOULD_STREAM,
            "dataSources": []
        }

        if DATASOURCE_TYPE == "AzureCognitiveSearch":
            # Set query type
            query_type = "simple"
            if AZURE_SEARCH_QUERY_TYPE:
                query_type = AZURE_SEARCH_QUERY_TYPE
            elif AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG:
                query_type = "semantic"

            # Set filter
            filter = None
            userToken = None
            if AZURE_SEARCH_PERMITTED_GROUPS_COLUMN:
                userToken = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN', "")
                if DEBUG_LOGGING:
                    logging.debug(f"USER TOKEN is {'present' if userToken else 'not present'}")

                filter = generateFilterString(userToken)
                if DEBUG_LOGGING:
                    logging.debug(f"FILTER: {filter}")

            body["dataSources"].append(
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
                        "key": AZURE_SEARCH_KEY,
                        "indexName": AZURE_SEARCH_INDEX,
                        "fieldsMapping": {
                            "contentFields": AZURE_SEARCH_CONTENT_COLUMNS.split("|") if AZURE_SEARCH_CONTENT_COLUMNS else [],
                            "titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
                            "urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
                            "filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None,
                            "vectorFields": AZURE_SEARCH_VECTOR_COLUMNS.split("|") if AZURE_SEARCH_VECTOR_COLUMNS else []
                        },
                        "inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
                        "topNDocuments": AZURE_SEARCH_TOP_K,
                        "queryType": query_type,
                        "semanticConfiguration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
                        "roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE,
                        "filter": filter,
                        "strictness": int(AZURE_SEARCH_STRICTNESS)
                    }
                })
        elif DATASOURCE_TYPE == "AzureCosmosDB":
            # Set query type
            query_type = "vector"

            body["dataSources"].append(
                {
                    "type": "AzureCosmosDB",
                    "parameters": {
                        "connectionString": AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING,
                        "indexName": AZURE_COSMOSDB_MONGO_VCORE_INDEX,
                        "databaseName": AZURE_COSMOSDB_MONGO_VCORE_DATABASE,
                        "containerName": AZURE_COSMOSDB_MONGO_VCORE_CONTAINER,                    
                        "fieldsMapping": {
                            "contentFields": AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS.split("|") if AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS else [],
                            "titleField": AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN if AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN else None,
                            "urlField": AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN if AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN else None,
                            "filepathField": AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN if AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN else None,
                            "vectorFields": AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS.split("|") if AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS else []
                        },
                        "inScope": True if AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN.lower() == "true" else False,
                        "topNDocuments": AZURE_COSMOSDB_MONGO_VCORE_TOP_K,
                        "strictness": int(AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS),
                        "queryType": query_type,
                        "roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE
                    }
                }
            )

        elif DATASOURCE_TYPE == "Elasticsearch":
            body["dataSources"].append(
                {
                    "messages": request_messages,
                    "temperature": float(AZURE_OPENAI_TEMPERATURE),
                    "max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
                    "top_p": float(AZURE_OPENAI_TOP_P),
                    "stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
                    "stream": SHOULD_STREAM,
                    "dataSources": [
                        {
                            "type": "AzureCognitiveSearch",
                            "parameters": {
                                "endpoint": ELASTICSEARCH_ENDPOINT,
                                "encodedApiKey": ELASTICSEARCH_ENCODED_API_KEY,
                                "indexName": ELASTICSEARCH_INDEX,
                                "fieldsMapping": {
                                    "contentFields": ELASTICSEARCH_CONTENT_COLUMNS.split("|") if ELASTICSEARCH_CONTENT_COLUMNS else [],
                                    "titleField": ELASTICSEARCH_TITLE_COLUMN if ELASTICSEARCH_TITLE_COLUMN else None,
                                    "urlField": ELASTICSEARCH_URL_COLUMN if ELASTICSEARCH_URL_COLUMN else None,
                                    "filepathField": ELASTICSEARCH_FILENAME_COLUMN if ELASTICSEARCH_FILENAME_COLUMN else None,
                                    "vectorFields": ELASTICSEARCH_VECTOR_COLUMNS.split("|") if ELASTICSEARCH_VECTOR_COLUMNS else []
                                },
                                "inScope": True if ELASTICSEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
                                "topNDocuments": int(ELASTICSEARCH_TOP_K),
                                "queryType": ELASTICSEARCH_QUERY_TYPE,
                                "roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE,
                                "embeddingEndpoint": AZURE_OPENAI_EMBEDDING_ENDPOINT,
                                "embeddingKey": AZURE_OPENAI_EMBEDDING_KEY,
                                "embeddingModelId": ELASTICSEARCH_EMBEDDING_MODEL_ID,
                                "strictness": int(ELASTICSEARCH_STRICTNESS)
                            }
                        }
                    ]
                }
            )
        else:
            raise Exception(f"DATASOURCE_TYPE is not configured or unknown: {DATASOURCE_TYPE}")

        if "vector" in query_type.lower():
            if AZURE_OPENAI_EMBEDDING_NAME:
                body["dataSources"][0]["parameters"]["embeddingDeploymentName"] = AZURE_OPENAI_EMBEDDING_NAME
            else:
                body["dataSources"][0]["parameters"]["embeddingEndpoint"] = AZURE_OPENAI_EMBEDDING_ENDPOINT
                body["dataSources"][0]["parameters"]["embeddingKey"] = AZURE_OPENAI_EMBEDDING_KEY

        if DEBUG_LOGGING:
            body_clean = copy.deepcopy(body)
            if body_clean["dataSources"][0]["parameters"].get("key"):
                body_clean["dataSources"][0]["parameters"]["key"] = "*****"
            if body_clean["dataSources"][0]["parameters"].get("connectionString"):
                body_clean["dataSources"][0]["parameters"]["connectionString"] = "*****"
            if body_clean["dataSources"][0]["parameters"].get("embeddingKey"):
                body_clean["dataSources"][0]["parameters"]["embeddingKey"] = "*****"
                
            logging.debug(f"REQUEST BODY: {json.dumps(body_clean, indent=4)}")

        headers = {
            'Content-Type': 'application/json',
            'api-key': AZURE_OPENAI_KEY,
            "x-ms-useragent": "GitHubSampleWebApp/PublicAPI/3.0.0"
        }

        return body, headers

    def formatApiResponseNoStreaming(self, rawResponse):
        if 'error' in rawResponse:
            return {"error": rawResponse["error"]}
        response = {
            "id": rawResponse["id"],
            "model": rawResponse["model"],
            "created": rawResponse["created"],
            "object": rawResponse["object"],
            "choices": [{
                "messages": []
            }],
        }
        toolMessage = {
            "role": "tool",
            "content": rawResponse["choices"][0]["message"]["context"]["messages"][0]["content"]
        }
        assistantMessage = {
            "role": "assistant",
            "content": rawResponse["choices"][0]["message"]["content"]
        }
        response["choices"][0]["messages"].append(toolMessage)
        response["choices"][0]["messages"].append(assistantMessage)

        return response
    
    def formatApiResponseStreaming(self, rawResponse):
        if 'error' in rawResponse:
            return {"error": rawResponse["error"]}
        response = {
            "id": rawResponse["id"],
            "model": rawResponse["model"],
            "created": rawResponse["created"],
            "object": rawResponse["object"],
            "choices": [{
                "messages": []
            }],
        }

        if rawResponse["choices"][0]["delta"].get("context"):
            messageObj = {
                "delta": {
                    "role": "tool",
                    "content": rawResponse["choices"][0]["delta"]["context"]["messages"][0]["content"]
                }
            }
            response["choices"][0]["messages"].append(messageObj)
        elif rawResponse["choices"][0]["delta"].get("role"):
            messageObj = {
                "delta": {
                    "role": "assistant",
                }
            }
            response["choices"][0]["messages"].append(messageObj)
        else:
            if rawResponse["choices"][0]["end_turn"]:
                messageObj = {
                    "delta": {
                        "content": "[DONE]",
                    }
                }
                response["choices"][0]["messages"].append(messageObj)
            else:
                messageObj = {
                    "delta": {
                        "content": rawResponse["choices"][0]["delta"]["content"],
                    }
                }
                response["choices"][0]["messages"].append(messageObj)

        return response
        
    
    def stream_with_data(self, body, headers, endpoint, history_metadata={}):
        s = requests.Session()
        try:
            with s.post(endpoint, json=body, headers=headers, stream=True) as r:
                for line in r.iter_lines(chunk_size=10):
                    response = {
                        "id": "",
                        "model": "",
                        "created": 0,
                        "object": "",
                        "choices": [{
                            "messages": []
                        }],
                        "apim-request-id": "",
                        'history_metadata': history_metadata
                    }
                    if line:
                        if AZURE_OPENAI_PREVIEW_API_VERSION == '2023-06-01-preview':
                            lineJson = json.loads(line.lstrip(b'data:').decode('utf-8'))
                        else:
                            try:
                                rawResponse = json.loads(line.lstrip(b'data:').decode('utf-8'))
                                lineJson = formatApiResponseStreaming(rawResponse)
                            except json.decoder.JSONDecodeError:
                                continue

                        if 'error' in lineJson:
                            yield format_as_ndjson(lineJson)
                        response["id"] = lineJson["id"]
                        response["model"] = lineJson["model"]
                        response["created"] = lineJson["created"]
                        response["object"] = lineJson["object"]
                        response["apim-request-id"] = r.headers.get('apim-request-id')

                        role = lineJson["choices"][0]["messages"][0]["delta"].get("role")

                        if role == "tool":
                            response["choices"][0]["messages"].append(lineJson["choices"][0]["messages"][0]["delta"])
                            yield self.format_as_ndjson(response)
                        elif role == "assistant": 
                            if response['apim-request-id'] and DEBUG_LOGGING: 
                                logging.debug(f"RESPONSE apim-request-id: {response['apim-request-id']}")
                            response["choices"][0]["messages"].append({
                                "role": "assistant",
                                "content": ""
                            })
                            yield self.format_as_ndjson(response)
                        else:
                            deltaText = lineJson["choices"][0]["messages"][0]["delta"]["content"]
                            if deltaText != "[DONE]":
                                response["choices"][0]["messages"].append({
                                    "role": "assistant",
                                    "content": deltaText
                                })
                                yield self.format_as_ndjson(response)
        except Exception as e:
            yield self.format_as_ndjson({"error" + str(e)})

    def stream_without_data(self, response, history_metadata={}):
        responseText = ""
        for line in response:
            if line["choices"]:
                deltaText = line["choices"][0]["delta"].get('content')
            else:
                deltaText = ""
            if deltaText and deltaText != "[DONE]":
                responseText = deltaText

            response_obj = {
                "id": line["id"],
                "model": line["model"],
                "created": line["created"],
                "object": line["object"],
                "choices": [{
                    "messages": [{
                        "role": "assistant",
                        "content": responseText
                    }]
                }],
                "history_metadata": history_metadata
            }
            yield self.format_as_ndjson(response_obj)

    # override? how to 
    # pass in keys - initialization for client