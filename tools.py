from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder import flow, Flow


@tool(name="id_to_url", description="Get the TikTok video url. Input: tiktok Creater username and Video ID. Returns url")
def ttmeta_to_url (username:str, id:str):
    return f"https://tiktok.com/@{username}/video/{id}"

@flow(
    name = "TikTok_use_flow",
    input_schema=Name,
    output_schema=str
)
def build_hello_message_flow(aflow: Flow = None) -> Flow:
    """ Based on the first and last name of a person, combine into a single name and create a simple hello world message. """

    combine_names_node = aflow.tool(combine_names)
    get_hello_message_node = aflow.tool(get_hello_message)

    aflow.edge(START, combine_names_node).edge(combine_names_node, get_hello_message_node).edge(get_hello_message_node, END)

    return aflow