# Terminal-Velocity
Project made for **IBM TechXchange 2025 Pre-conference watsonx Hackathon**

## Tools
MCP Servers Used:
- Instagram: https://glama.ai/mcp/servers/@Bob-lance/instagram-engagement-mcp
- TikTok: https://glama.ai/mcp/servers/@fmd-labs/viral-app-mcp
- Selenium: https://github.com/angiejones/mcp-selenium

See more details in [setup.md](./setup.md).

### Command for tool imports
NOTE: needs apify-api app ID in `Connections`
```
orchestrate tools import -k python -f src/tools.py -r requirements.txt --app-id "apify-api" --app-id "screenshot-api"
```

## Agents
### Command for agent imports
```
orchestrate agents import -f src/agents.py
```

