# Kịch bản tự động hóa tích hợp liên tục CI/CD của ChatGPT - Version 1.0
name: DreamForge Engine CI Pipeline

on:
  push:
    branches: [ "main", "feature/*" ]
  pull_request:
    branches: [ "main" ]

jobs:
  run-integration-tests:
    runs-on: ubuntu-latest

    steps:
    # Bước 1: Trích xuất và nạp mã nguồn thật từ kho lưu trữ GitHub
    - name: Checkout Source Code
      uses: actions/checkout@v4

    # Bước 2: Khởi tạo môi trường lập trình Python độc lập trên đám mây
    - name: Set up Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"

    # Bước 3: Cài đặt tự động các thư viện (cài dependencies theo đặc tả ChatGPT)
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install sqlalchemy alembic

    # Bước 4: Khởi chạy bộ 26 ca kiểm thử liên tầng (chạy test & báo kết quả)
    - name: Run Supreme Unit Test Suites
      env:
        PYTHONPATH: src
      run: |
        python -m unittest discover tests