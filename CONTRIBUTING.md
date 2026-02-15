# Contributing to Deshrupantor Scraper

Thank you for your interest in contributing! Here are some guidelines.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

### Suggesting Enhancements

We welcome feature requests! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- How it should work

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test your changes
5. Commit with clear messages (`git commit -am 'Add new feature'`)
6. Push to your fork (`git push origin feature/your-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/deshrupantor-scraper.git
cd deshrupantor-scraper

# Install dependencies
pip install -r requirements.txt

# Run the scraper locally
python scraper.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing

Before submitting a PR:
- Test the scraper runs without errors
- Verify XML output is valid
- Check that new articles are added correctly
- Ensure max article limit works

## Questions?

Feel free to open an issue for any questions!
