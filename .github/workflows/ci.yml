name: DreamForge Engine CI Pipeline

on:
  push:
    branches: [ main, feature/*, release/* ]
  pull_request:
    branches: [ main ]

jobs:
  run-integration-tests:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Source Code From Repository
      uses: actions/checkout@v4

    - name: Set Up Python Environment
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install System and Project Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install sqlalchemy pyperclip google-generativeai openai

    - name: Execute Automated Test Suite (Nghiệm thu Milestone)
      run: |
        python -m unittest discover tests
