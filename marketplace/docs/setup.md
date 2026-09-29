# Local setup

## Требования

- Docker + Docker Compose
- Git
- (опционально) Python 3.12, Node 20 — для запуска без контейнера API/UI

## Перенос на GitLab (этап 0)

1. Создай **новый пустой** проект на GitLab (без README/LICENSE — чтобы не было конфликта).
2. Скопируй URL вида `https://gitlab.com/<group>/<project>.git` или SSH.
3. Из каталога `marketplace/`:

```bash
./scripts/push-to-gitlab.sh git@gitlab.com:<group>/<project>.git
```

Скрипт выгружает содержимое папки как **корень** нового репозитория.

Рекомендуемый способ для пары: один создаёт GitLab-проект, добавляет второго Maintainer, пушите только `marketplace/` как корень.

### GitLab settings после первого push

- Settings → Repository → **Protected branches**: `main` (no direct push)
- Settings → CI/CD → **Variables**: позже `DATABASE_URL`, `JWT_SECRET`
- Settings → Merge requests: pipeline success + 1 approval (по желанию)
- Issues / Milestones: `M0 Planning` … `M4 MVP` (см. ROADMAP)

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
