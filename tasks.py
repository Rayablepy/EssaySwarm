from crewai import Task


class EssaySwarmTasks:
    def __init__(self, leader, researcher, writer, reviewer):
        self.planning = Task(
            description="""
            Given the essay request on {topic}, analyze the assignment and produce
            two deliverables: a research brief and an essay problem statement.

            The research brief must name the specific resources the Researcher should
            gather and scrape, including the key questions to answer, the types of
            sources to prefer, suggested search terms, and the facts that must be
            verified.

            The essay problem statement must define the central question, the scope
            and stance, and the criteria for a successful essay. Do not write the
            essay itself.
            """,
            expected_output="""
            A structured brief with two sections:

            1. Research Resources: source types, key questions, suggested search
               terms, and the facts that must be verified.
            2. Essay Problem Statement: the central question, scope and stance, and
               the success criteria for the essay.
            """,
            agent=leader,
            output_file="EssaySwarmOutput/01_planning.md",
        )

        self.research = Task(
            description="""
            Using the research brief from the Leader, use your available tools to
            find, scrape, and verify sources on {topic}. Prioritize primary and
            reputable sources, and record each source's title, author or publisher,
            publication date, and URL. Extract the facts, quotes, and figures needed
            to support the essay problem statement, and note any conflicting evidence
            or gaps.
            """,
            expected_output="""
            A citation-ready research packet. For each source, include its title,
            author or publisher, publication date, URL, a short summary, and the
            specific facts or quotes it supports. Include key findings mapped to the
            essay problem statement, plus any caveats or conflicting evidence.
            """,
            agent=researcher,
            context=[self.planning],
            output_file="EssaySwarmOutput/02_research.md",
        )

        self.writing = Task(
            description="""
            Write an essay on {topic} that answers the Leader's essay problem
            statement using only the sources in the Researcher's packet. Include a
            clear thesis, a logical introduction, body, and conclusion, and cite the
            provided sources inline. Every factual claim must be traceable to a
            provided source, and the essay must meet the success criteria in the
            problem statement.
            """,
            expected_output="""
            A complete, polished essay with a title, a clear thesis, coherent
            paragraphs, inline citations to the provided sources, and a conclusion.
            No unsupported claims.
            """,
            agent=writer,
            context=[self.planning, self.research],
            output_file="EssaySwarmOutput/03_essay.md",
        )

        self.review = Task(
            description="""
            Review the Writer's essay against the essay problem statement and its
            success criteria. Quote specific passages to support every judgment, and
            flag unsupported claims, off-topic material, structural problems, and
            citation errors.
            """,
            expected_output="""
            A structured review containing an overall verdict (pass or revise), a
            criterion-by-criterion assessment quoting evidence from the essay, a list
            of concrete issues ordered by severity, and specific revision
            recommendations. Do not rewrite the essay.
            """,
            agent=reviewer,
            context=[self.planning, self.research, self.writing],
            output_file="EssaySwarmOutput/04_review.md",
        )

    def all(self):
        return [self.planning, self.research, self.writing, self.review]
