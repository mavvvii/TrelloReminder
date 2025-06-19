# TRELLOREMINDER

*Transform Tasks Into Timely Triumphs Effortlessly*

![last-commit](https://img.shields.io/github/last-commit/mavvvii/TrelloReminder?style=flat&logo=git&logoColor=white&color=0080ff)
![repo-top-language](https://img.shields.io/github/languages/top/mavvvii/TrelloReminder?style=flat&color=0080ff)
![repo-language-count](https://img.shields.io/github/languages/count/mavvvii/TrelloReminder?style=flat&color=0080ff)

## Built with the tools and technologies:

![Markdown](https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white)
![TOML](https://img.shields.io/badge/TOML-9C4121.svg?style=flat&logo=TOML&logoColor=white)
![precommit](https://img.shields.io/badge/precommit-FAB040.svg?style=flat&logo=pre-commit&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat&logo=Poetry&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-5865F2.svg?style=flat&logo=Discord&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white)

---

## 📑 Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)

---

## 📌 Overview

TrelloReminder automatyzuje przypomnienia o zadaniach z tablic Trello, zapewniając płynny przepływ pracy i lepsze zarządzanie czasem. Dzięki integracji z Dockerem, Poetry i Discordem możesz łatwo zarządzać zadaniami w czasie rzeczywistym i otrzymywać powiadomienia bezpośrednio tam, gdzie ich potrzebujesz.

---

## 🚀 Getting Started

### 🔧 Prerequisites

Ten projekt wymaga:

- **Programming Language:** Python  
- **Package Manager:** Poetry  
- **Container Runtime:** Docker

---

### 💾 Installation

Zbuduj i zainstaluj TrelloReminder lokalnie:

#### 1. Sklonuj repozytorium

```sh
git clone https://github.com/mavvvii/TrelloReminder
```

#### 2. Przejdź do katalogu projektu

```sh
cd TrelloReminder
```

#### 3. Zainstaluj zależności

##### Za pomocą [Docker](https://www.docker.com/):

```sh
docker build -t mavvvii/TrelloReminder .
```

##### Za pomocą [Poetry](https://python-poetry.org/):

```sh
poetry install
```

---

### ▶️ Usage

#### Z Dockerem:

```sh
docker run -it {image_name}
```

#### Z Poetry:

```sh
poetry run python {entrypoint}
```

Zamień `{image_name}` i `{entrypoint}` na konkretne wartości zgodnie z konfiguracją projektu.

---

### ✅ Testing

TrelloReminder używa frameworka **{test_framework}** do testów.

#### Z Dockerem:

```sh
echo 'INSERT-TEST-COMMAND-HERE'
```

#### Z Poetry:

```sh
poetry run pytest
```

Zamień `{test_framework}` oraz `INSERT-TEST-COMMAND-HERE` na właściwe wartości (np. `pytest`).

---

[⬆ Return to Top](#trelloreminder)
