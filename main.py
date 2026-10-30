from crewai import Crew
from crewai.llm import LLM

from agents import EssaySwarmAgents
from config import LOG_LEVEL, MODEL, PORT, TIMEOUT
from server import ModelServer
from tasks import EssaySwarmTasks


def main():
    topic = input("Enter essay topic: ").strip()
    if not topic:
        raise SystemExit("Essay topic cannot be empty.")

    with ModelServer(MODEL, PORT, TIMEOUT, LOG_LEVEL) as model_server:
        model = LLM(
            model=MODEL,
            custom_openai=True,
            base_url=model_server.v1_url,
            api_key="local_key",
        )

        agents = EssaySwarmAgents(model)
        tasks = EssaySwarmTasks()

        leader = agents.leader()
        writer = agents.writer()
        researcher = agents.researcher()
        reviewer = agents.reviewer()

        plan = tasks.plan(leader, topic)
        research = tasks.research(researcher, topic)
        write = tasks.write(writer, topic)
        review = tasks.review(reviewer, topic)

        essay_crew = Crew(
            agents=[leader, writer, researcher, reviewer],
            tasks=[plan, research, write, review],
            verbose=True,
        )
        return essay_crew.kickoff()


if __name__ == "__main__":
    print(main())
