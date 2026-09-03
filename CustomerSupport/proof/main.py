from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from mcp_client.client import get_streamable_http_mcp_client, get_gateway_mcp_client
from memory.session import get_memory_session_manager

app = BedrockAgentCoreApp()
log = app.logger
mcp_clients = [get_streamable_http_mcp_client(), get_gateway_mcp_client()]

SYSTEM_PROMPT = """You are a helpful and professional customer support assistant."""

RETURN_POLICIES = {
    "electronics": {"window": "30 days"},
    "accessories": {"window": "14 days"},
    "audio": {"window": "30 days"},
}
PRODUCTS = {
    "PROD-001": {"name": "Wireless Headphones", "price": 79.99},
    "PROD-002": {"name": "Smart Watch", "price": 249.99},
}

@tool
def get_return_policy(product_category: str) -> str:
    return str(RETURN_POLICIES.get(product_category.lower(), "No policy"))

@tool
def get_product_info(query: str) -> str:
    return str(PRODUCTS.get(query.upper(), query))

tools = [get_return_policy, get_product_info]
for c in mcp_clients:
    if c:
        tools.append(c)

_agent = None
def get_or_create_agent(sid, uid):
    global _agent
    if _agent is None:
        _agent = Agent(model=load_model(), session_manager=get_memory_session_manager(sid, uid), system_prompt=SYSTEM_PROMPT, tools=tools)
    return _agent

@app.entrypoint
async def invoke(payload, context):
    hdrs = {k.lower(): v for k, v in (getattr(context, 'request_headers', {}) or {}).items()}
    sid = getattr(context, 'session_id', None) or hdrs.get('x-amzn-bedrock-agentcore-runtime-session-id')
    uid = hdrs.get('x-amzn-bedrock-agentcore-runtime-custom-user-id') or getattr(context, 'user_id', None) or "default-user"
    log.info(f"sid={sid} uid={uid}")
    agent = get_or_create_agent(sid, uid)
    async for e in agent.stream_async(payload.get("prompt","")):
        if "data" in e and isinstance(e["data"], str):
            yield e["data"]

if __name__ == "__main__":
    app.run()
