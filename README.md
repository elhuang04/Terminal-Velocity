# Terminal-Velocity
IBM TechXchange 2025 Pre-conference watsonx Hackathon

## Observations
Use MCP servers for external tool integrations and create custom tool configs where needed:
	- Resource for finding MCP servers for social media platforms: https://glama.ai/mcp/servers/categories/social-media
	- Others: https://mcp.so/server/social-media-mcp
	- https://github.com/seekrays/mcp-monitor | #TODO: replace with platform native API configuration later


API keys can be set up in Manage > Connections, and can also be used to create env connections for MCP servers

--> unreliable/ broken; recommend using the ADK instead: https://developer.watson-orchestrate.ibm.com/getting_started/installing 

Orchestrate API keys here: https://cloud.ibm.com/services/watsonx-orchestrate/crn%3Av1%3Abluemix%3Apublic%3Awatsonx-orchestrate%3Aca-tor%3Aa%2F5d27013365134da681381a7d979088af%3Ad4fc2132-78e5-41cb-88a8-81a09b36faad%3A%3A?paneId=manage

In ADK tooling implementation, copy/reference from provided workday SSO API template use: https://developer.watson-orchestrate.ibm.com/tutorials/workday_sso_connections
	- note: gives agent direct access to use RESTful actions, most likely not needed

Setting secrets (API keys): https://developer.watson-orchestrate.ibm.com/environment/initiate_environment

## Action Items / How to Implement
1) Set up agent ADK in local IDE: https://developer.watson-orchestrate.ibm.com/getting_started/installing, https://developer.watson-orchestrate.ibm.com/agents/build_agent (create simple agent and test it through IBM cloud dashboard) 

2) Research and find any MCP servers that offer desired tools/services. Follow https://developer.watson-orchestrate.ibm.com/tools/toolkits to import all the tools from the server to the agent.

3) Embed 3rd party integrations within tools rather than giving 3rd party permissions to agent itself (requires connection configs): https://developer.watson-orchestrate.ibm.com/tools/create_tool 

4) Setup flows for chained tool calls: https://developer.watson-orchestrate.ibm.com/tools/flows/overview#when-to-use-flow

5) Basic interaction interface (web chat/ text box): https://developer.watson-orchestrate.ibm.com/manage/channels