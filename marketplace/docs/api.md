# API draft

Base URL: `/api/v1`  
Auth: `Authorization: Bearer <jwt>`  
Идемпотентные мутации buy: заголовок `Idempotency-Key: <uuid>`

## Auth

| Method | Path | Desc |
|--------|------|------|
| POST | `/auth/register` | email + password → tokens |
| POST | `/auth/login` | email + password → tokens |
| GET | `/auth/me` | текущий пользователь |

## Wallet & inventory

| Method | Path | Desc |
|--------|------|------|
| GET | `/me/wallet` | balance, held |
| GET | `/me/inventory` | список экземпляров |
| GET | `/me/trades` | история сделок пользователя |

## Catalog & market

| Method | Path | Desc |
|--------|------|------|
| GET | `/catalog/items` | справочник |
| GET | `/catalog/items/{id}` | карточка |
| GET | `/market/listings` | `?item_id=&status=open` |
| POST | `/market/listings` | создать sell listing |
| DELETE | `/market/listings/{id}` | отмена |
| POST | `/market/listings/{id}/buy` | Buy Now |
| GET | `/market/trades` | публичная лента (позже) |

## Примеры

### Create listing

```http
POST /api/v1/market/listings
Authorization: Bearer …
Content-Type: application/json

{
  "inventory_id": "…",
  "price": 100
}
```

### Buy Now

```http
POST /api/v1/market/listings/{id}/buy
Authorization: Bearer …
Idempotency-Key: 7b1c0f6e-…
```

### Ошибки (ориентир)

| Code | Когда |
|------|--------|
| 400 | валидация |
| 401 | нет/битый токен |
| 402/400 | недостаточно средств |
| 404 | listing не найден |
| 409 | listing уже filled/cancelled / конфликт идемпотентности |

Точные коды зафиксируем в OpenAPI на этапе 1–3.

## Этап 5 (позже)

- `POST /market/buy-orders`
- `DELETE /market/buy-orders/{id}`
- matching internals — не отдельный публичный endpoint
