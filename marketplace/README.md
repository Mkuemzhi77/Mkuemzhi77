# P2P Market

> Учебный **P2P-маркетплейс цифровых товаров** (аналог Steam Community Market / Buff).  
> Docs-first: GitLab, CI/CD, roadmap, code review.

![status](https://img.shields.io/badge/status-planning-yellow)
![stack](https://img.shields.io/badge/backend-FastAPI-009688)
![db](https://img.shields.io/badge/db-PostgreSQL-336791)
![ci](https://img.shields.io/badge/CI-GitLab%20CI-fc6d26)

---

## О проекте

Платформа, где пользователи:

1. держат **виртуальный инвентарь** и **баланс**;
2. выставляют предметы на продажу (**Sell / listing**);
3. покупают чужие лоты (**Buy Now** → позже Buy orders);
4. получают **атомарную сделку** без double-sell при параллельных запросах.

Все предметы и деньги — **виртуальные** (без Steam API, без реальных платежей и аккаунтов).

### Зачем этот проект

| Цель | Как закрываем |
|------|----------------|
| Опыт backend / собесы | транзакции, race conditions, ledger, идемпотентность |
| Командная практика | GitLab flow, MR, CI, code review |
| Дисциплина поставки | roadmap по этапам, Definition of Done, тесты в пайплайне |

---

## Документация

| Документ | Содержание |
|----------|------------|
| [ROADMAP.md](./ROADMAP.md) | этапы, даты-ориентиры, DoD |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | ветки, MR, commit-сообщения, ревью |
| [docs/architecture.md](./docs/architecture.md) | модули, потоки, границы |
| [docs/domain.md](./docs/domain.md) | сущности, инварианты, сценарии |
| [docs/setup.md](./docs/setup.md) | локальный запуск |
| [docs/api.md](./docs/api.md) | черновик HTTP API |

Глубокий продуктово-технический разбор: [docs/deepdive.md](./docs/deepdive.md).

---

## Стек (v1)

| Слой | Выбор |
|------|--------|
| Backend | Python 3.12 + **FastAPI** |
| DB | **PostgreSQL** 16 |
| Миграции | Alembic |
| Auth | JWT |
| Frontend | React + TypeScript (Next.js — опционально) |
| Контейнеры | Docker Compose |
| CI/CD | **GitLab CI** (lint → test → build → deploy staging) |
| Тесты | pytest + интеграционные тесты на гонки |

> Стек можно сменить на Go — решение фиксируем до конца Этапа 0.  
> Главное не язык, а **PostgreSQL + атомарные сделки + CI**.

---

## Структура репозитория

```text
marketplace/
├── README.md                 # ты здесь
├── ROADMAP.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitlab-ci.yml
├── docker-compose.yml
├── docs/
│   ├── architecture.md
│   ├── domain.md
│   ├── setup.md
│   └── api.md
├── backend/                  # FastAPI (появится на этапе 1)
└── frontend/                 # React (появится на этапе 1–2)
```

---

## Быстрый старт (когда появится код)

```bash
# клон
git clone <gitlab-repo-url> p2p-market
cd p2p-market

# окружение
cp .env.example .env
docker compose up -d --build

# API:      http://localhost:8000
# docs:     http://localhost:8000/docs
# frontend: http://localhost:3000
```

Подробности: [docs/setup.md](./docs/setup.md).

---

## GitLab workflow

```text
issue → feature branch → Merge Request → CI (lint/test) → review → merge в main
                                                              ↓
                                                         deploy staging (manual/auto)
```

### Правила коротко

- В `main` только через **Merge Request**
- MR без зелёного пайплайна не мержим
- Одна задача = одна ветка: `feature/…`, `fix/…`, `docs/…`
- Перед крупной фичей — issue + чекпоинт в Roadmap

Полностью: [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## CI/CD пайплайн

Стадии в `.gitlab-ci.yml`:

| Stage | Что делает |
|-------|------------|
| `lint` | ruff / eslint |
| `test` | unit + integration (Postgres service) |
| `build` | Docker image |
| `deploy` | staging (manual на старте) |

Пайплайн обязателен до появления «толстого» кода: сначала docs/CI-скелет, потом реализация.

---

## MVP (Definition of Done)

- [ ] Регистрация / логин (JWT)
- [ ] Инвентарь + виртуальный баланс
- [ ] Создание / отмена listing
- [ ] Buy Now в **одной DB-транзакции**
- [ ] История сделок + ledger
- [ ] Интеграционный тест: N параллельных покупок → ровно 1 success
- [ ] CI зелёный на MR
- [ ] README + скрин/гифка демо

---

## Команда и роли

| Роль | Фокус |
|------|--------|
| Backend core | схема БД, trading/wallet, тесты гонок, CI |
| Fullstack / UI | auth UI, каталог, инвентарь, история, DX |

В первую неделю вместе: **схема БД + OpenAPI-контракт**.

---

## Безопасные границы (учебный проект)

**Делаем:** виртуальные item_id, виртуальная валюта, сиды предметов.  
**Не делаем в v1:** Steam trade bots, реальные платежи, продажа аккаунтов/ключей, микросервисный зоопарк.

---

## Статус

**Этап 0 — Planning / docs-first** (README, Roadmap, GitLab skeleton).  
Следующий шаг: Этап 1 — каркас backend + Postgres + CI test job.

См. [ROADMAP.md](./ROADMAP.md).

---

## Лицензия

Учебный проект. MIT (можно сменить позже).
