import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


load_dotenv()
KAGGLE_API_KEY = os.getenv("KAGGLE_API_KEY")



tools = [
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
    "list_dataset_tree_files"
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
                tool_filter = tools
            ),
            timeout=30,
        )
    )

    return kaggle_tool
