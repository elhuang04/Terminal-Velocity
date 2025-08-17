# Terminal-Velocity
Project made for **IBM TechXchange 2025 Pre-conference watsonx Hackathon**

## Tools
MCP Servers Used:
- Instagram: https://glama.ai/mcp/servers/@Bob-lance/instagram-engagement-mcp
- TikTok: https://glama.ai/mcp/servers/@fmd-labs/viral-app-mcp
- Selenium: https://github.com/angiejones/mcp-selenium

See more details in [setup.md](./setup.md).

### Command for tool imports
NOTE: needs `apify-api` and `screenshot-api` app ID in `Connections` (both use `API_KEY` as key)
```
orchestrate tools import -k python -f src/tools.py -r requirements.txt --app-id "apify-api" --app-id "screenshot-api"
```

## Agents
### Command for agent imports
```
orchestrate agents import -f src/agents.py
```

## Webhook used to connect to Twilio sandbox
Follow the documentation here (https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=integrations-integrating-whatsapp) to setup the agent within a Twilio sandbox, paste the
following webhook URI: `https://channels.ca-tor.watson-orchestrate.cloud.ibm.com/tenants/5d27013365134da681381a7d979088af_d4fc2132-78e5-41cb-88a8-81a09b36faad/agents/a60bfbd5-bc8d-4220-b0b7-1bb70ab34567/environments/80201c44-c955-46a3-acab-8a039c6c326d/channels/twilio_whatsapp/b1be38c3-3f4b-489c-9fd8-dfaaa6192af0/events`
