from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
#from ibm_watsonx_orchestrate.agent_builder import flow, Flow
import re
from datetime import datetime

@tool(name="id_to_url", description="Get the TikTok video url. Input: tiktok Creater username and Video ID. Returns url")
def ttmeta_to_url (username:str, id:str):
    return f"https://tiktok.com/@{username}/video/{id}"

harmful_words = {
    "n****", "f****t", "ch*nk", "sp*c", "white trash", "go back to your country", "dirty immigrant",
    "terrorist", "subhuman", "suicide", "kill myself", "end my life", "kms",
    "cutting", "slit wrists", "jump off bridge",
    "overdose", "self harm",
    "hang myself", "I want to die", "stab", "shoot", "murder", "kill you", "gun down",
    "blow up", "bomb", "strangle", "beat to death",
    "assault", "rape", "torture", "hang", "choke",
    "arson", "attack", "fight you", "kill yourself", "nobody likes you", "you’re disgusting", "freak"
}

@tool(name="content_moderation", description = "Flags harmful words and reports them")
def flag(content:str, url:str):
    counter = 0
    flag = []
    ticket = None
    word = content.lower
    for i in range(len(harmful_words)):
        if(word.equals(i)):
            if(word not in flag):
                flag.append(word)
                counter+=1
    
    if(counter>0):
            ticket = {
            "ticket_id": f"TICKET-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "video_url": url,
            "detected_words": list(set(flag)),
            "created_at": datetime.now().isoformat(),
            "status": "OPEN",
            "priority": "HIGH"
            }
    return{
        "Is this harmful: ", counter>0,
        "Bad words: ", flag,
        "Ticket: " , ticket
    }

            



#