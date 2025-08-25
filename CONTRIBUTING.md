# Contributing to VertexOps

We love your input! We want to make contributing to VertexOps as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## 🛠️ Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/vertexops.git
cd vertexops

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn vertexops.main:app --reload --host 127.0.0.1 --port 8080
```

## 📝 Pull Request Process

1. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
2. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
3. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## 🐛 Report bugs using GitHub's [issues](https://github.com/yourusername/vertexops/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/vertexops/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## 🎯 Feature Requests

We welcome feature requests! Please use GitHub issues and include:

- Use case description
- Expected behavior
- Current behavior (if applicable)
- Possible implementation approach

## 📋 Coding Standards

* Use [Black](https://black.readthedocs.io/) for Python code formatting
* Follow [PEP 8](https://pep8.org/) style guide
* Add type hints for all function parameters and return values
* Write docstrings for all public functions and classes
* Keep functions focused and small
* Use meaningful variable and function names

## 🧪 Testing

We use pytest for testing. Please write tests for any new functionality:

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=vertexops
```

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our project and our community a harassment-free experience for everyone.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

## 📞 Contact

Questions? Reach out via GitHub issues or discussions.

Thank you for contributing to VertexOps! 🚀
