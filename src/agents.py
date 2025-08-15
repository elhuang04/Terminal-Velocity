#------------------------------------------
#               All Imports
#------------------------------------------
from ibm_watsonx_orchestrate.agent_builder.agents import Agent, AgentKind, AgentStyle

'''
Code referenced from official docs:
https://developer.watson-orchestrate.ibm.com/agents/build_agent#agent-styles

name_of_collaborator_agent_1 = Agent(
    # omitted for brevity
)    
@tool
def name_of_tool_1(input: str) -> str:
    """
    Returns the string output

    :param input: the input string
    
    :returns: the string output
    """
    return 'output'
'''
#------------------------------------------
#             Global Variables
#------------------------------------------
# All descriptions and instructions enhanced using ChatGPT
TIKTOK_DESCRIPTION = '''
An analytical agent for exploring and researching TikTok 
content. It can search for videos retrieve detailed post 
information extract subtitles and map IDs to URLs for 
in-depth analysis.
'''
TIKTOK_INSTRUCTIONS = '''
This agent is designed to assist with interacting with 
TikTok content and its data. Search for TikTok videos based 
on keywords, trends, or hashtags. Retrieve detailed information 
about specific posts, including metadata and engagement metrics.
Extract subtitles or captions from videos for textual analysis.
Convert TikTok IDs to URLs for easy reference.
Provide clear and specific queries, such as keywords, post IDs, or 
hashtags, all schema data to get accurate and actionable results.
'''

CONTENT_DESCRIPTION = '''
An agent designed to manage content-related workflows, including 
reviewing posts, detecting policy violations, moderating content, 
and flagging inappropriate material for further action.
'''
CONTENT_INSTRUCTIONS = '''
This agent assists in analyzing and managing content to ensure 
compliance with platform policies and community guidelines. It can:
Review content to identify potential issues or violations.
Moderate posts by categorizing, approving, or restricting content 
as needed. Flag content that requires further attention or escalation.
Provide clear details about the content to be reviewed, including IDs, 
text, or metadata, so the agent can accurately assess and take the 
appropriate action.
'''

#------------------------------------------
#             Agent Creation
#------------------------------------------

agent_1 = Agent(
    name="content_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.DEFAULT,
    description=CONTENT_DESCRIPTION,
    instructions=CONTENT_INSTRUCTIONS,
    collaborators = [],
    tools=[
        "content_moderation"
        ]  
    )

agent_2 = Agent(
    name="tiktok_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.DEFAULT,
    description=TIKTOK_DESCRIPTION,
    instructions=TIKTOK_INSTRUCTIONS,
    collaborators = [],
    tools=[
        "tiktok-mcp:tiktok_search",
        "tiktok-mcp:tiktok_get_post_details",
        "tiktok-mcp:tiktok_get_subtitle",
        "id_to_url",
        ]  
    )

manager_agent = Agent(
    name="supervisor_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.PLANNER,
    description="placeholder",
    instructions="placeholder",
    collaborators=[
        "tiktok_agent",
        # "content_agent",
    ],
    tools = []
    )