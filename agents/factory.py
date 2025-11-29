from agents.concrete import SearchAgent, KaggleAgent, NotionAgent


class AgentFactory:
    """
    Returns the specific agent class requested.
    """
    _registry = {
        "search": SearchAgent,
        "kaggle": KaggleAgent,
        "notion": NotionAgent
    }

    @staticmethod
    def get_agent(agent_name: str):
        agent_class = AgentFactory._registry.get(agent_name.lower())
        print(f"🦁 🦁 🦁 : {agent_name}")
        if not agent_class:
            raise ValueError(f"Agent '{agent_name}' is not supported. Available: {list(AgentFactory._registry.keys())}")

        return agent_class()

    def run_dynamic_agent(self, agent_name: str, message: str, session_id: str):
        try:
            agent = self.get_agent(agent_name)
            resource = agent.run(message, session_id)
            print(f"✅ ✅ ✅ : {resource}")
            return resource
        except Exception as e:
            print(f"🚨 🚨 🚨 : {e}")
            return f"Error: {e}"

