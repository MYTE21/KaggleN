import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()
KAGGLE_API_KEY = os.getenv("KAGGLE_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")


kaggle_tools = [
    "get_competition_data_files_summary",
    "get_competition_leaderboard",
    "update_dataset_metadata",
    "download_dataset",
    "download_competition_leaderboard",
    "get_model_variation",
    "get_dataset_files_summary",
    "list_model_variation_versions",
    "get_benchmark_leaderboard",
    "download_model_variation_version",
    "get_notebook_info",
    "create_code_competition_submission",
    "list_models",
    "create_model",
    "get_dataset_status",
    "create_benchmark_task_from_prompt",
    "get_notebook_session_status",
    "download_notebook_output_zip",
    "update_model",
    "get_model",
    "download_competition_data_file",
    "get_dataset_info",
    "list_model_variation_version_files",
    "get_competition_submission",
    "cancel_notebook_session",
    "authorize",
    "list_competition_data_files",
    "search_competition_submissions",
    "get_dataset_metadata",
    "submit_to_competition",
    "download_notebook_output",
    "list_dataset_files",
    "get_competition",
    "list_model_variations",
    "list_competition_data_tree_files",
    "update_model_variation",
    "download_competition_data_files",
    "search_competitions",
    "save_notebook",
    "list_notebook_files",
    "search_notebooks",
    "start_competition_submission_upload",
    "create_notebook_session",
    "search_datasets",
    "list_notebook_session_output",
    "upload_dataset_file",
    "list_dataset_tree_files",
]

# notion_tools = [
#     "API-get-user",
#     "API-get-users",
#     "API-get-self",
#     "API-post-database-query",
#     "API-post-search",
#     "API-get-block-children",
#     "API-patch-block-children",
#     "API-retrieve-a-block",
#     "API-update-a-block",
#     "API-delete-a-block",
#     "API-retrieve-a-page",
#     "API-patch-page",
#     "API-post-page",
#     "API-create-a-database",
#     "API-update-a-database",
#     "API-retrieve-a-database",
#     "API-retrieve-a-page-property",
#     "API-retrieve-a-comment",
#     "API-create-a-comment",
# ]

notion_tools = [
    "notion-get-user",
    "notion-get-users",
    "notion-get-self",
    "notion-post-database-query",
    "notion-post-search",
    "notion-get-block-children",
    "notion-patch-block-children",
    "notion-retrieve-a-block",
    "notion-update-a-block",
    "notion-delete-a-block",
    "notion-retrieve-a-page",
    "notion-patch-page",
    "notion-post-page",
    "notion-create-a-database",
    "notion-update-a-database",
    "notion-retrieve-a-database",
    "notion-retrieve-a-page-property",
    "notion-retrieve-a-comment",
    "notion-create-a-comment",
]

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
                    f"Authorization: Bearer {KAGGLE_API_KEY}",
                ],
                tool_filter=kaggle_tools,
            ),
            timeout=60,
        )
    )

    return kaggle_tool


def get_notion_mcp_tool():
    notion_tool = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@notionhq/notion-mcp-server"],
                # args=["-y", "mcp-remote", "https://mcp.notion.com/mcp"],
                env={
                    "NOTION_TOKEN": NOTION_API_KEY,
                },
                tool_filter=notion_tools
            ),
            timeout=60,
        )
    )

    return notion_tool
