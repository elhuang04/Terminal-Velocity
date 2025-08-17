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
Make sure to always get the URL of any TikTok videos you find and
give a list of all the URLs back to the user.
'''

INSTA_DESCRIPTION = '''
An analytical agent for exploring and researching Instagram 
content.
'''
INSTA_INSTRUCTIONS = '''
Features
Analyze Post Comments: Extract sentiment, themes, and potential leads from comments on Instagram posts
Compare Accounts: Compare engagement metrics across different Instagram accounts
Extract Demographics: Get demographic insights from users engaged with a post or account
Identify Leads: Find potential leads based on engagement patterns and criteria
Generate Engagement Reports: Create comprehensive reports with actionable insights
'''

BROWSER_DESCRIPTION = '''
An analytical agent observing keywords and guidelines to determine if there
are any content violations. 
'''
BROWSER_INSTRUCTIONS = '''
You are an analytical agent tasked with reviewing web content for harmful words and guideline violations.
Steps:
1. Examine the content on the page or media.
2. Use `flag_harmful` to detect offensive or harmful words.
3. Use `check_guidelines` to compare content against platform rules (infer platform from URL or agent if needed).
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
SUPERVISOR_DESCRIPTION = '''
Supervisor agent to designate subtasks to subagents.
'''

SUPERVISOR_INSTRUCTIONS = '''
First use all social media agents (tiktok_agent, instagram_agent) to get all relevant content.
Once all content has been received, use the content_agent to analyze
whether any posts or content violate the platform's community guidelines.
'''

#------------------------------------------
#             Agent Creation
#------------------------------------------
agent_1 = Agent(
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

agent_2 = Agent(
    name="instagram_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.DEFAULT,
    description=INSTA_DESCRIPTION,
    instructions=INSTA_INSTRUCTIONS,
    collaborators = [],
    tools=[
        "apify_insta_hashtag_search",
        "apify_insta_post_details",
        "apify_insta_reels",
        ]
    )

agent_3 = Agent(
    name="content_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.DEFAULT,
    description=BROWSER_DESCRIPTION,
    instructions=BROWSER_INSTRUCTIONS,
    collaborators = [],
    tools=[
        "content_moderation",
        "check_guidelines",
        # "get_screenshot", #TODO: fix bugs with rendering base64 image!
        ]
    )

manager_agent = Agent(
    name="supervisor_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.PLANNER,
    description=SUPERVISOR_DESCRIPTION,
    instructions=SUPERVISOR_INSTRUCTIONS,
    collaborators=[
        agent_1, #tiktok
        agent_2, #instagram
        agent_3, #content
    ],
    tools = []
)
