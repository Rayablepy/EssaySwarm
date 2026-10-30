from crewai import Crew
from tasks import EssaySwarmTasks
from agents import EssaySwarmAgents
from server import MODEL
agents=EssaySwarmAgents(MODEL)
tasks=EssaySwarmTasks()

def main():
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
