# Roadmap — P2P Market

Дорожная карта: этапы, цели, Definition of Done, что явно **не** входит в этап.

Ориентир по календарю условный (пары / вечерами). Длительности — в объёме работ, не в «календарных неделях обязательств».

---

## Обзор этапов

| Этап | Название | Цель | Статус |
|------|----------|------|--------|
| 0 | Planning & GitLab | README, roadmap, CI skeleton, правила | **in progress** |
| 1 | Foundation | Auth, DB, docker, CI test | planned |
| 2 | Inventory & Listings | инвентарь, sell listing, каталог | planned |
| 3 | Trading Core | Buy Now + гонки + ledger | planned |
| 4 | MVP UI & Polish | фронт, идемпотентность, демо | planned |
| 5 | Order Book Lite | buy orders + простой match | optional |
| 6 | Realtime & Ops | WS-лента сделок, staging deploy | optional |

```text
0 docs/CI → 1 foundation → 2 listings → 3 trading → 4 MVP demo
                                              ↘ 5 order book → 6 realtime
```

---

## Этап 0 — Planning & GitLab

**Цель:** одинаковое понимание продукта и процесса у обоих.

### Deliverables
- [x] `README.md`
- [x] `ROADMAP.md`
- [x] `CONTRIBUTING.md`
- [x] `docs/architecture.md`, `domain.md`, `api.md`, `setup.md`
- [x] `.gitlab-ci.yml` (скелет стадий)
- [x] `docker-compose.yml` (postgres (+ api stub later))
- [ ] GitLab project создан, protected `main`, templates issues/MR
- [ ] 2–3 стартовых issue (foundation / listing / buy)

### DoD
- Оба участника прочитали README + domain
- Есть GitLab-репо и доступ у обоих
- Согласован стек (FastAPI или Go) — зафиксировать в README

### Out of scope
Код бизнес-логики, UI.

---

## Этап 1 — Foundation

**Цель:** поднимается пустой, но «взрослый» каркас.

### Deliverables
- [ ] Backend skeleton (FastAPI): healthcheck, settings, logging
- [ ] PostgreSQL + Alembic + первая миграция `users`
- [ ] JWT register/login
- [ ] Docker Compose: `db` + `api`
- [ ] CI: `lint` + `test` (хотя бы health + auth smoke)
- [ ] `.env.example`

### DoD
- `docker compose up` поднимает API
- MR с тестом auth проходит в GitLab CI
- `/docs` отдаёт OpenAPI

### Out of scope
Маркет, инвентарь, сделки.

---

## Этап 2 — Inventory & Listings

**Цель:** продавец может выставить предмет.

### Deliverables
- [ ] Справочник `items` + seed (10–20 предметов)
- [ ] `inventories` (владение, статусы `available|listed`)
- [ ] `wallets` (balance)
- [ ] CRUD/read инвентаря
- [ ] Создание / отмена sell listing
- [ ] Каталог + страница предмета (API; UI можно черновой)

### DoD
- Пользователь A видит предмет и создаёт listing
- Отмена listing возвращает предмет в `available`
- Миграции накатываются чисто на пустой БД

### Out of scope
Покупка, матчинг, WebSocket.

---

## Этап 3 — Trading Core (главный хардкор)

**Цель:** атомарная покупка без double-sell.

### Deliverables
- [ ] `POST /market/listings/:id/buy` в одной транзакции
- [ ] `trades` + `ledger_entries`
- [ ] Корректные ошибки: нет денег / listing закрыт
- [ ] Интеграционный тест параллельных покупок (обязателен)
- [ ] История сделок API

### DoD
- 20 параллельных buy одного listing → **ровно 1** success
- Балансы и владелец предмета сходятся с ledger
- Тест гонки зелёный в CI

### Out of scope
Buy orders, частичное исполнение, realtime.

---

## Этап 4 — MVP UI & Polish

**Цель:** можно показать одногруппнику демо за 2 минуты.

### Deliverables
- [ ] UI: логин, инвентарь, каталог, listing, buy, история
- [ ] `Idempotency-Key` на buy
- [ ] Простой rate limit на buy
- [ ] README: скрин/гифка + «How to demo»
- [ ] CHANGELOG для MVP tag `v0.1.0`

### DoD
- Сквозной сценарий без Postman
- CI зелёный
- Тег `v0.1.0` в GitLab

### Out of scope
Идеальный дизайн, мобильное приложение, прод-мониторинг.

---

## Этап 5 — Order Book Lite (optional)

**Цель:** приблизиться к Steam Market.

### Deliverables
- [ ] Buy orders
- [ ] Matching: `buy.price >= sell.price`
- [ ] Held balance (escrow) на открытых buy orders
- [ ] Тесты матчинга и отмены

### DoD
- Новый sell может схлопнуться с существующим buy (и наоборот)
- Cancel buy → held возвращается

---

## Этап 6 — Realtime & Ops (optional)

### Deliverables
- [ ] WebSocket / SSE: лента последних сделок
- [ ] Staging deploy job в GitLab
- [ ] Базовые метрики/логи (хотя бы structured logging)
- [ ] Бэкап Postgres на staging (скрипт)

---

## Приоритизация (если мало времени)

1. Этап 3 (гонки + buy) — **must**  
2. Этап 4 (демо UI) — **must**  
3. Этап 5–6 — только если MVP стабилен  

Правило: **не начинаем следующий этап, пока DoD текущего не закрыт в MR**.

---

## Milestone mapping (GitLab)

| GitLab Milestone | Этапы |
|------------------|--------|
| `M0 Planning` | 0 |
| `M1 Foundation` | 1 |
| `M2 Market Listings` | 2 |
| `M3 Trading` | 3 |
| `M4 MVP` | 4 |
| `M5+ Extensions` | 5–6 |

Issues вешаем на milestone. В MR указываем `Closes #N`.

---

## Риски и митигация

| Риск | Митигация |
|------|-----------|
| Утонуть в идеальном order book | Сначала Buy Now (этап 3), book — этап 5 |
| Нет демо-вайба | Этап 4 обязателен, лента сделок |
| CI «потом» | Скелет CI с этапа 0, тесты с этапа 1 |
| Разъезд схемы у двоих | Общий ERD в `docs/domain.md` до кода |
| Спор про стек | Решение до конца этапа 0, дальше не пересматриваем |

---

## Changelog этапов

Ведём краткие итоги в [CHANGELOG.md](./CHANGELOG.md) при закрытии milestone.
