"""
Available tools:
1. get_competition_data_files_summary
2. get_competition_leaderboard
3. update_dataset_metadata
download_dataset, download_competition_leaderboard,
get_model_variation, get_dataset_files_summary, list_model_variation_versions,
get_benchmark_leaderboard, download_model_variation_version, get_notebook_info,
create_code_competition_submission, list_models, create_model, get_dataset_status,
create_benchmark_task_from_prompt, get_notebook_session_status,
download_notebook_output_zip, update_model, get_model,
download_competition_data_file, get_dataset_info, list_model_variation_version_files,
get_competition_submission, cancel_notebook_session, authorize,
list_competition_data_files, search_competition_submissions, get_dataset_metadata,
submit_to_competition, download_notebook_output, list_dataset_files,
get_competition, list_model_variations, list_competition_data_tree_files,
update_model_variation, download_competition_data_files,
search_competitions, save_notebook, list_notebook_files, search_notebooks,
start_competition_submission_upload, create_notebook_session, search_datasets,
list_notebook_session_output, upload_dataset_file, list_dataset_tree_files
"""
import asyncio
from utilities.setup import *

GOOGLE_API_KEY = get_google_api_key()
retry_config = get_retry_config()
KAGGLE_API_KEY = get_kaggle_credentials()

mcp_kaggle_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=[
                '-y',
                'mcp-remote',
                'https://www.kaggle.com/mcp',
                "--header",
                f"Authorization: Bearer {KAGGLE_API_KEY}"
            ],
            tool_filter=["search_notebooks", "get_notebook_info", "search_competitions"]
        ),
        timeout=30,
    )
)

print("✅ MCP Kaggle Toolset defined.")

root_agent = LlmAgent(
    name="helpful_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="""
        You are a Kaggle Data Science assistant. Use the provided Kaggle MCP tools to search for competitions,
                find relevant datasets, and retrieve details about notebooks/kernels based on the user’s request.
            
                CRITICAL RULE: You typically do not know the exact 'user_name' or 'slug' of a notebook. ALWAYS use
                'search_notebooks' first to find the correct author and slug before attempting to use 'get_notebook_info'.
                Never guess the username.
                
                For competitions, ALWAYS start with 'search_competitions' or similar tools to fetch current data.
                If needed, chain tools to get details like prize pools.""",
    tools=[mcp_kaggle_server],
)

print("✅ Root Agent defined.")

runner = InMemoryRunner(app_name="agents", agent=root_agent)

print("✅ Runner created.")

response = asyncio.run(runner.run_debug("""What are the recent Kaggle competitions that are active?""", verbose=True))

