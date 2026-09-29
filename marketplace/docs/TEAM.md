# Команда и задачи

Два участника. Задачи берём в GitLab Issues → Assignee = себя.  
Доска: **Plan → Issue boards** (колонки по статусу).

---

## Роли

| | **Участник A — Backend** | **Участник B — Fullstack / UI** |
|--|--------------------------|--------------------------------|
| Фокус | БД, API, транзакции, тесты, CI | UI, UX покупки/листинга, DX |
| Стек | FastAPI, PostgreSQL, Alembic, pytest | React/TS, API-клиент |
| Не лезет без согл. | в вёрстку «на вкус» | в схему сделок / wallet без ревью A |

В первую неделю **вместе**: схема БД + OpenAPI-контракт (issue `T0-shared`).

Подставьте имена:

| Роль | Имя / GitLab username |
|------|------------------------|
| A — Backend | _(например mkuemzhi)_ |
| B — Fullstack/UI | _(друг)_ |

---

## Как брать задачу

1. Открой [Issues](https://gitlab.com/myvibe-group/marketplacep2p/-/issues)
2. Выбери issue с лейблом своего этапа / роли
3. **Assign to me**
4. Статус: `Todo` → `Doing` (лейбл или колонка борда)
5. Ветка: `feature/<issue-iid>-short-name`
6. MR → `Closes #<iid>` → ревью у второго → merge

**Правило:** одна задача = один assignee. Не берём две крупные сразу.

---

## Лейблы (завести в GitLab)

| Label | Цвет (примерно) | Смысл |
|-------|-----------------|--------|
| `role::backend` | синий | задача A |
| `role::frontend` | фиолетовый | задача B |
| `role::shared` | серый | оба / вместе |
| `stage::0` … `stage::4` | зелёный | этап roadmap |
| `size::S` / `M` / `L` | оранжевый | оценка |
| `status::todo` | светлый | в бэклоге |
| `status::doing` | жёлтый | в работе |
| `status::blocked` | красный | ждёт другого |
| `status::done` | зелёный | закрыто |

---

## Доска (Issue Board)

Колонки:
1. **Open** (без status::doing)
2. **Doing** — label `status::doing`
3. **Blocked** — label `status::blocked`
4. **Closed**

Фильтры борда: можно сделать два борда — «Backend» (`role::backend`) и «Frontend» (`role::frontend`).

---

## Стартовый бэклог (этап 0–1)

Создайте issues вручную (или скриптом ниже) с этими заголовками.

### Shared

| ID | Title | Labels | Assignee |
|----|-------|--------|----------|
| T0-1 | Зафиксировать имена ролей A/B в TEAM.md | `role::shared` `stage::0` `size::S` | оба (коротко) |
| T0-2 | Protect `main` + правила MR | `role::shared` `stage::0` `size::S` | A |
| T0-3 | Согласовать ERD users/items/inventory/wallet | `role::shared` `stage::1` `size::M` | оба |
| T0-4 | Черновик OpenAPI auth + health | `role::shared` `stage::1` `size::M` | оба |

### Backend (A)

| ID | Title | Labels | Size |
|----|-------|--------|------|
| T1-A1 | Skeleton FastAPI: health, settings, logging | `role::backend` `stage::1` | M |
| T1-A2 | Docker Compose: api + postgres | `role::backend` `stage::1` | M |
| T1-A3 | Alembic + миграция users | `role::backend` `stage::1` | M |
| T1-A4 | JWT register/login/me | `role::backend` `stage::1` | L |
| T1-A5 | CI: pytest job когда появится requirements.txt | `role::backend` `stage::1` | S |
| T2-A1 | Модели items, inventories, wallets + seed | `role::backend` `stage::2` | L |
| T2-A2 | API инвентаря и создания listing | `role::backend` `stage::2` | L |
| T3-A1 | Buy Now в одной транзакции + ledger | `role::backend` `stage::3` | L |
| T3-A2 | Интеграционный тест параллельных покупок | `role::backend` `stage::3` | M |

### Frontend (B)

| ID | Title | Labels | Size |
|----|-------|--------|------|
| T1-B1 | Scaffold React/TS + роутинг | `role::frontend` `stage::1` | M |
| T1-B2 | Страницы Login / Register → JWT в storage | `role::frontend` `stage::1` | M |
| T1-B3 | Каркас layout + API client (fetch/axios) | `role::frontend` `stage::1` | M |
| T2-B1 | Каталог предметов (список из API) | `role::frontend` `stage::2` | M |
| T2-B2 | Инвентарь пользователя | `role::frontend` `stage::2` | M |
| T2-B3 | Создать / отменить listing (форма) | `role::frontend` `stage::2` | M |
| T3-B1 | Кнопка Buy + состояния loading/error | `role::frontend` `stage::3` | M |
| T3-B2 | История сделок | `role::frontend` `stage::3` | S |
| T4-B1 | Демо-гифка / README How to demo | `role::frontend` `stage::4` | S |

---

## Кто чем занят сейчас (обновляйте)

| Участник | Сейчас Doing | Next |
|----------|--------------|------|
| A | _пока пусто_ | T0-2, T1-A1 |
| B | _пока пусто_ | T1-B1, ждать T0-3 вместе |

---

## Зависимости (чтобы не блокировать друг друга)

```text
T0-3 (ERD вместе)
   ├─► T1-A1…A4 (backend foundation)
   │      └─► T2-A* → T3-A*
   └─► T1-B1…B3 (frontend scaffold на моках/OpenAPI)
          └─► T2-B* нужен живой API из T2-A
```

B может начинать UI на **моках** параллельно с A (этап 1), не дожидаясь buy.

---

См. также: [ROADMAP.md](./ROADMAP.md), [CONTRIBUTING.md](./CONTRIBUTING.md).
