# Domain model

## Язык предметной области

| Термин | Смысл |
|--------|--------|
| Item | Тип предмета из каталога (не экземпляр) |
| Inventory item | Конкретный экземпляр у пользователя |
| Listing | Выставленный на продажу экземпляр по цене |
| Buy Now | Мгновенная покупка listing |
| Trade | Факт состоявшейся сделки |
| Wallet | Баланс виртуальной валюты |
| Ledger entry | Запись движения денег |
| Hold | Заморозка средств под buy order (этап 5) |

## Сущности

### User
- id, email, password_hash, created_at

### Item (catalog)
- id, slug, name, rarity, image_url

### InventoryItem
- id, user_id, item_id
- status: `available` | `listed` | `locked`
- Инвариант: `listed` ↔ существует open listing на этот inventory_id

### Wallet
- user_id
- balance (доступно)
- held_balance (этап 5; в MVP можно = 0)

### Listing
- id, seller_id, inventory_id, item_id, price
- status: `open` | `filled` | `cancelled`
- Инвариант: один open listing на inventory_id

### Trade
- id, listing_id, buyer_id, seller_id, item_id, inventory_id, price, created_at

### LedgerEntry
- id, user_id, trade_id nullable, amount (+/-), kind, created_at
- kind: `seed` | `hold` | `release` | `purchase` | `sale` | …

## Инварианты (критично)

1. Предмет не может иметь двух владельцев.
2. Open listing нельзя купить дважды.
3. Сумма изменений ledger по пользователю = текущий balance (+ held).
4. Trade создаётся только вместе с переводами в одной транзакции.
5. Повтор с тем же Idempotency-Key не создаёт второй trade.

## Сценарии приёмки

### Успешная покупка
Given open listing price=100 and buyer balance>=100  
When buyer buys  
Then listing=filled, buyer owns item, balances updated, trade exists

### Double buy
Given one open listing  
When two buyers buy in parallel  
Then exactly one success, one error, one owner

### Cancel
Given open listing  
When seller cancels  
Then inventory=available, buy returns error

### Insufficient funds
Given buyer balance < price  
When buy  
Then listing stays open, balances unchanged

## Что сознательно упрощено в MVP

- Нет buy order book
- Нет комиссий маркета
- Нет частичных исполнений
- Один рынок / одна валюта
- Нет редкости-влияния на цены (только отображение)
