from agents.factory import AgentFactory


if __name__ == "__main__":
    agent = AgentFactory()
    response = agent.run_dynamic_agent(
        "search",
        "What is the recent news about AI?",
        "session_k1"
    )
    print(response)
