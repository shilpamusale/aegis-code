# In src/tests/test_github_tools.py

from src.integrations import github_tools


def test_get_pr_diff_success(mocker):
    """
    Tests the get_pr_diff tool in a successful scenario by mocking the GitHub API.
    """
    # 1. Create a fake "PullRequest" object that our mock will return.
    mock_pr = mocker.Mock()
    mock_pr.get_diff.return_value = (
        "--- a/file.py\n+++ b/file.py\n- old line\n+ new line"
    )

    # 2. Create a fake "Repo" object.
    mock_repo = mocker.Mock()
    mock_repo.get_pull.return_value = mock_pr

    # 3. Mock the get_github_repo helper function to return our fake repo.
    mocker.patch(
        "src.integrations.github_tools.get_github_repo", return_value=mock_repo
    )

    # 4. Run the actual tool.
    diff = github_tools.get_pr_diff(pr_number=123)

    # 5. Assert that the tool returned the diff from our fake PR object.
    assert "new line" in diff
    # Assert that the get_pull method on our mock repo was called correctly.
    mock_repo.get_pull.assert_called_once_with(123)


def test_post_pr_comment_success(mocker):
    """
    Tests the post_pr_comment tool by mocking the GitHub API.
    """
    # 1. Create a fake "Comment" object.
    mock_comment = mocker.Mock()
    mock_comment.html_url = "https://github.com/mock/issue/1#comment-123"

    # 2. Create a fake "Issue" object.
    mock_issue = mocker.Mock()
    mock_issue.create_comment.return_value = mock_comment

    # 3. Create a fake "Repo" object.
    mock_repo = mocker.Mock()
    mock_repo.get_issue.return_value = mock_issue

    # 4. Mock the get_github_repo helper.
    mocker.patch(
        "src.integrations.github_tools.get_github_repo", return_value=mock_repo
    )

    # 5. Run the actual tool.
    comment_body = "This is a test comment."
    result = github_tools.post_pr_comment(pr_number=1, comment_body=comment_body)

    # 6. Assert the results.
    assert "Successfully posted comment" in result
    assert mock_comment.html_url in result
    mock_repo.get_issue.assert_called_once_with(number=1)
    mock_issue.create_comment.assert_called_once_with(comment_body)
