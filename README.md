# TRELLOREMINDER

*Never Miss a Trello Deadline*

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
- [Installation & Setup](#installation--setup)
  - [Docker Compose](#docker-compose)
  - [Poetry](#poetry)
- [Running Tests](#running-tests)
  - [Docker Compose](#docker-compose-1)
  - [Poetry](#poetry-1)
- [License](#license)

---

## 📌 Overview

TrelloReminder automates reminders for your Trello cards, ensuring you never miss a deadline. Receive notifications directly in Discord with zero hassle, and keep your workflow seamless and on-track.

Key features:

🕒 Periodic scanning of Trello boards and lists for upcoming due dates

🔔 Discord notifications with customizable timing (e.g., 1 day, 1 hour before due)

🐳 Easy deployment with Docker Compose or Poetry

⚙️ Full configuration via YAML or environment variables

---

## 🚀 Getting Started

### 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**
- **Poetry**   
- **Docker**
- **Docker Compose**

---

## 💾 Installation & Setup

Choose one of the setup methods below.

### 🐳 Docker Compose

1. Clone the repository:
```sh
git clone https://github.com/mavvvii/TrelloReminder.git
cd TrelloReminder
```
2.Copy the example environment file and provide your credentials:
```sh
cp .env.example .env
# Edit .env to set TRELLO_KEY, TRELLO_TOKEN, DISCORD_WEBHOOK_URL, etc.
```
3.Start the service:
```sh
docker-compose up -d --build
```
4.Tail the logs to verify it’s running:
```sh
docker-compose logs -f
```

### 📦 Poetry

1. Clone the repository:
```sh
git clone https://github.com/mavvvii/TrelloReminder.git
cd TrelloReminder
```
2.Copy the example environment file and provide your credentials:
```sh
cp .env.example .env
# Edit .env to set TRELLO_KEY, TRELLO_TOKEN, DISCORD_WEBHOOK_URL, etc.
```
3.Install dependencies:
```sh
poetry install
```
4.Run the application:
```sh
poetry run python -m src/main
```

---

## ✅ Running Tests
All tests are located in the tests/ directory at the project root. Framework that is use to testing is pytest.

Run tests via:
### 🐳 Docker Compose
```sh
docker-compose run --rm reminder_app pytest
```

### 📦 Poetry
```sh
poetry run pytest
```

---

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

[⬆ Return to Top](#trelloreminder)
