<h1 align="center"> 🤖 Reprebot </h1>

<div align="center">
  <h3>Welcome to <b>Reprebot</b>!</h3>

A chatbot to answer questions for the Faculty of Engineering community at the
National University of Colombia.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/91b3b1c0dca44a828461a62a5ffe032e)](https://app.codacy.com/gh/Represoft/reprebot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/91b3b1c0dca44a828461a62a5ffe032e)](https://app.codacy.com/gh/Represoft/reprebot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

</div>

## Introduction 🚀

**Reprebot** uses a method called Retrieval Augmented Generation (RAG).
This technique involves utilizing a Language Model (LLM) to generate text using
a specific context of information stored in a vector database. In this case,
the context revolves around information related to the academic processes within
the Faculty of Engineering.

## Scope 🔭

**Reprebot** will initially be a microservice containerized and ready to be
incorporated in any architecture. In the future we may implement a user-friendly
interface so that the community can access it in the web at any time. Or it may
be integrated in any of the other systems of the Faculty of Engineering.

## Purpose 🎯

**Reprebot** has the following main objectives:

- **Quick Help:** Provide fast responses to the Faculty of Engineering community
  whenever they need assistance, eliminating the need for emails or visiting
  various departments.

- **Student Support:** Assist students throughout their academic journey by
  offering information on processes, events, and career opportunities.

- **Reduce Workload:** Ease the workload of **Repreisis** and other dependencies
  within the Faculty of Engineering, enabling them to concentrate on more
  impactful tasks and better address student needs.

## Getting Involved 🙌

There are various ways to contribute to **Reprebot**:

- **Join the Team:** Interested in being part of the project? Express your
  interest in joining our team of dedicated volunteers by reaching out to
  **Repreisis** through any of their communication channels.

- **Contribute:** Share your ideas by submitting them to our
  [issues](https://github.com/Represoft/reprebot/issues) backlog.
  Check out our [contributing](CONTRIBUTING.md) guidelines and start
  collaborating.

- **Provide Feedback:** Let us know how Reprebot can be enhanced. Your feedback
  is valuable, and you can reach out to **Repreisis** directly or share your
  ideas in our [issues](https://github.com/Represoft/reprebot/issues) backlog.

- **Spread the Word:** Help us broaden Reprebot's impact by telling your friends
  and peers about its capabilities and benefits within the Faculty of
  Engineering community.

## How to Get Started?

1. Install [Python](https://www.python.org/downloads/).
2. Install [Git](https://git-scm.com/downloads).
3. Install [pip](https://pip.pypa.io/en/stable/installation/).
4. Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
5. Create a [GitHub](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) account if you don't have one.
6. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the [reprebot](https://github.com/Represoft/reprebot) repository.
7. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) your fork.
8. [Create](https://docs.python.org/3/library/venv.html) a virtual environment
   inside your cloned repository: `python3 -m venv env`.
9. [Activate](https://docs.python.org/3/tutorial/venv.html) the virtual
   environment. On Windows, run `env\Scripts\activate`, and on Linux run
   `source env/bin/activate`.
10. Install the dependencies: `pip install -r requirements.txt`.
11. Run the unit tests: `pytest test/unit/src`.
12. Now your ready to start sending your contributions. See this
    [guide](https://github.com/Represoft/reprebot/blob/main/CONTRIBUTING.md).

### To run the context builder scripts:

1. Navigate to the folder of the script you want to run.
2. Execute the `main.py` script.

For example:

```sh
cd src/context_builder/faculty_secretary_faq
py main.py
```

### To start the API:

1. Navigate to the `api` module folder.
2. Start the web service.

```sh
cd src/api
uvicorn main:app --reload
```
3. You can test the API endpoint at `http://127.0.0.1:8000`.

## Technical Details ⚙️

### Programming Languages 🖥️

- **Python**

### Dependencies 🛠️

Reprebot relies on the following dependencies:

- `beautifulsoup4`
- `chromadb`
- `coverage`
- `cryptography`
- `fastapi`
- `Jinja2`
- `langchain`
- `langchain-openai`
- `pytest`
- `requests`
- `transformers`
- `uvicorn`

For a comprehensive list of dependencies, including both direct and transitive
dependencies, please refer to the `requirements.txt` file.
