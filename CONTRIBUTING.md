# Contributing to Restaurant AI Assistant

Thank you for your interest in contributing to this project! This is a teaching project, so contributions that help make it clearer and more beginner-friendly are especially welcome.

## 🎯 How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/restaurant-ai-model.git
cd restaurant-ai-model
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment

```bash
# Install all dependencies
make install-dev

# Or manually:
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
pip install -r requirements-dev.txt
```

### 4. Make Your Changes

- Keep code clean and simple (this is a teaching project!)
- Follow PEP 8 for Python
- Follow ESLint rules for JavaScript
- Add comments for complex logic
- Write tests for new features

### 5. Test Your Changes

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Check code quality
make lint

# Format code
make format
```

### 6. Commit and Push

```bash
git add .
git commit -m "feat: add descriptive commit message"
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

- Provide a clear description of your changes
- Link any related issues
- Ensure CI/CD checks pass

## 🏗️ Project Structure Review

```
backend/
  ├── main.py                 # FastAPI app - Add endpoints here
  └── requirements.txt        # Python dependencies

frontend/
  ├── src/
  │   ├── App.jsx            # Main component - Modify chat UI here
  │   └── App.css            # Styling - Improve design here
  └── package.json           # Dependencies

tests/
  └── test_restaurant_assistant.py  # Add test cases here
```

## 📝 Code Style Guidelines

### Python
- Use Black for formatting: `black backend/`
- Use isort for imports: `isort backend/`
- Max line length: 100 characters
- Add docstrings to functions

```python
def send_message(message: str) -> str:
    """Send message to chatbot and get response."""
    response = requests.post(API_URL, json={"message": message})
    return response.json()["reply"]
```

### JavaScript/React
- Use modern ES6+ syntax
- Use meaningful variable names
- Add comments for complex logic
- Keep components small and focused

```jsx
function ChatMessage({ message, isUser }) {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {message}
    </div>
  )
}
```

## 🧪 Testing Guidelines

- Write tests for new features
- Test happy paths and edge cases
- Use descriptive test names
- Keep tests simple and focused

```python
def test_handles_party_size():
    """Should match party size to appropriate table."""
    response = send_message("I need a table for 4 people")
    assert "4" in response or "Table" in response
```

## 🐛 Reporting Bugs

1. Check if the bug already exists in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment info (OS, Python version, etc.)

## 💡 Suggesting Improvements

- Open a discussion in Issues
- Describe the improvement
- Explain why it would help
- Keep it beginner-friendly

## 📚 Documentation

- Update README.md if you change features
- Add docstrings to new functions
- Update API docs if you change endpoints
- Add comments to complex logic

## 🚀 Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Added tests for new features
- [ ] All tests pass locally
- [ ] Updated documentation
- [ ] No breaking changes
- [ ] Commit messages are clear

## 🎓 Learning Focus Areas

This project is designed to teach:
- **Full-stack development** - React + FastAPI
- **AI integration** - Working with LLM APIs
- **Testing LLMs** - Using DeepEval framework
- **Clean code** - Writing maintainable, simple code
- **DevOps basics** - Docker, CI/CD, deployment

When contributing, keep these learning goals in mind!

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn
- Share knowledge
- Welcome feedback
- Have fun! 🎉

## 📞 Questions?

- Check the README.md
- Review DEEPEVAL_GUIDE.md for testing
- Open an issue for questions
- Join discussions

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's license.

---

**Thank you for contributing! You're helping make AI education better for everyone! 🚀**
