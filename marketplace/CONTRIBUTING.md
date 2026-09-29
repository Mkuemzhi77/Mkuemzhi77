# Contributing — P2P Market

Процесс: issue → ветка → MR → CI → review → merge.

---

## 1. Перед кодом

1. Прочитай [README.md](./README.md) и [docs/domain.md](./docs/domain.md)
2. Возьми issue из текущего milestone ([ROADMAP.md](./ROADMAP.md))
3. Если issue нет — создай: проблема, DoD, критерии приёмки

---

## 2. Ветки

| Тип | Шаблон | Пример |
|-----|--------|--------|
| Фича | `feature/<short>` | `feature/buy-now-transaction` |
| Фикс | `fix/<short>` | `fix/listing-cancel-race` |
| Доки | `docs/<short>` | `docs/api-buy-endpoint` |
| CI/chore | `chore/<short>` | `chore/gitlab-test-postgres` |

- Базовая ветка: `main` (protected)
- Не пушим в `main` напрямую
- Одна ветка ≈ один issue

---

## 3. Commit-сообщения

Формат:

```text
type(scope): short summary

optional body
```

Типы: `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`

Примеры:

```text
feat(trading): atomic buy for listings
test(trading): parallel buy race integration
docs(api): describe Idempotency-Key
ci: add postgres service to test job
```

---

## 4. Merge Request

### Чеклист автора

- [ ] MR связан с issue (`Closes #123`)
- [ ] Описание: что сделано / как проверить
- [ ] Локально: lint + tests зелёные
- [ ] CI на MR зелёный
- [ ] Нет секретов в коде / `.env` не закоммичен
- [ ] Миграции обратимы или описан rollback

### Шаблон описания MR

```markdown
## What
…

## Why
…

## How to test
1. …
2. …

## Screenshots / logs
(если UI или гонка)

Closes #…
```

### Ревью

- Нужен **1 approve** (второй участник)
- Смотрим: корректность транзакций, краевые случаи, читаемость тестов
- «Нитрайте» по делу; спорные решения — коротко в треде, потом ADR в `docs/` если надо

---

## 5. Code style

### Backend
- Типы / pydantic-схемы на границах API
- Бизнес-логика сделок — в сервисах, не в роутерах
- Любая смена баланса/владельца — **в транзакции**
- Тест на гонку обязателен для trading-изменений

### Frontend
- TypeScript strict
- Никаких секретов в клиенте
- Состояния загрузки/ошибок на buy/listing

---

## 6. Тесты

| Уровень | Когда обязателен |
|---------|------------------|
| Unit | чистые функции (pricing, state transitions) |
| Integration | любые изменения wallet / listing / buy |
| Race | обязательно для buy / cancel listing |

Без зелёного race-теста MR в trading **не мержим**.

---

## 7. Releases

- MVP: тег `v0.1.0` после закрытия этапа 4
- Пишем запись в `CHANGELOG.md`
- Staging deploy — manual job в GitLab

---

## 8. Communication

- Крупные решения (стек, модель ордеров) — в issue или `docs/`
- Ежедневный sync не обязателен; блокеры — сразу в issue / чат
- Не держим MR > 3 дней без апдейта
