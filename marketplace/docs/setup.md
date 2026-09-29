# Local setup

## Требования

- Docker + Docker Compose
- Git
- (опционально) Python 3.12, Node 20 — для запуска без контейнера API/UI

## GitLab remote

После создания проекта в GitLab:

```bash
cd marketplace
git remote add gitlab git@gitlab.com:<group>/<project>.git
git push -u gitlab main
```

Protected branch `main`: Settings → Repository → Protected branches  
CI variables: Settings → CI/CD → Variables (`DATABASE_URL`, `JWT_SECRET`, …)

## Запуск (целевой)

```bash
cp .env.example .env
docker compose up -d --build
curl http://localhost:8000/health
```

Сейчас на этапе 0 compose поднимает только Postgres (API добавим на этапе 1).

## Полезные команды (появятся с кодом)

```bash
# миграции
docker compose exec api alembic upgrade head

# тесты
docker compose exec api pytest -q

# логи
docker compose logs -f api
```

## Типовые проблемы

| Симптом | Что проверить |
|---------|----------------|
| CI красный на test | сервис Postgres в job, `DATABASE_URL` |
| conflict на buy | так и должно для второго параллельного запроса |
| «password auth failed» | `.env` vs CI variables |

## Seed данных

На этапе 2: команда/скрипт `python -m app.seed` — пользователи demo + предметы + балансы.
