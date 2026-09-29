# Local setup

## Требования

- Docker + Docker Compose
- Git
- (опционально) Python 3.12, Node 20 — для запуска без контейнера API/UI

## Перенос на GitLab (этап 0)

Репозиторий: https://gitlab.com/myvibe-group/marketplacep2p

Каркас уже запушен в `main`. Дальше:

1. Settings → Repository → **Protected branches**: `main` (no direct push)
2. Invite members — одногруппник (Maintainer)
3. Issues / Milestones: `M0 Planning` … `M4 MVP` (см. ROADMAP)
4. CI/CD Variables позже: `DATABASE_URL`, `JWT_SECRET`

Повторный пуш содержимого этой папки как корня:

```bash
./scripts/push-to-gitlab.sh https://oauth2:<TOKEN>@gitlab.com/myvibe-group/marketplacep2p.git
```

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
