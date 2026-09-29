#!/usr/bin/env python3
"""Build a clean, scannable PDF for project topic evaluation."""

from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "project-topics-evaluation.pdf"
HTML_PATH = ROOT / "project-topics-evaluation.html"

CSS = r"""
@page {
  size: A4;
  margin: 14mm 12mm 16mm 12mm;
  @bottom-center {
    content: "Оценка проектов  ·  " counter(page);
    font-family: "Lato", "DejaVu Sans", sans-serif;
    font-size: 8.5pt;
    color: #94a3b8;
  }
}

:root {
  --ink: #0b1220;
  --muted: #5b6b7c;
  --line: #e6edf2;
  --soft: #f4f8f8;
  --teal: #0f766e;
  --teal-dark: #115e59;
  --teal-soft: #d9f3ef;
  --amber: #c2410c;
  --amber-soft: #ffedd5;
  --green: #166534;
  --green-soft: #dcfce7;
  --blue: #1e40af;
  --blue-soft: #dbeafe;
}

* { box-sizing: border-box; }
html { font-size: 10.25pt; }
body {
  margin: 0;
  font-family: "Lato", "DejaVu Sans", sans-serif;
  color: var(--ink);
  line-height: 1.42;
}

h1, h2, h3 {
  font-family: "DejaVu Serif", "Liberation Serif", serif;
  line-height: 1.2;
  page-break-after: avoid;
}

h1 { font-size: 1.55rem; margin: 0 0 0.35rem; }
h2 {
  font-size: 1.18rem;
  margin: 1.35rem 0 0.55rem;
  padding-bottom: 0.28rem;
  border-bottom: 2.5px solid var(--teal);
  color: var(--ink);
}
h3 {
  font-size: 1rem;
  margin: 0;
  color: var(--ink);
}

p { margin: 0.35rem 0; }
ul, ol { margin: 0.3rem 0 0.55rem; padding-left: 1.15rem; }
li { margin: 0.15rem 0; }
strong { font-weight: 700; }

.cover {
  background: linear-gradient(135deg, #0f766e 0%, #0f5f5a 55%, #123f3c 100%);
  color: #fff;
  border-radius: 16px;
  padding: 1.35rem 1.3rem 1.2rem;
  margin-bottom: 0.9rem;
}
.cover h1 { color: #fff; font-size: 1.65rem; }
.cover .sub { color: rgba(255,255,255,0.92); margin: 0.2rem 0; }
.pills { margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.35rem; }
.pill {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.22rem 0.58rem;
  border-radius: 999px;
  background: rgba(255,255,255,0.15);
  color: #fff;
}

.score-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.45rem;
  margin: 0.7rem 0 0.9rem;
}
.score-card {
  background: var(--soft);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.55rem 0.45rem 0.5rem;
  text-align: center;
  page-break-inside: avoid;
}
.score-card .num {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--teal);
  line-height: 1;
}
.score-card .name {
  margin-top: 0.28rem;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.score-card .hint {
  margin-top: 0.18rem;
  font-size: 0.78rem;
  color: var(--ink);
}

.callout {
  border-radius: 0 12px 12px 0;
  padding: 0.65rem 0.85rem;
  margin: 0.55rem 0 0.85rem;
  border-left: 4px solid var(--teal);
  background: var(--teal-soft);
  page-break-inside: avoid;
}
.callout.good { background: var(--green-soft); border-left-color: var(--green); }
.callout.warn { background: var(--amber-soft); border-left-color: var(--amber); }
.callout .title {
  font-weight: 800;
  margin-bottom: 0.25rem;
  font-size: 0.92rem;
}
.callout ul { margin-bottom: 0; }

.project {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 0.8rem 0.9rem 0.85rem;
  margin: 0.75rem 0;
  page-break-inside: avoid;
}
.project-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.6rem;
  margin-bottom: 0.35rem;
}
.badge {
  flex-shrink: 0;
  background: var(--ink);
  color: #fff;
  font-weight: 800;
  font-size: 0.8rem;
  border-radius: 8px;
  padding: 0.28rem 0.5rem;
}
.badge.top { background: var(--teal); }
.analogs {
  color: var(--muted);
  font-size: 0.86rem;
  margin: 0 0 0.45rem;
}
.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.35rem;
  margin: 0.45rem 0 0.55rem;
}
.metric {
  background: var(--soft);
  border-radius: 8px;
  padding: 0.35rem 0.4rem;
  text-align: center;
}
.metric b {
  display: block;
  color: var(--teal-dark);
  font-size: 0.95rem;
}
.metric span {
  display: block;
  color: var(--muted);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.55rem;
  margin-top: 0.35rem;
}
.box {
  background: var(--soft);
  border-radius: 10px;
  padding: 0.5rem 0.6rem;
}
.box .label {
  font-weight: 800;
  font-size: 0.8rem;
  margin-bottom: 0.2rem;
  color: var(--teal-dark);
}
.box.risk .label { color: var(--amber); }
.box ul { margin: 0; padding-left: 1rem; }
.box li { font-size: 0.86rem; }
.mvp {
  margin-top: 0.45rem;
  padding-top: 0.4rem;
  border-top: 1px dashed var(--line);
  font-size: 0.88rem;
}
.mvp b { color: var(--blue); }

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.45rem 0 0.8rem;
  font-size: 0.84rem;
}
th {
  background: var(--teal);
  color: #fff;
  text-align: left;
  padding: 0.4rem 0.45rem;
  font-weight: 700;
}
td {
  padding: 0.38rem 0.45rem;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
tr:nth-child(even) td { background: var(--soft); }

.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.45rem;
  margin: 0.5rem 0 0.8rem;
}
.mini {
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 0.5rem 0.55rem;
  page-break-inside: avoid;
  background: #fff;
}
.mini .kicker {
  font-size: 0.68rem;
  font-weight: 800;
  color: var(--teal);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.mini .name {
  font-weight: 800;
  margin: 0.12rem 0 0.18rem;
  font-size: 0.92rem;
}
.mini p {
  margin: 0;
  color: var(--muted);
  font-size: 0.82rem;
}

.lead {
  color: var(--muted);
  margin: -0.15rem 0 0.55rem;
  font-size: 0.92rem;
}

.tag {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.12rem 0.42rem;
  border-radius: 999px;
  background: var(--blue-soft);
  color: var(--blue);
  margin-right: 0.2rem;
}
.tag.green { background: var(--green-soft); color: var(--green); }
.tag.amber { background: var(--amber-soft); color: var(--amber); }

.decision {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 0.45rem;
}
.decision .mini { background: var(--soft); }

.footer {
  margin-top: 1rem;
  padding-top: 0.55rem;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.78rem;
}
"""

HTML_DOC = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<title>Оценка учебных проектов</title>
<style>{CSS}</style>
</head>
<body>

<section class="cover">
  <h1>Оценка учебных проектов</h1>
  <p class="sub">Для пары: опыт, знания и интерес делать вместе</p>
  <p class="sub">Шкала 1–10 · интерес · польза · глубина · сложность · демо · риск выгорания</p>
  <div class="pills">
    <span class="pill">4 основные темы</span>
    <span class="pill">альтернативы</span>
    <span class="pill">как выбрать</span>
  </div>
</section>

<div class="score-row">
  <div class="score-card"><div class="num">8.5</div><div class="name">#1 Маркет</div><div class="hint">топ для собесов</div></div>
  <div class="score-card"><div class="num">6.7</div><div class="name">#2 SaaS</div><div class="hint">как на работе</div></div>
  <div class="score-card"><div class="num">7.0</div><div class="name">#3 Квизы</div><div class="hint">быстрое демо</div></div>
  <div class="score-card"><div class="num">8.5</div><div class="name">#4 Кейсы</div><div class="hint">вайб + хардкор</div></div>
</div>

<div class="callout good">
  <div class="title">Короткий вердикт</div>
  <ul>
    <li><strong>Собес / backend</strong> → #1 Маркетплейс</li>
    <li><strong>Кайф и демо</strong> → #4 Кейсы или #3 Квизы</li>
    <li><strong>Похоже на работу</strong> → #2 SaaS</li>
    <li><strong>Баланс</strong> → #4 (или #1, если гемблинг-ассоциации не хотите)</li>
  </ul>
</div>

<h2>1. Основные темы</h2>
<p class="lead">Четыре ваши идеи — с оценками, плюсами, рисками и MVP.</p>

<article class="project">
  <div class="project-head">
    <div>
      <h3>1) Игровой маркетплейс / P2P</h3>
      <p class="analogs">Steam Market · Buff · CS.Money (упрощённо)</p>
    </div>
    <div class="badge top">8.5</div>
  </div>
  <div class="metrics">
    <div class="metric"><b>8</b><span>интерес</span></div>
    <div class="metric"><b>10</b><span>опыт</span></div>
    <div class="metric"><b>10</b><span>глубина</span></div>
    <div class="metric"><b>9</b><span>сложность</span></div>
    <div class="metric"><b>7</b><span>демо</span></div>
    <div class="metric"><b>7</b><span>риск</span></div>
  </div>
  <p><span class="tag green">лучший для backend</span><span class="tag">order book</span><span class="tag">escrow</span></p>
  <div class="two-col">
    <div class="box">
      <div class="label">Плюсы</div>
      <ul>
        <li>Топовая тема для собесов</li>
        <li>Гонки, транзакции, изоляции</li>
        <li>Легко объяснить сложность</li>
      </ul>
    </div>
    <div class="box risk">
      <div class="label">Риски</div>
      <ul>
        <li>Демо скучнее кейсов/квизов</li>
        <li>Легко утонуть в order book</li>
        <li>Только виртуальные предметы</li>
      </ul>
    </div>
  </div>
  <div class="mvp"><b>MVP:</b> баланс + инвентарь → buy/sell orders → атомарный match → тест на гонку</div>
  <p><strong>Кому:</strong> серьёзный backend и сильная строка в резюме.</p>
</article>

<article class="project">
  <div class="project-head">
    <div>
      <h3>2) SaaS бронирование / CRM услуг</h3>
      <p class="analogs">YCLIENTS · Dikidi · Calendly · развитие YPlaces</p>
    </div>
    <div class="badge">6.7</div>
  </div>
  <div class="metrics">
    <div class="metric"><b>6</b><span>интерес</span></div>
    <div class="metric"><b>9</b><span>опыт</span></div>
    <div class="metric"><b>8</b><span>глубина</span></div>
    <div class="metric"><b>7</b><span>сложность</span></div>
    <div class="metric"><b>5</b><span>демо</span></div>
    <div class="metric"><b>5</b><span>риск</span></div>
  </div>
  <p><span class="tag">multi-tenant</span><span class="tag">слоты</span><span class="tag amber">слабый вайб</span></p>
  <div class="two-col">
    <div class="box">
      <div class="label">Плюсы</div>
      <ul>
        <li>Максимально «как работа»</li>
        <li>Можно внедрить знакомым</li>
        <li>Хорошо делится на двоих</li>
      </ul>
    </div>
    <div class="box risk">
      <div class="label">Риски</div>
      <ul>
        <li>Мало «вау»</li>
        <li>Календарный UI — боль</li>
        <li>Расползается в большую CRM</li>
      </ul>
    </div>
  </div>
  <div class="mvp"><b>MVP:</b> 1 тенант → мастера/услуги/график → бронь без double-book → напоминание</div>
  <p><strong>Кому:</strong> fullstack/product опыт без игрового вайба.</p>
</article>

<article class="project">
  <div class="project-head">
    <div>
      <h3>3) Real-time квизы (Kahoot / Квизли)</h3>
      <p class="analogs">Kahoot · Quizizz · вечеринки / стримы / учёба</p>
    </div>
    <div class="badge">7.0</div>
  </div>
  <div class="metrics">
    <div class="metric"><b>9</b><span>интерес</span></div>
    <div class="metric"><b>7</b><span>опыт</span></div>
    <div class="metric"><b>7</b><span>глубина</span></div>
    <div class="metric"><b>6</b><span>сложность</span></div>
    <div class="metric"><b>10</b><span>демо</span></div>
    <div class="metric"><b>3</b><span>риск</span></div>
  </div>
  <p><span class="tag green">быстрый результат</span><span class="tag">WebSocket</span><span class="tag">wow-демо</span></p>
  <div class="two-col">
    <div class="box">
      <div class="label">Плюсы</div>
      <ul>
        <li>Быстро до «можно играть»</li>
        <li>Идеально делится: UI / сокеты</li>
        <li>Без юридической серости</li>
      </ul>
    </div>
    <div class="box risk">
      <div class="label">Риски</div>
      <ul>
        <li>Слабее на «финтех»-собесах</li>
        <li>Можно остаться игрушкой</li>
        <li>Нужна эмуляция нагрузки</li>
      </ul>
    </div>
  </div>
  <div class="mvp"><b>MVP:</b> создание квиза → комната по коду → раунд + таймер → лидерборд на TV</div>
  <p><strong>Кому:</strong> скорость, веселье, realtime.</p>
</article>

<article class="project">
  <div class="project-head">
    <div>
      <h3>4) Кейсы + инвентарь + валюта</h3>
      <p class="analogs">Кейс-сайты · виртуальная экономика · live drops</p>
    </div>
    <div class="badge top">8.5</div>
  </div>
  <div class="metrics">
    <div class="metric"><b>10</b><span>интерес</span></div>
    <div class="metric"><b>8</b><span>опыт</span></div>
    <div class="metric"><b>9</b><span>глубина</span></div>
    <div class="metric"><b>8</b><span>сложность</span></div>
    <div class="metric"><b>10</b><span>демо</span></div>
    <div class="metric"><b>6</b><span>риск</span></div>
  </div>
  <p><span class="tag green">топ вайб</span><span class="tag">экономика</span><span class="tag amber">осторожно в резюме</span></p>
  <div class="two-col">
    <div class="box">
      <div class="label">Плюсы</div>
      <ul>
        <li>Максимальная мотивация</li>
        <li>Красивое вирусное демо</li>
        <li>Почти тот же хардкор, что #1</li>
      </ul>
    </div>
    <div class="box risk">
      <div class="label">Риски</div>
      <ul>
        <li>Ассоциация с гемблингом</li>
        <li>Увлечься анимациями</li>
        <li>Без реальных денег</li>
      </ul>
    </div>
  </div>
  <div class="mvp"><b>MVP:</b> вирт. баланс → 2–3 кейса → открытие + инвентарь → live-лента дропов</div>
  <p><strong>Кому:</strong> драйв + жёсткая экономика. В резюме: <em>virtual item economy / educational lootbox</em>.</p>
</article>

<h2>2. Что прокачиваете</h2>
<table>
  <thead>
    <tr><th>Навык</th><th>#1</th><th>#2</th><th>#3</th><th>#4</th></tr>
  </thead>
  <tbody>
    <tr><td>Транзакции / consistency</td><td>★★★★★</td><td>★★★★</td><td>★★</td><td>★★★★★</td></tr>
    <tr><td>Race conditions</td><td>★★★★★</td><td>★★★★★</td><td>★★★</td><td>★★★★</td></tr>
    <tr><td>WebSockets / realtime</td><td>★★</td><td>★★</td><td>★★★★★</td><td>★★★★</td></tr>
    <tr><td>Доменная логика</td><td>★★★★</td><td>★★★★★</td><td>★★★</td><td>★★★★</td></tr>
    <tr><td>Frontend / анимации</td><td>★★★</td><td>★★★★</td><td>★★★★★</td><td>★★★★★</td></tr>
    <tr><td>Сила на backend-собесе</td><td>★★★★★</td><td>★★★★</td><td>★★★</td><td>★★★★</td></tr>
    <tr><td>Скорость до демо</td><td>★★</td><td>★★★</td><td>★★★★★</td><td>★★★★</td></tr>
  </tbody>
</table>

<div class="callout">
  <div class="title">Практичный путь на семестр</div>
  <p>Старт с <strong>#4</strong> (баланс, инвентарь, кейсы, live) → позже P2P-торговля предметами из <strong>#1</strong>. Не запускайте #2 и #3 параллельно.</p>
</div>

<h2>3. Альтернативы (если свои 4 не зашли)</h2>
<p class="lead">Сильные идеи сверх списка — коротко и по делу.</p>

<div class="grid2">
  <div class="mini"><div class="kicker">A · опыт 10</div><div class="name">Мини-банк / кошелёк</div><p>Переводы, hold/capture, ledger. Тот же хардкор без гемблинга.</p></div>
  <div class="mini"><div class="kicker">B · баланс</div><div class="name">Билеты на события</div><p>Race на места + QR. Веселее CRM, полезно как #2.</p></div>
  <div class="mini"><div class="kicker">C · realtime</div><div class="name">Discord / Slack lite</div><p>Комнаты, presence, роли. Быстро «оживает».</p></div>
  <div class="mini"><div class="kicker">D · wow</div><div class="name">Miro / доска</div><p>Синхрон объектов и курсоров. Сильное демо.</p></div>
  <div class="mini"><div class="kicker">I · домен</div><div class="name">Splitwise</div><p>Балансы группы и долги. Чисто и полезно.</p></div>
  <div class="mini"><div class="kicker">N · продукт</div><div class="name">Заказы в ресторане</div><p>QR стола → кухня-экран → статусы realtime.</p></div>
  <div class="mini"><div class="kicker">S · быстро</div><div class="name">Q&amp;A-стена (Slido)</div><p>Проще квизов, тот же эффект на зале.</p></div>
  <div class="mini"><div class="kicker">U · platform</div><div class="name">Feature flags</div><p>Rollout %, audit. Ценится на backend-собесах.</p></div>
  <div class="mini"><div class="kicker">AA · AI с мясом</div><div class="name">RAG по PDF</div><p>Чанки, эмбеддинги, ответ + цитата источника.</p></div>
  <div class="mini"><div class="kicker">бонус</div><div class="name">Аукцион realtime</div><p>Ставки + таймер = кусок биржи, но веселее.</p></div>
</div>

<div class="callout warn">
  <div class="title">Лучше не брать как основной</div>
  <ul>
    <li>Todo / блог / «магазин футболок» без сложной логики</li>
    <li>Весь Instagram сразу · микросервисы ради микросервисов</li>
    <li>Голая LLM-обёртка без пайплайна и своей доменки</li>
    <li>Реальные платежи, чужие аккаунты, гемблинг на деньги</li>
  </ul>
</div>

<h2>4. Как выбрать вдвоём</h2>
<div class="decision">
  <div class="mini">
    <div class="name">3 вопроса</div>
    <ol>
      <li>Важнее вайб или строка в резюме?</li>
      <li>Больше frontend/realtime или backend/данные?</li>
      <li>Нужен результат за месяц или ок 2+ месяца?</li>
    </ol>
  </div>
  <div class="mini">
    <div class="name">Шорт-лист</div>
    <ol>
      <li><strong>#4 Кейсы</strong> — драйв</li>
      <li><strong>Мини-банк</strong> — резюме</li>
      <li><strong>Билеты / ресторан</strong> — компромисс</li>
      <li><strong>Квизы / чат / доска</strong> — realtime</li>
    </ol>
  </div>
</div>

<div class="callout good">
  <div class="title">Итоговая рекомендация</div>
  <p>Под «опыт и знания + чтобы было интересно» — берите <strong>#4</strong>, с прицелом добавить торговлю из <strong>#1</strong>. Если гемблинг-вайб мешает портфолио — <strong>мини-банк</strong> или <strong>#1 на виртуальных предметах</strong>.</p>
  <p><strong>Роли:</strong> один — core backend и тесты · второй — frontend/realtime/админка · вместе в первую неделю — схема БД и API.</p>
</div>

<p class="footer">Полная текстовая версия со всеми деталями — в project-topics-evaluation.md. Оценки субъективные.</p>

</body>
</html>
"""


def main() -> None:
    HTML_PATH.write_text(HTML_DOC, encoding="utf-8")
    HTML(string=HTML_DOC, base_url=str(ROOT)).write_pdf(PDF_PATH)
    print(f"OK {PDF_PATH} ({PDF_PATH.stat().st_size} bytes), pages roughly check via file")


if __name__ == "__main__":
    main()
