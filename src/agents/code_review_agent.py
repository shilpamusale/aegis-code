# In src/agents/code_review_agent.py


class CodeReviewAgent:
    """
    An agent specialized in reviewing code for quality, style and correctness.

    This agent acts as an "evaluator" in our system. It takes code changes
    (e.g. a pull request diff) as input and provides a structured review as output.
    Its logic is primarily driven by the LLM, guided by the specific prompt deined in 'src/agents/prompts.py'.

    This class integrated LangGraph workflow, where it will be connected to an LLM and the GitHub API tools to perform
    its review tasks.
    """

    def __init__(self) -> None:
        """
        Initializes the CodeReviewAgent.

        The initialize the LLM, prompt, and tools.
        """

        print("CodeReviewAgent initialized.")

    def run(self, code_diff: str) -> str:
        """
        This method takes a diff string, pass it to the LLM with
        the appropriate prompt, and return the LLM's generated review.

        Args:
            code_diff: A string containing the diff of the code to be reviewed.

        Returns:
            A string containing the generated code review.
        """

        print("\n --- CodeReviewAgent: Pretending to review the code diff ---\n")
        print(code_diff)

        # Placeholder for the actual LLM call
        dummy_review = (
            "This is a dummy review from the CodeReviewAgent.\n"
            "I see you've made some changes. In a real run, I would provide "
            "detailed feedback on potential bugs, style issues, and improvements."
        )

        print("\n--- CodeReviewAgent: Dummy review generated ---\n")
        print(dummy_review)

        return dummy_review
