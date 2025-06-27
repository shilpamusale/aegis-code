# In src/integrations/github_tools.py

import os
from github import Github, GithubException

# --- HELPER FUNCTION ---


def get_github_repo():
    """
    Authenticates with Github and returns the repository object.

    This helper function centralizes authentication. It uses a GitHub
    Personal Access Token and the respository name from environment variables.
    This is the entry point for all interactions with the GitHub API.

    Returns:
        A PyGithub Repository object, or None if authentication fails.

    """

    try:
        github_token = os.environ.get("GITHUB_TOKEN")
        repo_name = os.environ.get("GITHUB_REPOSITORY")

        if not github_token or not repo_name:
            print(
                "Error: GITHUB_TOKEN and GITHUB_REPOSITORY environment variables are required."
            )
            return None
        g = Github(github_token)
        return g.get_repo(repo_name)
    except Exception as e:
        print(f"Error authenticating with GitHub: {e}")
        return None


# --- ATOMIC TOOLS ---
def get_pr_diff(pr_number: int) -> str:
    """
    Fetches the diff for a given pull request number.

    The "diff" is a string that shows exactly which lines were added,
    remved, or changed in a pull request. This is the primary context
    our review agent will need.

    Args:
        pr_number: The number of the pull request.

    Returns:
        A string containing the diff, or an error message.
    """

    repo = get_github_repo()

    if not repo:
        return "Error: Could not connect to the GitHub repository."

    try:
        pr = repo.get_pull(pr_number)
        diff_content = pr.get_diff()
        return diff_content
    except GithubException as e:
        return f"Error fetching PR diff: {e.status} {e.data.get('message', '')}"
    except Exception as e:
        return f"An unexpected error occurred while fetching PR diff: {e}"


def post_pr_comment(pr_number: int, comment_body: str) -> str:
    """
    Posts a comment to a specified pull request.

    This tool allows the agent to provide its final, synthesized feedback
    directly on the pull request, engaging with the developer's workflow.

    Args:
        pr_number: The number of the pull request to comment on.
        comment_body: The string content of the comment to post.

    Returns:
        A success message with the URL of the new comment or an error message.

    """
    repo = get_github_repo()
    if not repo:
        return "Error: Could not connect to the GitHub repository."

    try:
        # In the Github api, comments on the Pull Requests are handled as "issue" comments.
        issue = repo.get_issue(number=pr_number)
        comment = issue.create_comment(comment_body)
        return f"Successfully posted comment: {comment.html_url}"

    except GithubException as e:
        return f"Error posting PR comment: {e.status} {e.data.get('message', '')}"
    except Exception as e:
        return f"An unexpected error occurred while posting PR comment: {e}"


# ==============================================================================
# Local Test Block
# ==============================================================================
if __name__ == "__main__":
    print("--- GitHub Tools: Local Test ---")
    print("This block demonstrates how the functions would be called.")
    print(
        "For a real run, ensure GITHUB_TOKEN and GITHUB_REPOSITORY are set in your environment.\n"
    )

    # To run a real test:
    # 1. Create a Personal Access Token with 'repo' scope on GitHub.
    # 2. Set the environment variables:
    #    export GITHUB_TOKEN="your_token_here"
    #    export GITHUB_REPOSITORY="your_username/aegis-code"
    # 3. Choose a real PR number from your repository.
    # 4. Uncomment and run the code below.

    # pr_num_to_test = 1 # Replace with a real PR number

    # print(f"--- Testing get_pr_diff on PR #{pr_num_to_test} ---")
    # diff = get_pr_diff(pr_num_to_test)
    # print(diff)

    # print(f"\n--- Testing post_pr_comment on PR #{pr_num_to_test} ---")
    # comment_text = "This is a test comment from the Aegis Code agent system."
    # result = post_pr_comment(pr_num_to_test, comment_text)
    # print(result)

    print("Local test demonstration complete.")
