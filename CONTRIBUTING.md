# Contributing to pr-summary-github-action

Thank you for your interest in contributing to pr-summary-github-action! This document provides guidelines and steps for contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/nejcm/pr-summary-github-action.git
   cd pr-summary-github-action
   ```

## Development Setup

Install Python 3.12 or higher

Install dependencies:

```bash
pip install -r requirements.txt
```

## Making Changes

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Test your changes locally
4. Commit your changes using clear commit messages
5. Push to your fork
6. Submit a Pull Request

## Pull Request Guidelines

- Ensure your PR is targeted to the main branch
- Include a clear description of the changes
- Reference any related issues
- Make sure all tests pass
- Keep changes focused and atomic

## Testing

Test your changes by creating a workflow in your repository that uses your fork of the action. Ensure it works with:

- Different API providers (OpenAI, Anthropic)
- Different issue tracking tools (Linear)
- Notion integration

Run unit tests:

```bash
python -m unittest discover -s src
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Need Help?

Create an issue in the repository if you:

- Found a bug
- Have questions about the code
- Want to discuss new features

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

This CONTRIBUTING.md provides clear guidelines while keeping things concise and focused on the specific needs of your GitHub Action. Let me know if you'd like me to adjust anything!
