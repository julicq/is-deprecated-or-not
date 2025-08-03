# Установка и настройка Deprecated Checker

## Быстрая установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/deprecated-checker.git
cd deprecated-checker
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Проверка установки
```bash
python deprecated_checker.py --help
```

## Альтернативные способы установки

### Установка как пакет
```bash
pip install -e .
```

После установки можно использовать команду:
```bash
deprecated-checker check
```

### Установка в виртуальном окружении
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## Настройка

### 1. Конфигурация базы данных

База данных deprecated пакетов находится в файле `data/deprecated_packages.yaml`. 
Вы можете добавить новые пакеты или изменить существующие:

```yaml
package-name:
  deprecated_since: "2024-01-01"
  reason: "Причина deprecation"
  alternatives:
    - name: "alternative-package"
      reason: "Почему лучше"
      migration_guide: "https://example.com/migration"
```

### 2. Настройка CI/CD

#### GitHub Actions
Создайте файл `.github/workflows/deprecated-check.yml`:

```yaml
name: Check Deprecated Dependencies

on: [push, pull_request]

jobs:
  check-deps:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run deprecated checker
      run: |
        python deprecated_checker.py check --export json --output report.json
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: dependency-report
        path: report.json
```

#### GitLab CI
Добавьте в `.gitlab-ci.yml`:

```yaml
check_dependencies:
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python deprecated_checker.py check --export json --output report.json
  artifacts:
    reports:
      junit: report.json
```

### 3. Pre-commit hook

Создайте файл `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: deprecated-checker
        name: Check deprecated dependencies
        entry: python deprecated_checker.py check
        language: system
        pass_filenames: false
        always_run: true
```

Установите pre-commit:
```bash
pip install pre-commit
pre-commit install
```

### 4. Makefile

Создайте `Makefile` для удобства:

```makefile
.PHONY: check-deps check-deps-verbose check-deps-json update-db test

check-deps:
	python deprecated_checker.py check

check-deps-verbose:
	python deprecated_checker.py check --verbose

check-deps-json:
	python deprecated_checker.py check --export json --output deps-report.json

update-db:
	python deprecated_checker.py list-db

test:
	python test_checker.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .
```

## Использование

### Базовые команды

```bash
# Проверка текущей директории
python deprecated_checker.py check

# Проверка конкретной директории
python deprecated_checker.py check --path /path/to/project

# Подробный вывод
python deprecated_checker.py check --verbose

# Экспорт в JSON
python deprecated_checker.py check --export json

# Экспорт в YAML
python deprecated_checker.py check --export yaml

# Сохранение отчета в файл
python deprecated_checker.py check --export json --output report.json
```

### Работа с базой данных

```bash
# Просмотр всех deprecated пакетов
python deprecated_checker.py list-db

# Поиск конкретного пакета
python deprecated_checker.py search requests
```

## Поддерживаемые файлы

Утилита автоматически обнаруживает и анализирует следующие файлы:

- `requirements.txt`
- `requirements-dev.txt`
- `setup.py`
- `pyproject.toml`

## Устранение неполадок

### Проблема: "ModuleNotFoundError"
```bash
# Убедитесь, что все зависимости установлены
pip install -r requirements.txt
```

### Проблема: "Permission denied"
```bash
# Установите права на выполнение
chmod +x deprecated_checker.py
```

### Проблема: "No module named 'toml'"
```bash
# Установите недостающую зависимость
pip install toml
```

## Разработка

### Установка для разработки
```bash
git clone https://github.com/yourusername/deprecated-checker.git
cd deprecated-checker
pip install -e .
pip install -r requirements.txt
```

### Запуск тестов
```bash
python test_checker.py
```

### Добавление новых тестов
Создайте новые тесты в файле `test_checker.py` или создайте отдельные файлы тестов.

## Лицензия

MIT License - см. файл LICENSE для подробностей.

## Поддержка

Если у вас есть вопросы или проблемы:

1. Создайте issue в GitHub
2. Проверьте документацию в README.md
3. Посмотрите примеры в examples.md 