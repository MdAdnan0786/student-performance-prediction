# Contributing Guide

## Project Maintenance

### Documentation Files

This project maintains several documentation files:

- **README.md** - Main project documentation with setup and usage instructions
- **backend/README.md** - Backend API documentation and endpoints
- **backend/CHANGELOG.md** - Version history and changes
- **CONTRIBUTING.md** - This file - maintenance and contribution guidelines

### Code Organization

#### Backend (`backend/`)
- `main.py` - FastAPI application with ML models and API endpoints
- `start_server.py` - Simple Python launcher for the backend server
- `run_server.py` - Alternative launcher with detailed logging
- `test_run.py` - Diagnostic script for testing imports
- `requirements.txt` - Python dependencies

#### Frontend (`src/`)
- `App.tsx` - Main React application component
- `components/` - React components (PredictionForm, ResultsDisplay, ModelInfo)
- `main.tsx` - Application entry point

#### Startup Scripts
- `start.ps1` - PowerShell script to launch both servers
- `start.bat` - Windows batch script to launch both servers

### Git Workflow

1. **Check Status**
   ```bash
   git status
   ```

2. **Add Changes**
   ```bash
   git add .
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Descriptive commit message"
   ```

4. **Pull Latest Changes**
   ```bash
   git pull origin main --rebase
   ```

5. **Push Changes**
   ```bash
   git push origin main
   ```

### .gitignore Maintenance

The `.gitignore` file excludes:
- Python bytecode and cache (`__pycache__/`, `*.pyc`)
- Node modules (`node_modules/`)
- Build outputs (`dist/`, `build/`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Test and log files (`*_output.txt`, `*_log.txt`, `*_check.txt`)
- Environment variables (`.env`)
- ML model files (`*.pkl`, `*.joblib`)
- Temporary files (`*.tmp`, `*.bak`)

### Adding New Features

When adding new features:

1. **Update Documentation** - Modify relevant .md files
2. **Update Dependencies** - Add to `requirements.txt` (backend) or `package.json` (frontend)
3. **Test Thoroughly** - Run both servers and test the feature
4. **Commit Changes** - Use descriptive commit messages
5. **Update CHANGELOG** - Document the change in `backend/CHANGELOG.md`

### Running Tests

**Backend:**
```bash
cd backend
python -m pytest  # If tests are added
```

**Frontend:**
```bash
npm run typecheck  # TypeScript validation
npm run lint       # Code linting
```

### Deployment Checklist

Before deploying:
- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] .gitignore excludes all temporary files
- [ ] Dependencies are documented
- [ ] API endpoints are documented
- [ ] Version numbers are updated
- [ ] Changelog is updated
- [ ] Code is committed and pushed

### Version Control

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Document changes in `backend/CHANGELOG.md`
- Tag releases: `git tag -a v1.0.0 -m "Release version 1.0.0"`

### Issues and Bugs

When reporting issues:
1. Describe the expected behavior
2. Describe the actual behavior
3. Include error messages and logs
4. Specify your environment (OS, Python version, Node version)
5. List steps to reproduce

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where appropriate
- Document functions with docstrings

**TypeScript/React:**
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Use Tailwind CSS for styling

### Useful Commands

**Backend:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start server (simple)
python start_server.py

# Start server (uvicorn)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

**Both:**
```bash
# Windows PowerShell
.\start.ps1

# Windows Command Prompt
start.bat
```

## Getting Help

- Check the README.md for setup instructions
- Review backend/README.md for API documentation
- Check existing issues on GitHub
- Read error messages carefully - they often contain solutions

## License

This project is for educational purposes.
