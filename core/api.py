from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.core.handlers.wsgi import WSGIRequest  # noqa: TC002
from ninja import Router

from core.sites_github import get_repo_contents

if TYPE_CHECKING:
    from github.ContentFile import ContentFile

logger: logging.Logger = logging.getLogger(__name__)

router = Router()
github_router = Router()

router.add_router("/github/", github_router)


def convert_content_file_to_json(content_file: ContentFile) -> dict[str, str | int]:
    """Convert a ContentFile object to a dictionary.

    Args:
        content_file (ContentFile): The ContentFile object.

    Returns:
        dict[str, str]: The ContentFile object as a dictionary.
    """
    return {
        "name": content_file.name,
        "path": content_file.path,
        "type": content_file.type,
        "download_url": content_file.download_url,
        "html_url": content_file.html_url,
        "size": content_file.size,
        "sha": content_file.sha,
    }


@github_router.get("repos/{username}/{repo_name}/contents/")
def api_get_repo_contents(
    request: WSGIRequest,  # noqa: ARG001
    username: str,
    repo_name: str,
) -> list[dict[str, str | int]] | dict[str, str | int]:
    """Get all of the contents of the root directory of the repository.

    Args:
        request (WSGIRequest): The request object.
        username (str): The username of the repository owner.
        repo_name (str): The name of the repository.

    Returns:
        list[dict[str, str]]: The contents of the root directory
    """
    logger.info("Getting contents of %s/%s", username, repo_name)
    contents: list[ContentFile] | ContentFile = get_repo_contents(username, repo_name)

    if isinstance(contents, list):
        return [convert_content_file_to_json(content_file) for content_file in contents]
    return convert_content_file_to_json(contents)
