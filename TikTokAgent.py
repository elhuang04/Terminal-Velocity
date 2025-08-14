from ibm_watsonx_orchestrate.agent_builder.agents import Agent, AgentKind, AgentStyle
# from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# name_of_collaborator_agent_1 = Agent(
#     # omitted for brevity
# )    
# @tool(name="id_to_url", description="Get the TikTok video url. Input: tiktok Creater username and Video ID. Returns url")
# def ttmeta_to_url (username:str, id:str):
#     return f"https://tiktok.com/@{username}/video/{id}"
# @tool
# def name_of_tool_1(input: str) -> str:
#     """
#     Returns the string output

#     :param input: the input string
    
#     :returns: the string output
#     """
#     return 'output'


my_agent = Agent(
    name="test_native_agent",
    kind=AgentKind.NATIVE,
    llm="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    style=AgentStyle.DEFAULT,
    description="A description of what the should be used for when used as a collaborator.",
    instructions="These instructions control the behavior of the agent and provide context for how to use its tools and agents.",
    # collaborators=[
    #     "name_of_collaborator_agent_1",
    #     "name_of_collaborator_agent_2",
    # ],
    tools=[
        "tiktok-mcp:tiktok_search",
        "tiktok-mcp:tiktok_get_post_details",
        "tiktok-mcp:tiktok_get_subtitle",
        "id_to_url"
        ]  
    )
