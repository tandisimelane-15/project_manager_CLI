# Project Manager CLI

## Description

Project Manager CLI is a command-line application built with Python that enables users to manage projects and tasks efficiently. The application allows users to create accounts, create projects, add tasks, view stored information, and mark tasks as completed. All data is stored persistently using JSON, ensuring information is retained between sessions.

## Features

* Create user accounts
* List all registered users
* Create projects for users
* View user projects
* Add tasks to projects
* View project tasks
* Mark tasks as completed
* Edit existing tasks
* Delete tasks
* Allow system operators to manage users, projects, and tasks
* Validate user input
* Store data using JSON
* Automated testing with pytest

## Technologies Used

* Python 3
* Object-Oriented Programming (OOP)
* argparse
* rich
* JSON
* pytest
* Pipenv
* Git
* GitHub

## Installation

1. Clone the repository.

```bash
git clone <https://github.com/tandisimelane-15/project_manager_CLI>
```

2. Navigate into the project folder.

```bash
cd project_manager
```

3. Install the project dependencies.

```bash
pipenv install
```

4. Activate the virtual environment.

```bash
pipenv shell
```

## How to Run the Project

The application opens an interactive menu where you can:

1. Add User
2. List Users
3. Add Project
4. List Projects
5. Add Task
6. List Tasks
7. Complete Task
8. Edit Task
9. Delete Task
10. Exit

Alternatively, you can still use command-line commands directly:

```bash
python main.py --help
```

## Running Tests

Run all automated tests using:

```bash
pytest tests/ -v
```

A successful test run should display:

```text
15 passed
```

## Future Improvements

* Add user authentication
* Add project deadlines
* Add task priorities
* Add task due dates
* Add search functionality
* Export reports to CSV or PDF
* Replace JSON storage with SQLite

## Author

**Abigail Tandiwe**

* GitHub: https://github.com/tandisimelane-15
* LinkedIn: https://www.linkedin.com/in/abigailtandi
* Email: [tandisimelane24@gmail.com](mailto:tandisimelane24@gmail.com)

## License

MIT License

Copyright (c) 2026 Abigail Tandiwe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
