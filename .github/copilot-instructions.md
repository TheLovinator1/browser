# Copilot Instructions

- This project is a web browser based application that uses PySide 6 to create a GUI.
- This repo is split into two main parts: the Django API and the GUI.
- The Django API is used to store and retrieve data from the database. The GUI is used to display the data to the user.
- Use Python 3.12 or above for all examples and code snippets.
- We use uv for dependency management, so all examples and code snippets should use uv.
- Include type hints in all Python code examples and explanations.
- Organize Python code in accordance with Django conventions, and prefer modern Python features when applicable.
- Assume that the reader has an advanced understanding of Python and Django.
- Dark mode is preferred for design-related examples or suggestions.
- Use try-except blocks for error handling in all Python code examples.
- Add logging to all Python code examples.
- Write docstrings for all Python functions and classes.
- Prefetch related objects in Django ORM queries.
- Use database indexes in Django models. Our database is Sqlite.
- The project structure is the following:

    ```text
    .
    ├── .github
    │   └── copilot-instructions.md
    ├── src
    │   ├── api # Django API
    │   │   ├── config
    │   │   └── manage.py
    │   ├── browser # GUI
    │   │   └── main.py
    │   └── tests
    ├── manage.py
    ├── pyproject.toml
    └── README.md
    ```
