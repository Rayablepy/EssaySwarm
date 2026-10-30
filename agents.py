from crewai import Agent

class EssaySwarmAgents:
    def __init__(self,model):
        self.model=model
    def leader(self):
        return Agent(
            role="leader",
        )
    def writer():
        ...
    def researcher():
        ...
    def reviewer():
        ...
