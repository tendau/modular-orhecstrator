from .Orchestrator import Orchestrator
import os
import json
import logging
import requests
import copy
import openai
from dotenv import load_dotenv
from flask import  Response, request, jsonify

class BaseOrchestrator(Orchestrator):
    def conversation_with_data(self, request_body):
        print(request.json["messages"])
        body, headers = super().prepare_body_headers_with_data(request)
        base_url = super().AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
        endpoint = f"{base_url}openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
        history_metadata = request_body.get("history_metadata", {})

        if not SHOULD_STREAM:
            r = requests.post(endpoint, headers=headers, json=body)
            status_code = r.status_code
            r = r.json()
            if AZURE_OPENAI_PREVIEW_API_VERSION == "2023-06-01-preview":
                r['history_metadata'] = history_metadata
                return Response(format_as_ndjson(r), status=status_code)
            else:
                result = formatApiResponseNoStreaming(r)
                result['history_metadata'] = history_metadata
                return Response(format_as_ndjson(result), status=status_code)

        else:
            return Response(stream_with_data(body, headers, endpoint, history_metadata), mimetype='text/event-stream')

    def conversation_without_data(request_body):
        openai.api_type = "azure"
        openai.api_base = AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
        openai.api_version = "2023-08-01-preview"
        openai.api_key = AZURE_OPENAI_KEY

        request_messages = request_body["messages"]
        messages = [
            {
                "role": "system",
                "content": AZURE_OPENAI_SYSTEM_MESSAGE
            }
        ]

        for message in request_messages:
            if message:
                messages.append({
                    "role": message["role"] ,
                    "content": message["content"]
                })

        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_MODEL,
            messages = messages,
            temperature=float(AZURE_OPENAI_TEMPERATURE),
            max_tokens=int(AZURE_OPENAI_MAX_TOKENS),
            top_p=float(AZURE_OPENAI_TOP_P),
            stop=AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
            stream=SHOULD_STREAM
        )

        history_metadata = request_body.get("history_metadata", {})

        if not SHOULD_STREAM:
            response_obj = {
                "id": response,
                "model": response.model,
                "created": response.created,
                "object": response.object,
                "choices": [{
                    "messages": [{
                        "role": "assistant",
                        "content": response.choices[0].message.content
                    }]
                }],
                "history_metadata": history_metadata
            }

            return jsonify(response_obj), 200
        else:
            return Response(stream_without_data(response, history_metadata), mimetype='text/event-stream')