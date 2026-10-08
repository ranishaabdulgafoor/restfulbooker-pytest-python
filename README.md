# Restful-Booker REST API Modular Testing Automation Framework

An enterprise-ready, data-driven API regression automation framework modeled inside a Python/PyTest runtime matrix environment. This platform validates the structural CRUD integrity, authentication state boundaries, and role-based access configurations of a live hotel management web system.

## 🏛️ Framework Structural Design Architecture
The workspace architecture isolates procedural execution layers away from static global environmental property parameters:
* `config/` - Houses isolated environmental variables and backend target base destination paths.
* `postman_collections/` - Stores raw automated request blueprints exported from manual discovery loops.
* `utils/` - Contains contextual tracking logging mechanics designed to capture transaction logs on failures.
* `tests/` - Holds modularized state-assertion validation suites mapped to explicit sequential lifecycle scripts.
* `reports/` - Generates dynamic self-contained interactive HTML test execution dashboards on runtime calls.

## 🔄 Core End-to-End API Transaction Flow
1. **GET /ping** - Baseline verification testing environmental server pipeline availability.
2. **POST /auth** - Authenticates session admin credentials to extract dynamic temporary authorization tokens.
3. **POST /booking** - State generation check-in payload transaction creating a unique dynamic `bookingid`.
4. **GET /booking/{id}** - Asserts system state storage and record integrity configurations.
5. **PUT /booking/{id}** - Requires administrative authorization tokens to trigger full resource records replacements.
6. **PATCH /booking/{id}** - Executes a surgical single-field property modification while preserving target attributes.
7. **DELETE /booking/{id}** - Purges entity properties safely from the server instance layer.
8. **GET /booking/{id}** - Teardown verification audit asserting that query criteria correctly yields an absolute 404 block.
9. **Negative Bounds Validation** - Multi-case boundary injection checks confirming robust token rejection error handling.

## 🚀 Deployment and Execution Guide

### 1. Initialize and Activate the Isolated Workspace Virtual Sandbox
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Synchronize Production Package Dependencies
```bash
pip install pytest requests pytest-html
```

### 3. Trigger the Suite Matrix and Generate Interactive HTML Reports
```bash
pytest -s -v --html=reports/dashboard.html --self-contained-html
```
