import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import AsyncGenerator, List, Literal

from agent import invoke_lang_graph

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "https://tiebreak-demo-ui-350195377988.us-central1.run.app"
]

app.add_middleware(CORSMiddleware,
    allow_origins=origins,              # or ["*"] for all origins (not recommended in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# {
#    "model":"local-model",
#    "messages":[
#       {
#          "role":"system",
#          "content":"You are a helpful assistant."
#       },
#       {
#          "role":"user",
#          "content":"hi"
#       }
#    ],
#    "stream":True,
#    "temperature":0.7
# }

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool = False
    temperature: float = 0.7


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    llm_response = invoke_lang_graph(request.messages[-1])
    # if llm_response == "":
    #     return JSONResponse(
    #         content={"response":"Nothing"}, 
    #         status_code=200
    #     )

    # return JSONResponse(
    #     content={"response":llm_response}, 
    #     status_code=200
    # )
    
    if request.stream and llm_response != "":
        async def event_stream() -> AsyncGenerator[str, None]:
            # Simulate a streaming LLM response
            reply = llm_response["message"]
            for word in reply.split():
                chunk = {
                    "choices": [{
                        "delta": {
                            "content": word + " "
                        }
                    }]
                }
                yield f"data: {json.dumps(chunk)}\n"
                await asyncio.sleep(0.2)

            # Signal that stream is done
            yield "data: [DONE]\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    else:
        # If not streaming, return a regular full message
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "This is a full response (not streamed)."
                }
            }]
        }
