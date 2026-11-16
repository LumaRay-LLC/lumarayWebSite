import re, os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def version(rel):
    """Short content hash, appended as ?v= so browsers drop a cached old copy."""
    return hashlib.sha1(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:8]

CSS_V = version("style.css")
JS_V = version("assets/site.js")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">')

def L(en, pt, tag="span"):
    return f'<{tag} data-lang-block="en">{en}</{tag}><{tag} data-lang-block="pt" lang="pt-BR">{pt}</{tag}>'

APPS = [
    ("next-chapter", "Next Chapter", "next-chapter.png", "theme-nextchapter"),
    ("wetab", "WeTab", "wetab.png", "theme-wetab"),
    ("pantry-stock", "Pantry Stock", "pantry-stock.png", "theme-pantry"),
]

def head(r, title, desc, cls=""):
    c = f' class="{cls}"' if cls and cls != "home" else ""
    fonts = FONTS
    if cls in ("theme-nextchapter", "home"):
        fonts = FONTS.replace("family=Montserrat", "family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700&family=Montserrat")
    return f'''<!doctype html>
<html lang="en"{c}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{r}assets/favicon.png" type="image/png">
{fonts}
<link rel="stylesheet" href="{r}style.css?v={CSS_V}">
</head>
<body>
'''

def header(r, current):
    home_href = r or './'
    hc = ' aria-current="page"' if current == "home" else ""
    tabs = [f'<a href="{home_href}"{hc}>{L("Home", "Início")}</a>']
    for slug, name, icon, _ in APPS:
        cur = ' aria-current="page"' if current == slug else ""
        tabs.append(f'<a href="{r}{slug}/"{cur}><img src="{r}assets/{icon}" alt="">{name}</a>')
    cur = ' aria-current="page"' if current == "privacy" else ""
    tabs.append(f'<a href="{r}privacy/"{cur}>{L("Privacy", "Privacidade")}</a>')
    tabs_html = "\n    ".join(tabs)
    return f'''<header class="site-header">
  <div class="bar">
    <a class="logo-link" href="{home_href}"><img src="{r}assets/logo-tile.jpg" alt="LumaRay Software logo"><div><span>LUMARAY</span><small>SOFTWARE</small></div></a>
    <div class="lang-switch" role="group" aria-label="Language">
      <button type="button" data-set-lang="en" aria-pressed="true">EN</button>
      <button type="button" data-set-lang="pt" aria-pressed="false">PT</button>
    </div>
  </div>
  <nav class="tabs" aria-label="Site">
    {tabs_html}
  </nav>
</header>
'''

def footer(r):
    return f'''<footer class="site-footer">
  © 2026 LumaRay Software LLC · <a href="{r}privacy/">{L("Privacy", "Privacidade")}</a> · <a href="mailto:lumaraysoftware@gmail.com">lumaraysoftware@gmail.com</a>
</footer>
<script src="{r}assets/site.js?v={JS_V}"></script>
</body>
</html>
'''

def subtabs(r, slug, current):
    ov = ' aria-current="page"' if current == "overview" else ""
    pv = ' aria-current="page"' if current == "privacy" else ""
    base = "./" if current == "overview" else "../"
    return f'''<nav class="subtabs" aria-label="Product">
    <a href="{base}"{ov}>{L("Overview", "Visão geral")}</a>
    <a href="{base}privacy/"{pv}>{L("Privacy Policy", "Política de Privacidade")}</a>
    <a href="mailto:lumaraysoftware@gmail.com?subject={slug}%20support">{L("Support", "Suporte")}</a>
  </nav>
'''

def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(s)

def LI(en_src, pt_src, alt_en, alt_pt, cls="", lazy=True):
    """The same picture in each language; site.js shows the one that matches."""
    lz = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls and cls != "home" else ""
    if en_src == pt_src:
        return f'<img{c} src="{en_src}" alt="{alt_en}"{lz}>'
    return (f'<img{c} src="{en_src}" alt="{alt_en}" data-lang-block="en"{lz}>'
            f'<img{c} src="{pt_src}" alt="{alt_pt}" data-lang-block="pt" lang="pt-BR"{lz}>')

STORE = {
    "wetab": "https://apps.apple.com/app/id6806273923",
    "pantry-stock": "https://apps.apple.com/app/id6790430461",
}

# Art for each app, taken from its App Store assets. "frame" screens are raw
# captures shown inside a drawn phone; "card" screens already carry their
# own device and caption.
SHOW = {
    "next-chapter": dict(
        banner=("shots/next-chapter/banner-en.jpg", "shots/next-chapter/banner-pt.jpg"),
        style="frame",
        shots=[
            ("library", "library", ("Your library and current read", "Sua biblioteca e a leitura da vez")),
            ("foryou", "foryou", ("Picks by genre", "Sugestões por gênero")),
            ("club", "club", ("Book clubs with challenges", "Clubes do livro com desafios")),
            ("bookdetail2", "bookdetail2", ("Add a book in a tap", "Adicione um livro num toque")),
            ("profile", "profile", ("Your yearly reading quest", "Sua meta de leitura do ano")),
        ],
    ),
    "wetab": dict(
        banner=("shots/wetab/banner-en.jpg", "shots/wetab/banner-pt.jpg"),
        style="frame",
        shots=[(f"{n}-en", f"{n}-pt", c) for n, c in [
            ("01-inicio", ("Who owes you, at a glance", "Quem te deve, num relance")),
            ("03-itens", ("Items read from the receipt", "Itens lidos do recibo")),
            ("04-quem-consumiu", ("Tap who had what", "Toque em quem consumiu o quê")),
            ("06-cobranca-criada", ("Charges ready to send", "Cobranças prontas para enviar")),
            ("09-acertar-contas", ("Settle up in a few transfers", "Acerte em poucas transferências")),
            ("10-busca", ("Search bills and people", "Busque contas e pessoas")),
        ]],
    ),
    "pantry-stock": dict(
        banner=None,
        style="card",
        shots=[(f"{n}-en", f"{n}-pt", c) for n, c in [
            ("01-pantry", ("Your pantry", "Sua despensa")),
            ("04-expiry", ("Expiry dates", "Validade")),
            ("07-spending", ("Monthly spending", "Gasto do mês")),
            ("03-shopping", ("Shopping list", "Lista de compras")),
            ("05-maintenance", ("Home care", "Manutenção da casa")),
            ("09-aisles", ("Aisle order", "Ordem dos corredores")),
        ]],
    ),
}

def shot_src(r, slug, name):
    return f"{r}assets/shots/{slug}/{name}.jpg"

def art(r, slug, name, lazy=False):
    """The big picture for an app: its store banner, or three framed screens."""
    sh = SHOW[slug]
    if sh["banner"]:
        en, pt = sh["banner"]
        return f'<div class="art-banner">{LI(r + "assets/" + en, r + "assets/" + pt, f"{name} on the App Store", f"{name} na App Store", lazy=lazy)}</div>'
    trio = "".join(f'<div class="art-card">{LI(shot_src(r, slug, en), shot_src(r, slug, pt), cap[0], cap[1], lazy=lazy)}</div>'
                   for en, pt, cap in sh["shots"][:3])
    return f'<div class="art-trio">{trio}</div>'

STORE_LABEL = ("Download on the App Store", "Baixar na App Store")
APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.6c0-2.4 2-3.6 2.1-3.7-1.2-1.7-3-1.9-3.6-2-1.5-.2-3 .9-3.8.9-.8 0-2-.9-3.3-.9-1.7 0-3.3 1-4.2 2.5-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8s2 .8 3.3.8c1.4 0 2.3-1.2 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9 0 0-2.8-1.1-2.8-4.2zM14 5.3c.7-.8 1.2-2 1-3.1-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.9-1 3 1.1.1 2.2-.6 2.9-1.4z"/></svg>'

def store_btn(slug):
    if slug not in STORE:
        return ""
    return f'<a class="store-btn" href="{STORE[slug]}">{APPLE}{L(*STORE_LABEL)}</a>'

HOME_BLURB = {
    "next-chapter": ("Your reading quest log: track books, set yearly goals and run book clubs with friends.", "Seu diário de leitura: acompanhe livros, defina metas anuais e organize clubes do livro com amigos."),
    "wetab": ("Scan the receipt, tap who had what, and charge everyone their share with Pix.", "Leia o recibo, marque quem consumiu o quê e cobre a parte de cada um com Pix."),
    "pantry-stock": ("Keep track of what's at home with − and +, and get a shopping list when things run low.", "Controle o que tem em casa com − e +, e ganhe uma lista de compras quando algo estiver acabando."),
}
APP_ROWS = "\n".join(
    f'''      <article class="app-row {cls}">
        <div class="app-row-copy">
          <img class="app-icon" src="assets/{icon}" alt="">
          <h3>{name}</h3>
          <p>{L(*HOME_BLURB[slug])}</p>
          <div class="row-actions"><a class="go" href="{slug}/">{L("See the app →", "Conheça o app →")}</a>{store_btn(slug)}</div>
        </div>
        <a class="app-row-art" href="{slug}/" tabindex="-1" aria-hidden="true">{art("", slug, name, lazy=True)}</a>
      </article>''' for slug, name, icon, cls in APPS)

# ---------------------------------------------------------------- home
home = head("", "LumaRay Software", "LumaRay Software LLC is an independent studio making focused, private iPhone apps: Next Chapter, WeTab and Pantry Stock.", "home")
home += header("", "home")
home += f'''<section class="hero-ocean">
  <img class="logo" src="assets/logo-tile.jpg" alt="LumaRay Software logo">
  <h1>{L("Small apps, made with care, that keep your data yours.", "Apps simples, feitos com cuidado, que deixam seus dados com você.")}</h1>
  <p>{L("LumaRay Software is an independent studio building focused iPhone apps for everyday life.", "A LumaRay Software é um estúdio independente que cria apps para iPhone focados no dia a dia.")}</p>
  <div class="cta">
    <a class="btn primary" href="#apps">{L("See our apps", "Conheça os apps")}</a>
    <a class="btn ghost" href="#contact">{L("Contact us", "Fale conosco")}</a>
  </div>
  <svg class="waves" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
    <path class="w1" d="M0 38 C240 8 480 8 720 34 C960 60 1200 62 1440 30 L1440 90 L0 90 Z"/>
    <path class="w2" d="M0 56 C260 30 520 34 760 54 C1000 74 1220 70 1440 48 L1440 90 L0 90 Z"/>
    <path class="w3" d="M0 72 C240 54 500 56 740 70 C980 84 1220 82 1440 66 L1440 90 L0 90 Z"/>
  </svg>
</section>

<main class="page wide">
  <section id="about">
    <p class="section-label">{L("About", "Sobre")}</p>
    <h2 class="section-title">{L("An independent iOS studio", "Um estúdio independente de iOS")}</h2>
    <p class="lead" data-lang-block="en">LumaRay Software LLC designs and builds native iPhone apps in Swift and SwiftUI. We pick small, everyday problems (what to read next, who owes what after dinner, what's running out at home) and solve each one with a simple, polished app.</p>
    <p class="lead" data-lang-block="pt" lang="pt-BR">A LumaRay Software LLC projeta e desenvolve apps nativos para iPhone em Swift e SwiftUI. Escolhemos problemas pequenos do dia a dia (o que ler em seguida, quem deve quanto depois do jantar, o que está acabando em casa) e resolvemos cada um com um app simples e bem acabado.</p>
    <p class="lead" data-lang-block="en">Like a whale that surfaces only when it needs to, our apps stay out of your way: no accounts to create, no servers collecting your life, just tools that work.</p>
    <p class="lead" data-lang-block="pt" lang="pt-BR">Como a baleia que só sobe à superfície quando precisa, nossos apps não ficam no seu caminho: sem cadastro obrigatório, sem servidores coletando a sua vida, só ferramentas que funcionam.</p>
  </section>

  <section>
    <p class="section-label">{L("How we work", "Como trabalhamos")}</p>
    <div class="grid four">
      <div class="card"><span class="num">01</span><h3>{L("Your data, your iCloud", "Seus dados, seu iCloud")}</h3><p>{L("We don't run servers that store your data. It lives on your device and in your own private iCloud.", "Não mantemos servidores com os seus dados. Eles ficam no seu aparelho e no seu iCloud privado.")}</p></div>
      <div class="card"><span class="num">02</span><h3>{L("Native and light", "Nativos e leves")}</h3><p>{L("Built with Apple's own frameworks, with as few third-party SDKs as possible.", "Feitos com os frameworks da própria Apple, com o mínimo possível de SDKs de terceiros.")}</p></div>
      <div class="card"><span class="num">03</span><h3>{L("Honest privacy", "Privacidade honesta")}</h3><p>{L("Plain-language policies for every app, and a way to delete your data.", "Políticas em linguagem simples para cada app, e um jeito de apagar seus dados.")}</p></div>
      <div class="card"><span class="num">04</span><h3>{L("Made for many languages", "Feitos em vários idiomas")}</h3><p>{L("Every app is built in English and Portuguese from day one, and most also speak Spanish, French, Italian, German and more.", "Todo app nasce em português e inglês, e a maioria também fala espanhol, francês, italiano, alemão e outros.")}</p></div>
    </div>
  </section>

  <section id="apps">
    <p class="section-label">{L("Our apps", "Nossos apps")}</p>
    <h2 class="section-title">{L("Made by LumaRay", "Feitos pela LumaRay")}</h2>
    <div class="app-rows">
{APP_ROWS}
    </div>
  </section>

  <section class="contact-band" id="contact">
    <h2>{L("Get in touch", "Fale com a gente")}</h2>
    <p>{L("Support, feedback, partnerships or privacy questions:", "Suporte, sugestões, parcerias ou dúvidas sobre privacidade:")}</p>
    <p><a href="mailto:lumaraysoftware@gmail.com">lumaraysoftware@gmail.com</a></p>
  </section>
</main>
'''
home += footer("")
write("index.html", home)

# ---------------------------------------------------------------- products
ICONS = {
    "barcode": '<path d="M4 6v12M7 6v12M10 6v12M13 6v12M17 6v12M20 6v12"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".6"/>',
    "people": '<circle cx="9" cy="9" r="3"/><circle cx="16.5" cy="10" r="2.5"/><path d="M3.5 19c.8-3 3-4.5 5.5-4.5s4.7 1.5 5.5 4.5M14.5 15c2.6-.6 5 .6 6 3.5"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 .5-8 6 6 0 0 0-11.4 1.6A3.3 3.3 0 0 0 7 18z"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "star": '<path d="M12 4l2.4 5 5.4.6-4 3.7 1.1 5.3L12 16l-4.9 2.6 1.1-5.3-4-3.7 5.4-.6z"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "split": '<path d="M12 4v6M12 10l-6 6M12 10l6 6"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/>',
    "percent": '<path d="M18 6L6 18"/><circle cx="7.5" cy="7.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/>',
    "send": '<path d="M4 12l16-8-6 16-3-7z"/><path d="M11 13l9-9"/>',
    "bell": '<path d="M6 16v-5a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    "arrows": '<path d="M4 8h14l-3-3M20 16H6l3 3"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
    "plusminus": '<path d="M4 12h6M14 12h6M17 9v6"/>',
    "cart": '<path d="M3 4h2.5l2 11h10.5l2-8H6.5"/><circle cx="9" cy="19" r="1.4"/><circle cx="17" cy="19" r="1.4"/>',
    "tag": '<path d="M3.5 12V4.5h7.5l9 9-7.5 7.5z"/><circle cx="8" cy="8.5" r="1.4"/>',
    "chart": '<path d="M5 19v-7M10 19V6M15 19v-4M20 19V9"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="M15.5 15.5L20 20"/>',
    "widget": '<rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="16" height="7" rx="2"/>',
    "calendar": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M8 3v4M16 3v4"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4"/>',
    "coin": '<circle cx="12" cy="12" r="8"/><path d="M14.5 9.5c-.5-1-1.4-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.6 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1.1 0-2-.5-2.5-1.5M12 6.5V8M12 16v1.5"/>',
}
icons = {
    "next-chapter": ["barcode", "target", "people", "cloud", "lock", "star"],
    "wetab": ["receipt", "split", "percent", "send", "arrows", "search", "bell", "widget"],
    "pantry-stock": ["list", "plusminus", "bell", "cart", "widget", "tag", "calendar", "coin", "chart"],
}

PRODUCTS = {
    "next-chapter": dict(
        tag=("Your reading quest log and book clubs.", "Seu diário de leitura e clube do livro."),
        intro=("Next Chapter keeps your reading life in one place: the books you've read, the ones you're reading and the ones you want next. Set a yearly goal, watch your progress and read together with friends in book clubs, all synced through your own iCloud.",
               "O Next Chapter reúne sua vida de leitor num só lugar: os livros que você leu, os que está lendo e os próximos. Defina uma meta anual, acompanhe seu progresso e leia junto com amigos em clubes do livro, tudo sincronizado pelo seu próprio iCloud."),
        features=[
            (("Scan or search", "Escaneie ou busque"), ("Add books by scanning the barcode or searching by title, author or ISBN.", "Adicione livros escaneando o código de barras ou buscando por título, autor ou ISBN."), ""),
            (("Reading goals", "Metas de leitura"), ("Set a yearly goal and track your progress book by book.", "Defina uma meta anual e acompanhe o progresso livro a livro."), ""),
            (("Book clubs", "Clubes do livro"), ("Invite friends, vote on the next book, share notes and take on reading challenges.", "Convide amigos, votem no próximo livro, compartilhem notas e encarem desafios de leitura."), ""),
            (("iCloud sync", "Sincronização pelo iCloud"), ("Your library follows you across devices, stored in your own iCloud.", "Sua biblioteca acompanha você entre aparelhos, guardada no seu próprio iCloud."), ""),
            (("App lock", "Bloqueio do app"), ("Protect your reading life with Face ID or Touch ID.", "Proteja seu diário com Face ID ou Touch ID."), ""),
            (("Club Plus", "Club Plus"), ("A subscription for more from your book clubs, plus a one-time purchase to remove ads.", "Assinatura com mais recursos para os clubes, e uma compra única para remover anúncios."), "Premium"),
        ],
    ),
    "wetab": dict(
        tag=("Split the bill item by item. Charge with Pix.", "Divida a conta item por item. Cobre com Pix."),
        intro=("WeTab turns the end of a dinner into a few taps: read the receipt, mark who had what, and send each person exactly their share with your Pix key. It keeps track of who owes whom, and lets people know when they've been charged. Available in English, Portuguese, Spanish, French, Italian and German.",
               "O WeTab transforma o fim do jantar em poucos toques: leia o recibo, marque quem consumiu o quê e mande para cada pessoa exatamente a parte dela, com a sua chave Pix. Ele acompanha quem deve a quem e avisa as pessoas quando são cobradas. Disponível em português, inglês, espanhol, francês, italiano e alemão."),
        features=[
            (("Read the receipt", "Leia o recibo"), ("Point the camera or pick a photo, even a card-machine slip or a tilted shot. Items are read on your device.", "Aponte a câmera ou escolha uma foto, até comprovante de maquininha ou foto torta. Os itens são lidos no próprio aparelho."), ""),
            (("Item by item", "Item por item"), ("Tap who had each item. Shared items split to the cent.", "Toque em quem consumiu cada item. Itens divididos são rateados até o centavo."), ""),
            (("Service charge, your way", "Serviço do seu jeito"), ("10%, 12%, 15% or a custom rate, or turn it off for the table.", "10%, 12%, 15% ou outra taxa, ou desligue para a mesa toda."), ""),
            (("Charge with Pix", "Cobre com Pix"), ("Send each person their items, amount and your Pix key, with a link that opens right from WhatsApp.", "Mande para cada pessoa os itens, o valor e sua chave Pix, com um link que abre direto do WhatsApp."), ""),
            (("Know when they pay", "Saiba quando pagam"), ("Get notified when someone opens a charge or says they've paid, and see the fewest transfers that settle the group.", "Receba aviso quando alguém abre a cobrança ou avisa que pagou, e veja o mínimo de transferências que zera o grupo."), ""),
            (("Search bills and people", "Busque contas e pessoas"), ("Find a bill by place or item, and a person by name, right from the top of Home.", "Ache uma conta pelo lugar ou por um item, e uma pessoa pelo nome, no topo da tela inicial."), ""),
            (("Reminders and export", "Lembretes e exportação"), ("Gentle reminders for whoever hasn't paid, and every bill as a PDF or spreadsheet.", "Lembretes para quem ainda não pagou, e todas as contas em PDF ou planilha."), "Pro"),
            (("\u201cTo receive\u201d widget", "Widget \u201cA receber\u201d"), ("How much you're owed, on your Home Screen or Lock Screen. Everything else stays free.", "Quanto te devem, na tela inicial ou na tela bloqueada. O resto continua grátis."), "Pro"),
        ],
    ),
    "pantry-stock": dict(
        tag=("Know what's at home. Never run out.", "Saiba o que tem em casa. Nunca deixe faltar."),
        intro=("Pantry Stock comes with a ready-made catalog of about 75 household supplies, from rice and coffee to detergent and toothpaste. Day to day, you just tap − and +. When something drops below its minimum, it lands on your shopping list. Plus unlocks unlimited items and brands; Pro adds everything else.",
               "O Pantry Stock (Despensa) já vem com um catálogo de cerca de 75 itens da casa, do arroz e café ao detergente e creme dental. No dia a dia, é só tocar em − e +. Quando algo fica abaixo do mínimo, ele vai para a sua lista de compras. O Plus libera itens e marcas sem limite; o Pro traz todo o resto."),
        features=[
            (("Ready-made catalog", "Catálogo pronto"), ("Food, cleaning and personal care items, filtered by your region. Add more from it anytime with +.", "Alimentos, limpeza e higiene, filtrados pela sua região. Adicione mais quando quiser pelo +."), ""),
            (("Big − and + buttons", "Botões − e + grandes"), ("Update quantities in a tap, by unit, weight or volume.", "Atualize quantidades com um toque, por unidade, peso ou volume."), ""),
            (("Low-stock alerts", "Alertas de estoque baixo"), ("A heads-up when something runs low, plus a weekly pantry reminder. Items you haven't touched in 30 days are suggested for removal.", "Aviso quando algo está acabando, e um lembrete semanal da despensa. Itens parados há 30 dias são sugeridos para remoção."), ""),
            (("Automatic shopping list", "Lista de compras automática"), ("Pick Minimum, Half or Target for each item, sort it in your store's aisle order and send it by WhatsApp, Messages or email.", "Escolha Mínimo, Metade ou Ideal para cada item, ordene pelos corredores do seu mercado e envie por WhatsApp, Mensagens ou e-mail."), ""),
            (("Widget and Siri", "Widget e Siri"), ("See the shopping list on your Home Screen or Lock Screen, and tell Siri you ran out of coffee.", "Veja a lista de compras na tela inicial ou na tela bloqueada, e diga à Siri que o café acabou."), ""),
            (("Brands and your own items", "Marcas e itens próprios"), ("Record the exact brand and model, and add as many items as you like.", "Registre marca e modelo exatos, e cadastre quantos itens quiser."), "Plus"),
            (("Expiry dates and home care", "Validade e manutenção da casa"), ("An alert on the day something expires, and reminders to change the sheets, towels or sponge.", "Aviso no dia em que algo vence, e lembretes para trocar lençóis, toalhas ou esponja."), "Plus"),
            (("Prices and monthly spending", "Preços e gasto do mês"), ("Record what you paid, compare with last time and see the month's spending by category.", "Registre quanto pagou, compare com a última compra e veja o gasto do mês por categoria."), "Pro"),
            (("Summaries, forecast and sharing", "Resumos, previsão e compartilhamento"), ("Weekly and monthly consumption, run-out forecasts, and a shopping list shared with your household.", "Consumo semanal e mensal, previsão de quando vai acabar e lista de compras compartilhada com a casa."), "Pro"),
        ],
    ),
}

for slug, name, icon, cls in APPS:
    p = PRODUCTS[slug]
    sh = SHOW[slug]
    s = head("../", name, f"{name} by LumaRay Software: {p['tag'][0]}", cls)
    s += header("../", slug)
    s += f'''<main class="page wide product">
  <section class="showcase">
    <div class="showcase-copy">
      <img class="app-icon" src="../assets/{icon}" alt="{name} app icon">
      <h1>{name}</h1>
      <p class="tagline">{L(*p["tag"])}</p>
      <p class="lead" data-lang-block="en">{p["intro"][0]}</p>
      <p class="lead" data-lang-block="pt" lang="pt-BR">{p["intro"][1]}</p>
      <div class="row-actions">{store_btn(slug)}<a class="go" href="privacy/">{L("Privacy Policy", "Política de Privacidade")}</a></div>
    </div>
    <div class="showcase-art">{art("../", slug, name)}</div>
  </section>

  <section class="screens" aria-labelledby="screens-h">
    <h2 id="screens-h">{L("Inside the app", "Por dentro do app")}</h2>
    <div class="strip {sh["style"]}" tabindex="0">
'''
    for en, pt, cap in sh["shots"]:
        img = LI(shot_src("../", slug, en), shot_src("../", slug, pt), cap[0], cap[1])
        if sh["style"] == "frame":
            s += f'      <figure><div class="phone">{img}</div><figcaption>{L(*cap)}</figcaption></figure>\n'
        else:
            s += f'      <figure class="shot-card">{img}</figure>\n'
    s += f'''    </div>
  </section>

  <h2>{L("Features", "Recursos")}</h2>
  <ul class="features">
'''
    for i, (t, d, badge) in enumerate(p["features"]):
        b = f'<span class="badge">{badge}</span>' if badge else ""
        ic = ICONS[icons[slug][i]]
        s += f'    <li><span class="ficon tone{i}" aria-hidden="true"><svg viewBox="0 0 24 24">{ic}</svg></span><div><strong>{L(*t)}{b}</strong>{L(*d)}</div></li>\n'
    s += f'''  </ul>

  <h2>{L("Help and legal", "Ajuda e informações legais")}</h2>
  <div class="links">
    <a class="card" href="privacy/"><strong>{L("Privacy Policy", "Política de Privacidade")}</strong>{L("How the app handles your information.", "Como o app trata as suas informações.")}</a>
    <a class="card" href="mailto:lumaraysoftware@gmail.com?subject={name.replace(" ", "%20")}%20support"><strong>{L("Support", "Suporte")}</strong>{L("Questions, bugs or feedback? Email lumaraysoftware@gmail.com", "Dúvidas, problemas ou sugestões? Escreva para lumaraysoftware@gmail.com")}</a>
    <a class="card" href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"><strong>{L("Terms of Use", "Termos de Uso")}</strong>{L(f"Apple's standard license agreement applies to {name}.", f"O contrato de licença padrão da Apple se aplica ao {name}.")}</a>
  </div>
</main>
'''
    s += footer("../")
    write(f"{slug}/index.html", s)

    # -------- privacy page: keep the articles, swap the chrome around them
    path = os.path.join(ROOT, slug, "privacy", "index.html")
    old = open(path).read()
    articles = re.findall(r'(  <!-- =+ [A-ZÊ]+ =+ -->\n  <article.*?</article>)', old, re.S)
    assert len(articles) == 2, slug
    title = re.search(r"<title>(.*?)</title>", old).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', old).group(1)
    body = []
    for a in articles:
        a = re.sub(r'<article id="en" lang="en" class="policy">', '<article id="en" lang="en" class="policy" data-lang-block="en">', a)
        a = re.sub(r'<article id="pt" lang="pt-BR" class="policy">', '<article id="pt" lang="pt-BR" class="policy" data-lang-block="pt">', a)
        a = a.replace(' data-lang-block="en" data-lang-block="en"', ' data-lang-block="en"').replace(' data-lang-block="pt" data-lang-block="pt"', ' data-lang-block="pt"')
        body.append(a)
    s = head("../../", title, desc, cls)
    s += header("../../", slug)
    s += f'''<main class="page">
  <section class="product-hero">
    <img src="../../assets/{icon}" alt="{name} app icon">
    <div><h1>{name}</h1><p>{L("Privacy Policy", "Política de Privacidade")}</p></div>
  </section>
  {subtabs("../../", slug, "privacy")}
{body[0]}

{body[1]}
</main>
'''
    s += footer("../../")
    write(f"{slug}/privacy/index.html", s)

# ---------------------------------------------------------------- privacy hub
s = head("../", "LumaRay Privacy", "Privacy policies for every LumaRay Software app.")
s += header("../", "privacy")
s += f'''<main class="page">
  <h1>{L("Privacy", "Privacidade")}</h1>
  <p class="lead">{L("Each app has its own policy, in English and Portuguese.", "Cada app tem sua própria política, em inglês e português.")}</p>

  <ul class="policy-list">
'''
for slug, name, icon, _ in APPS:
    sub = {"next-chapter": ("Reading log and book clubs", "Leitura e clubes do livro"),
           "wetab": ("Bill splitting", "Divisão de contas"),
           "pantry-stock": ("Household supplies", "Estoque da casa")}[slug]
    s += f'''    <li><a class="card" href="../{slug}/privacy/"><img src="../assets/{icon}" alt=""><div><strong>{name}</strong>{L(*sub)}</div></a></li>
'''
s += f'''  </ul>

  <h2>{L("This website", "Este site")}</h2>
  <p data-lang-block="en">This website has no accounts, forms, cookies or analytics. It picks the starting language from your device's time zone, read in your browser and never sent anywhere, and remembers your language choice in your browser's local storage, which never leaves your device. Fonts are loaded from Google Fonts, which receives your IP address when the page loads (<a href="https://policies.google.com/privacy">Google Privacy Policy</a>).</p>
  <p data-lang-block="pt" lang="pt-BR">Este site não tem contas, formulários, cookies nem ferramentas de análise. Ele escolhe o idioma inicial pelo fuso horário do seu aparelho, lido no seu navegador e nunca enviado a lugar nenhum, e lembra o idioma escolhido no armazenamento local do seu navegador, que nunca sai do seu aparelho. As fontes são carregadas do Google Fonts, que recebe o seu endereço IP quando a página abre (<a href="https://policies.google.com/privacy?hl=pt-BR">Política de Privacidade do Google</a>).</p>

  <h2>{L("Contact", "Contato")}</h2>
  <p>LumaRay Software LLC<br><a href="mailto:lumaraysoftware@gmail.com">lumaraysoftware@gmail.com</a></p>
</main>
'''
s += footer("../")
write("privacy/index.html", s)
print("ok")
