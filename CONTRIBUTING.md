# Contributing Guidelines

Thank you for contributing to **UruQAI – Multi-Risk Logistics Platform**!

## Workflow
1. Fork the repository.
2. Create a branch:  
   `git checkout -b feat/<feature-name>`
3. Implement your feature or fix.
4. Run `make test` and ensure all checks pass.
5. Submit a Pull Request (PR) into `main`.

## Commit Convention
Use **Conventional Commits**:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` add or update tests
- `chore:` minor maintenance

Example:  
`feat: add QAOA logistics optimizer`

## Code Style
- Python ≥ 3.10
- `black`, `ruff`, and `mypy` are used for linting and formatting.
- Tests: `pytest` in the `tests/` folder.

## Data Policy
- Do **not** commit raw or private datasets.
- Add `.sample` config files for reproducibility.
- Document every dataset in `data/README.md`.

## Pull Requests
Before submitting:
- [ ] Lint and test pass  
- [ ] Docs updated  
- [ ] No credentials or tokens in code
