# Contributing to EGX Intelligence

Thank you for your interest in contributing to the EGX Intelligence project! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please treat everyone with respect and follow these principles:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### 1. Report Bugs

If you find a bug, please create an issue with the following information:

**Title**: A clear, descriptive title

**Description**:
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots or error messages (if applicable)

**Environment**:
- Python version
- Operating system
- List of installed packages (output of `pip freeze`)

**Labels**: `bug`, `priority-level`

### 2. Suggest Enhancements

We welcome feature requests and improvement suggestions!

**Title**: A clear title starting with `[Feature Request]`

**Description**:
- Describe the enhancement
- Explain the use case and benefit
- List any alternative approaches you've considered

**Labels**: `enhancement`, `feature-request`

### 3. Submit Pull Requests

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/egx-intelligence.git
   cd egx-intelligence
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/bug-description
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   # Optional: pip install pytest pytest-cov black flake8
   ```

#### Development Guidelines

**Code Style**:
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

**Example Function**:
```python
def analyze_signal_strength(text: str, keywords: List[str]) -> int:
    """
    Calculate signal strength based on keyword frequency.
    
    Args:
        text: Text to analyze
        keywords: List of keywords to search for
        
    Returns:
        Strength score (0 or higher)
    """
    strength = 0
    for keyword in keywords:
        strength += text.lower().count(keyword)
    return strength
```

**Comments**:
- Write clear comments explaining complex logic
- Comment on the "why", not the "what"
- Keep comments up-to-date with code changes

**Testing**:
- Write tests for new features
- Ensure existing tests still pass
- Aim for at least 80% code coverage

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=scripts
```

#### Making Changes

1. **Create your changes** in the appropriate file/directory
2. **Write or update tests** for your changes
3. **Format your code** (if using black):
   ```bash
   black scripts/
   ```

4. **Lint your code**:
   ```bash
   flake8 scripts/
   ```

5. **Test your changes**:
   ```bash
   python3 scripts/run_pipeline.py --steps analyze
   ```

#### Commit Messages

Write clear, descriptive commit messages:

**Format**:
```
[TYPE] Brief description (50 chars max)

Detailed explanation of the changes (70 chars per line)

Fixes #123
```

**Types**:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples**:
```
feat: Add support for multiple news sources

Implements fetching from Mubasher, Arab Finance, Al-Borsa, and HAPI.
Adds configuration options for source selection and parameters.

Fixes #42
```

```
fix: Handle missing data in analyze_signals

Added null checks for empty announcement lists to prevent errors
when data sources return no results.

Fixes #58
```

#### Pull Request Process

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to related issues (`Fixes #123`)
   - Screenshots or examples (if applicable)
   - Checklist of completed items

3. **PR Checklist**:
   ```markdown
   - [ ] Code follows style guidelines
   - [ ] Self-review of own code completed
   - [ ] Comments added for complex logic
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] All tests passing
   - [ ] No new warnings generated
   ```

4. **Respond to feedback**
   - Address reviewer comments
   - Re-request review after making changes
   - Discuss disagreements constructively

### 4. Improve Documentation

Documentation improvements are valuable contributions!

**Areas for improvement**:
- README clarifications
- Docstring improvements
- Usage examples
- Troubleshooting guides
- API documentation

**How to contribute**:
1. Identify unclear or missing documentation
2. Create a branch for documentation
3. Make improvements
4. Submit a PR with clear explanations

## Development Workflow

### Project Structure
```
egx-intelligence/
├── scripts/                 # Main Python scripts
│   ├── fetch_egx_announcements.py
│   ├── fetch_fra_announcements.py
│   ├── fetch_financial_news.py
│   ├── analyze_signals.py
│   ├── generate_report.py
│   └── run_pipeline.py
├── data/                    # Generated data (ignored in git)
├── reports/                 # Generated reports (ignored in git)
├── logs/                    # Log files (ignored in git)
├── config.ini               # Configuration file
├── requirements.txt         # Dependencies
├── README.md               # Main documentation
└── CONTRIBUTING.md         # This file
```

### Adding New Features

**Steps**:

1. **Create issue** to discuss the feature
2. **Update config.ini** with any new configuration options
3. **Create/modify script** in `scripts/` directory
4. **Add help text** with `--help` option
5. **Update `run_pipeline.py`** if adding a pipeline step
6. **Add tests** for new functionality
7. **Update README.md** with usage documentation
8. **Submit PR** with clear description

**Example: Adding a new data source**

1. Create `scripts/fetch_new_source.py`:
```python
#!/usr/bin/env python3
"""Fetch data from New Source."""

import argparse
import json
from datetime import datetime

def fetch_data(output_file: str):
    """Fetch data from new source."""
    data = {
        "source": "new_source",
        "timestamp": datetime.now().isoformat(),
        "items": []
    }
    
    # Implementation here
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    fetch_data(args.output)
```

2. Update `run_pipeline.py` to include new step
3. Add configuration options to `config.ini`
4. Update README with usage instructions

## Areas We Need Help With

- 🐛 **Bug fixes** - Tackle open issues
- 📚 **Documentation** - Improve guides and examples
- 🧪 **Testing** - Add unit and integration tests
- ✨ **Features** - Implement requested enhancements
- 🔍 **Code review** - Review open PRs and provide feedback
- 🌍 **Localization** - Help translate to other languages

## Recognition

Contributors are recognized in:
- GitHub contributor graph
- CONTRIBUTORS.md file
- Release notes

## Questions?

- **Issues**: Use GitHub Issues for discussions
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the maintainers directly

## License

By contributing to EGX Intelligence, you agree that your contributions will be licensed under the same license as the project.

## Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

Thank you for contributing to EGX Intelligence! 🙏

Your efforts help make this project better for everyone.
