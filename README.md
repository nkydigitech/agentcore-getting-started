# AWS Bedrock AgentCore — Customer Support Agent (Deployed)

**Cloud & DevOps Engineer | I turn 3 AM-breaking deployments into 1-min pipelines with AWS + Ansible + Terraform | Building security-first AI agents on Amazon Bedrock AgentCore | AI Governance on AWS certified**

Hands-on build with **AWS Bedrock AgentCore** — a Customer Support agent deployed to real AWS infrastructure: managed runtime, shared session memory, an API gateway with JWT authentication backed by Amazon Cognito, and evaluation runs. Not a hello-world — a deployed, security-tested agent.

🔗 [LinkedIn — Nkechi Ahanonye](https://www.linkedin.com/in/nkechiahanonye)

---

## What Was Deployed (Verified Proof)

| Resource | Status |
|---|---|
| AgentCore Runtime | `CustomerSupport_CustomerSupport-nDetTy7GmQ` — READY |
| Memory | `SharedMemory-rTT75GC95r` (session persistence) |
| Gateways | `my-gateway` + JWT-secured gateway (`my-gateway-jwt-qvtkeokzvx`) |
| Auth | CUSTOM_JWT via Amazon Cognito (`us-east-1_o72nbDaJP`) |
| Security test | No token → **401 Unauthorized**; valid token → session created ✅ |
| Evaluation | Eval run recorded — `proof/lab5/eval_2026-09-03_13-05-41.json` |

The 401-vs-session test matters: it proves the agent endpoint is not publicly callable and that auth, memory, and session creation work end-to-end.

## The Agent

A Customer Support agent built with the **AgentCore CLI** + CDK, featuring:

1. **MCP client** (`mcp_client/`) — connects to tool servers over the Model Context Protocol
2. **Session memory** (`memory/session.py`) — conversation state persisted in AgentCore Shared Memory
3. **Skills** (`skills/fetcher.py`) — modular agent capabilities
4. **Structured tools** (`tool/warranty_schema.json`) — typed tool definitions
5. **Model loading** (`model/`) — clean model integration layer

## Infrastructure

Provisioned with **AWS CDK** (`@aws/agentcore-cdk`):

```
agentcore/
├── agentcore.json      # Project config — runtimes, memories, gateways, evaluators
├── aws-targets.json    # Deployment targets (account + region)
└── cdk/                # CDK stack — full IaC for the agent estate
```

Deployment is one command: `agentcore deploy` (locally first: `agentcore dev` with hot-reload).

## Repo Structure

```
CustomerSupport/
├── AGENTS.md            # AI coding assistant context
├── agentcore/           # AgentCore project config + CDK infrastructure
├── app/CustomerSupport/ # Python agent — MCP client, memory, skills, tools
└── proof/               # Deployment proof: runtime status, CFN outputs, eval results
```

## How to Run

Prerequisites: Node.js 20+, Python 3.10+ with `uv`, AWS credentials configured.

```bash
# Run the agent locally (hot-reload)
agentcore dev

# Deploy to AWS via CDK
agentcore deploy

# Add more resources (agent, memory, credential, gateway, evaluator, policy)
agentcore add <resource>
```

---

Built by **Nkechi Anna Ahanonye** · [LinkedIn](https://www.linkedin.com/in/nkechiahanonye) · [GitHub](https://github.com/nkydigitech)

*Agentic AI, deployed and secured — not simulated.*
