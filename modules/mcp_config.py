import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


load_dotenv()
KAGGLE_API_KEY = os.getenv("KAGGLE_API_KEY")


def get_kaggle_mcp_tool():
    kaggle_tool = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "mcp-remote",
                    "https://www.kaggle.com/mcp",
                    "--header",
                    f"Authorization: Bearer {KAGGLE_API_KEY}"
                ]
            ),
            timeout=30,
        )
    )

    return kaggle_tool
