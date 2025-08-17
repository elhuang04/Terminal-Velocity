#------------------------------------------
#               All Imports
#------------------------------------------
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from apify_client import ApifyClient
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import ssl
import base64
from PIL import Image
import io
#------------------------------------------
#             Global Variables
#------------------------------------------
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

#------------------------------------------
#                  Tools
#------------------------------------------
#====================#
#    TikTok Tools    #
#====================#
@tool(name="id_to_url", description="Get the TikTok video url. Input: tiktok Creater username and Video ID. Returns url")
def ttmeta_to_url (username:str, id:str):
    return f"https://tiktok.com/@{username}/video/{id}"

#=================================#
#    Content Moderation Tools     #
#=================================#
@tool(
    name="content_moderation",
    description="Send back a report of any media containing harmful words/content."
)
def flag_harmful(content: str, url: str) -> dict:
    """
    Scans input content for harmful words and flags if necessary.
    :param content: The text content to check.
    :param url: The media URL associated with the content.
    :return: A dictionary report with findings.
    """
    content_lower = content.lower()
    flagged = []

    for word in harmful_words:
        if word in content_lower:
            flagged.append(word)

    return {
        "url": url,
        "content": content,
        "flagged": flagged,
        "is_harmful": len(flagged) > 0,
        "message": "Harmful content detected." if flagged else "No harmful content detected."
    }

@tool(
    name="check_guidelines",
    description="Gets a platform's community guidelines."
)
def check_guidelines(content: str, url: str = None, source_agent: str = None) -> dict:
    """
    Checks whether the provided content may violate a platform's community guidelines.
    The platform is inferred from either the URL or the calling agent.
    
    :param content: The text content to check.
    :param url: Optional media URL associated with the content.
    :param source_agent: Optional hint about which platform agent called this tool.
    :return: Dictionary with a summary of potential violations.
    """
    
    # Mapping for agents and platform URLs
    agent_to_platform = {
        "tiktok_agent": "TikTok",
        "instagram_agent": "Instagram",
    }
    
    guidelines_urls = {
        "instagram": "https://help.instagram.com/477434105621119",
        "tiktok": "https://www.facebook.com/help/instagram/477434105621119/",
    }
    platform = None
    if source_agent:
        platform = agent_to_platform.get(source_agent.lower())
    if not platform and url:
        if "instagram.com" in url:
            platform = "Instagram"
        elif "tiktok.com" in url:
            platform = "TikTok"
    
    if not platform:
        return {
            "content": content,
            "url": url,
            "error": "Unable to determine platform. Provide a URL or source_agent."
        }
    
    platform_lower = platform.lower()
    url_guidelines = guidelines_urls.get(platform_lower)
    
    try:
        response = requests.get(url_guidelines, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        guidelines_text = soup.get_text(separator=" ").lower()
        return guidelines_text
    
    except Exception as e:
        return {
            "platform": platform,
            "content": content,
            "url": url,
            "error": f"Failed to fetch guidelines: {str(e)}"
        }
    

@tool(
    name="get_screenshot",
    description="Takes in any URL, calls ScreenshotAPI.net, compresses the image, and outputs a base64 string safe for Watsonx.",
    expected_credentials=[
        ExpectedCredentials(
            app_id="screenshot-api",
            type=ConnectionType.KEY_VALUE
        )
    ]
)
def get_screenshot(url: str, max_base64_length: int = 200_000):
    """
    Takes a URL, requests a screenshot from ScreenshotAPI.net using stored credentials,
    compresses it, and returns Base64. Ensures the Base64 string stays under a max length.
    """
    try:
        # Use local SSL override
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Get API key from connections
        screenshot_credentials = connections.key_value("screenshot-api")
        api_key = screenshot_credentials.get("API_KEY")
        if not api_key:
            return {"error": "API_KEY missing from screenshot-api credentials."}
        
        encoded_url = urllib.parse.quote_plus(url)
        query = f"https://shot.screenshotapi.net/screenshot?token={api_key}&url={encoded_url}&output=image&file_type=png"
        
        # Retrieve the image as bytes
        with urllib.request.urlopen(query, timeout=15) as response:
            screenshot_bytes = response.read()
        
        # Compress image using Pillow
        image = Image.open(io.BytesIO(screenshot_bytes))
        image.thumbnail((800, 600))  # reduce dimensions to max 800x600
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=70)  # compress to JPEG
        compressed_bytes = buffer.getvalue()
        
        # Encode to Base64
        screenshot_b64 = base64.b64encode(compressed_bytes).decode('utf-8')
        
        # Truncate if exceeds max length
        if len(screenshot_b64) > max_base64_length:
            screenshot_b64 = screenshot_b64[:max_base64_length]
        
        return "data:image/jpeg;base64," + screenshot_b64
    
    except Exception as e:
        return {"error": f"Failed to capture screenshot: {str(e)}"}


#========================#
#    Instagram Tools     #
#========================#
def apify_insta_post_details(url: str, 
                             results_type: str = "details"):
    """
    Get detailed data from a specific Instagram post, reel, or profile.
    :param url: The Instagram URL (post, reel, profile, etc.)
    :param results_type: One of 'details', 'comments', 'posts', 'mentions', 'stories'.
    """
    apify_credentials = connections.key_value("apify-api")
    client = ApifyClient(apify_credentials["API_KEY"])
    results = []

    run_input = {
        "directUrls": [url],
        "resultsType": results_type,
    }

    if "/reels/" in url or "reel" in url:
        run_input["isUserReelFeedURL"] = True
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    for item in client.dataset(dataset_id).iterate_items():
        results.append(item)
    return results

@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id="apify-api",
            type=ConnectionType.KEY_VALUE
        )
    ]
)
def apify_insta_hashtag_search(hashtag: str, 
                               limit: int = 3, 
                               results_limit: int = 3):
    """
    Search Instagram by hashtag.
    :param hashtag: The hashtag (without '#', e.g. 'sunset').
    :param limit: How many hashtag search results to return.
    :param results_limit: Max posts per hashtag.
    """
    apify_credentials = connections.key_value("apify-api")
    client = ApifyClient(apify_credentials["API_KEY"])
    results = []

    run_input = {
        "search": hashtag,
        "searchType": "hashtag",
        "searchLimit": limit,
        "resultsType": "posts",
        "resultsLimit": results_limit,
    }
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    for item in client.dataset(dataset_id).iterate_items():
        results.append(item)
    return results

@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id="apify-api",
            type=ConnectionType.KEY_VALUE
        )
    ]
)
def apify_insta_reels(url: str, 
                      results_limit: int = 3):
    """
    Get reels from a profile or reel URL.
    :param url: The Instagram profile URL (to get all reels) or a specific reel URL.
    :param results_limit: How many reels to fetch.
    """
    apify_credentials = connections.key_value("apify-api")
    client = ApifyClient(apify_credentials["API_KEY"])
    results = []

    run_input = {
        "directUrls": [url],
        "resultsType": "posts",
        "resultsLimit": results_limit,
        "isUserReelFeedURL": True,
    }

    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    for item in client.dataset(dataset_id).iterate_items():
        results.append(item)
    return results