from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.conf import settings
from github import Auth, Github, UnknownObjectException

if TYPE_CHECKING:
    from github.ContentFile import ContentFile
    from github.Repository import Repository

logger: logging.Logger = logging.getLogger(__name__)

auth = Auth.Token(settings.GITHUB_ACCESS_TOKEN)
logger.info("Github auth token set %s", auth)


def get_repo_contents(username: str, repo_name: str) -> list[ContentFile] | ContentFile:
    """Get all of the contents of the root directory of the repository.

    Args:
        username (str): The username of the repository owner.
        repo_name (str): The name of the repository.

    Returns:
        list[ContentFile] | ContentFile: The contents of the root directory.
    """
    with Github(auth=auth) as g:
        repository_identifier: str = f"{username}/{repo_name}"
        logger.info("Getting contents of %s", repository_identifier)

        try:
            repo: Repository = g.get_repo(repository_identifier)
        except UnknownObjectException:
            logger.exception("Repository not found")
            return []

        contents: list[ContentFile] | ContentFile = repo.get_contents("")
        return contents
