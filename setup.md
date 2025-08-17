## MCP Server Commands

### Instagram MCP
```bash
orchestrate toolkits import \
  --kind=mcp \
  --name=instagram-mcp \
  --language=node \
  --description='instagram tools' \
  --package='instagram-engagement-mcp' \
  --command='npx instagram-engagement-mcp' \
  --tools="*" \
  --app-id "instagram"
```
### Selenium MCP (not used)
```bash
orchestrate toolkits import \
  --kind=mcp \
  --name=selenium-mcp \
  --language=node \
  --description='browser automation using selenium' \
  --package='@angiejones/mcp-selenium' \
  --command='npx -y @angiejones/mcp-selenium' \
  --tools="*" \
  --app-id=github
```
### TikTok MCP
NOTE: All code from the `tiktok-mcp` directory is an exact copy/clone 
from 
```bash
orchestrate toolkits import \
    --kind mcp \
    --name tiktok-mcp \
    --description "interactions with tiktok" \
    --package-root . \
    --command '["node", "./build/index.js", "--transport", "stdio"]' \
    --tools "tiktok_search, tiktok_get_post_details, tiktok_get_subtitle" \
    --app-id "tiktok"
```

