import os

from crewai import Crew
from crewai.llm import LLM
from tasks import EssaySwarmTasks
from agents import EssaySwarmAgents
from server import start
from config import MODEL,PORT,TIMEOUT,LOG_LEVEL

def main():
    start(MODEL,PORT,TIMEOUT,LOG_LEVEL)
    model = LLM(
        model=MODEL,
        custom_openai=True,
        base_url=f"http://localhost:{PORT}/v1",
        api_key="local_key"
    )
    agents=EssaySwarmAgents(model)
    tasks=EssaySwarmTasks()
    topic=str(input("Enter essay topic: "))
    leader=agents.leader()
    writer=agents.writer()
    researcher=agents.researcher()
    reviewer=agents.reviewer()

    plan=tasks.plan(leader,topic)
    research=tasks.research(researcher,topic)
    write=tasks.write(writer,topic)
    review=tasks.review(reviewer,topic)

    essay_crew=Crew(
        agents=[
            leader,writer,researcher,reviewer
        ],
        tasks=[
            plan,research,write,review
        ],
        verbose=True
    )
    essay = essay_crew.kickoff()
    return essay

if __name__ == "__main__":
    print(main())
