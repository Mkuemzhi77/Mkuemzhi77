# Architecture

Модульный **монолит**. Микросервисы не используем до стабильного MVP.

## Контекст

```text
[ Web UI (React) ] ----HTTP/JSON----> [ FastAPI ]
                                         |
                                         +--> Auth
                                         +--> Catalog
                                         +--> Inventory
                                         +--> Wallet / Ledger
                                         +--> Trading Engine
                                         |
                                      PostgreSQL
                                    (Redis optional)
```

## Модули

| Модуль | Ответственность | Граница |
|--------|-----------------|---------|
| Auth | register/login, JWT, текущий пользователь | не знает про сделки |
| Catalog | справочник предметов | не хранит владельцев |
| Inventory | экземпляры предметов у пользователя | статусы available/listed |
| Wallet | balance + held | изменяется только через ledger-операции |
| Trading | listings, buy, статусы ордеров | оркестрирует inventory+wallet в транзакции |
| Ledger | append-only журнал денег | источник правды для аудита |

## Поток Buy Now (MVP)

```text
UI buy click
   -> API POST /market/listings/{id}/buy
      -> BEGIN
         lock listing FOR UPDATE
         lock buyer wallet FOR UPDATE
         validate open + balance
         transfer money
         transfer inventory ownership
         close listing
         write trade + ledger
      -> COMMIT
   -> 200 trade
```

Параллельный второй buy ждёт лок / видит closed listing → ошибка.

## Технические решения

| Тема | Решение v1 | Почему |
|------|------------|--------|
| Консистентность | Postgres транзакции + `SELECT FOR UPDATE` | просто и надёжно для учёбы |
| Идемпотентность | заголовок `Idempotency-Key` | защита от double-click / retry |
| Кэш | не обязателен | сначала корректность |
| Очереди | нет | синхронный buy для MVP |
| Realtime | этап 6 | после MVP |

## Деплой (целевой, как LATAN)

```text
GitLab CI
  lint → test → build image → deploy staging (manual)
```

Staging: один compose/VPS, Postgres volume, env через GitLab CI variables.

## Анти-цели архитектуры

- Не дробим trading на отдельные сервисы «для резюме»
- Не тащим Kafka/Temporal в v1
- Не делаем event sourcing ради event sourcing
