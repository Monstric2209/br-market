import os
import html
from flask import Flask, make_response, redirect, render_template_string, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OWNER_USERNAME = "Monstric_Malikov"

users = {OWNER_USERNAME: "12345"}
items = []

SERVERS = [
    ("RED [1]", "#ff4444"), ("GREEN [2]", "#44bb44"), ("BLUE [3]", "#4488ff"),
    ("YELLOW [4]", "#ffbb00"), ("ORANGE [5]", "#ff7700"), ("PURPLE [6]", "#aa44ff"),
    ("LIME [7]", "#22cc88"), ("PINK [8]", "#ff66aa"), ("CHERRY [9]", "#cc2244"),
    ("BLACK [10]", "#aaaaaa"), ("INDIGO [11]", "#6644ff"), ("WHITE [12]", "#ffffff"),
    ("MAGENTA [13]", "#ff22cc"), ("CRIMSON [14]", "#cc3333"), ("GOLD [15]", "#ffaa00"),
    ("AZURE [16]", "#3388ff"), ("PLATINUM [17]", "#bbbbbb"), ("AQUA [18]", "#22aaff"),
    ("GRAY [19]", "#888888"), ("ICE [20]", "#00ffff"), ("CHILLI [21]", "#ff3333"),
    ("CHOCO [22]", "#cc6622"), ("MOSCOW [23]", "#ff3333"), ("SPB [24]", "#3388ff"),
    ("UFA [25]", "#ffbb00"), ("SOCHI [26]", "#22aaff"), ("KAZAN [27]", "#33aaff"),
    ("SAMARA [28]", "#aa44ff"), ("ROSTOV [29]", "#ff7700"), ("ANAPA [30]", "#3388ff"),
    ("EKB [31]", "#22cc88"), ("KRASNODAR [32]", "#ff3333"), ("ARZAMAS [33]", "#ffbb00"),
    ("NOVOSIBIRSK [34]", "#22cc88"), ("GROZNY [35]", "#22cc88"), ("SARATOV [36]", "#3388ff"),
    ("OMSK [37]", "#3388ff"), ("IRKUTSK [38]", "#3388ff"), ("VOLGOGRAD [39]", "#ff3333"),
    ("VORONEZH [40]", "#ffbb00"), ("BELGOROD [41]", "#22cc88"), ("MAKHACHKALA [42]", "#22cc88"),
    ("VLADIKAVKAZ [43]", "#aaaaaa"), ("VLADIVOSTOK [44]", "#3388ff"), ("KALININGRAD [45]", "#aaaaaa"),
    ("CHELYABINSK [46]", "#ff7700"), ("KRASNOYARSK [47]", "#ff7700"), ("CHEBOKSARY [48]", "#22cc88"),
    ("KHABAROVSK [49]", "#3388ff"), ("PERM [50]", "#ffbb00"), ("TULA [51]", "#ffbb00"),
    ("RYAZAN [52]", "#aa44ff"), ("MURMANSK [53]", "#3388ff"), ("PENZA [54]", "#22cc88"),
    ("KURSK [55]", "#ff3333"), ("ARKHANGELSK [56]", "#ffbb00"), ("ORENBURG [57]", "#ffbb00"),
    ("KIROV [58]", "#aaaaaa"), ("KEMEROVO [59]", "#ff3333"), ("TYUMEN [60]", "#3388ff"),
    ("TOLYATTI [61]", "#aa44ff"), ("IVANOVO [62]", "#aaaaaa"), ("STAVROPOL [63]", "#3388ff"),
    ("SMOLENSK [64]", "#ffbb00"), ("PSKOV [65]", "#22cc88"), ("BRYANSK [66]", "#22cc88"),
    ("OREL [67]", "#ffbb00"), ("YAROSLAVL [68]", "#ff3333"), ("BARNAUL [69]", "#3388ff"),
    ("LIPETSK [70]", "#aaaaaa"), ("ULYANOVSK [71]", "#ff7700"), ("TAMBOV [73]", "#aaaaaa"),
    ("BRATSK [74]", "#aaaaaa"), ("ASTRAKHAN [75]", "#ff3333"), ("CHITA [76]", "#22cc88"),
    ("KOSTROMA [77]", "#ffbb00"), ("VLADIMIR [78]", "#ff7700"), ("KALUGA [79]", "#3388ff"),
    ("N.NOVGOROD [80]", "#ffbb00"), ("TAGANROG [81]", "#aa44ff"), ("VOLOGDA [82]", "#ff3333"),
    ("TVER [83]", "#3388ff"), ("TOMSK [84]", "#22cc88"), ("IZHEVSK [85]", "#22cc88"),
    ("SURGUT [86]", "#aa44ff"), ("PODOLSK [87]", "#aaaaaa"), ("MAGADAN [88]", "#aaaaaa"),
    ("CHEREPOVETS [89]", "#3388ff"), ("NORILSK [90]", "#3388ff"), ("ASTANA [91]", "#3388ff")
]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_auth():
    return request.cookies.get('username')

def format_price(value):
    try:
        num = int(''.join(filter(str.isdigit, str(value))))
        return f"{num:,}".replace(",", " ")
    except:
        return str(value)

@app.route('/')
def index():
    username = check_auth()
    if not username:
        return redirect(url_for('login'))

    selected_server = request.args.get('server', 'All')
    search_query = request.args.get('q', '').strip().lower()
    sort_order = request.args.get('sort', 'new')

    filtered = items
    if selected_server != 'All':
        filtered = [i for i in filtered if i['server'] == selected_server]
    
    if search_query:
        filtered = [i for i in filtered if search_query in i['title'].lower()]

    if sort_order == 'cheap':
        filtered = sorted(filtered, key=lambda x: x['price_num'])
    elif sort_order == 'expensive':
        filtered = sorted(filtered, key=lambda x: x['price_num'], reverse=True)
    else:
        filtered = sorted(filtered, key=lambda x: x['id'], reverse=True)

    h = '<!DOCTYPE html><html><head><meta charset="UTF-8">'
    h += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    h += '<title>BLACK RUSSIA | Market</title>'
    h += '<style>'
    # Добавили фоновую картинку на весь рабочий стол (body) с затемнением
    h += 'body{font-family:Arial,sans-serif; background: linear-gradient(rgba(13, 13, 13, 0.85), rgba(13, 13, 13, 0.92)), url("https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed; background-size: cover; color:#e0e0e0; margin:0; padding:0; font-size:13px;}'
    h += 'header{position:sticky;top:0;z-index:100;background:linear-gradient(90deg, rgba(26,26,26,0.95), rgba(38,38,38,0.95));color:#ff4500;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #ff4500;box-shadow:0 3px 10px rgba(255,69,0,0.3);backdrop-filter: blur(5px);}'
    
    h += '.hero-banner{position:relative;width:100%;height:150px;background:rgba(0,0,0,0.4);border-bottom:2px solid #ff4500;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:10px;box-sizing:border-box}'
    h += '.hero-banner h1{margin:0;color:#ff4500;font-size:20px;text-shadow:0 2px 8px rgba(255,69,0,0.5)}'
    h += '.hero-banner p{margin:4px 0 0;color:#ccc;font-size:11px;max-width:380px}'

    h += '.box{padding:12px;max-width:550px;margin:auto}'
    # Карточки сделали чуть полупрозрачными для красоты на фоне
    h += '.card{background:rgba(28, 28, 28, 0.85);backdrop-filter: blur(4px);padding:12px;margin-bottom:12px;border-radius:10px;border:1px solid #333;box-shadow:0 3px 10px rgba(0,0,0,0.4);transition:transform 0.2s}'
    h += '.card:hover{border-color:#ff4500}'
    h += '.card img{width:100%;height:160px;object-fit:cover;border-radius:6px;margin-bottom:8px;border:1px solid #444}'
    h += '.btn{display:block;background:linear-gradient(90deg, #ff4500, #ff6a00);color:white;text-align:center;padding:11px;border-radius:6px;text-decoration:none;font-weight:bold;margin-bottom:12px;box-shadow:0 3px 8px rgba(255,69,0,0.3);font-size:14px}'
    h += 'select,input[type="text"]{width:100%;padding:10px;background:rgba(26,26,26,0.9);color:white;border:1px solid #444;border-radius:6px;margin-bottom:10px;box-sizing:border-box;font-size:13px}'
    h += '.price{color:#00ff73;font-weight:bold;font-size:17px;text-shadow:0 0 6px rgba(0,255,115,0.2)}'
    h += '.title{color:#fff;text-decoration:none;font-size:16px;font-weight:bold;display:block;margin:4px 0}'
    h += '.specs{font-size:12px;color:#bbb;margin:4px 0;background:rgba(34,34,34,0.8);padding:5px 7px;border-radius:5px}'
    h += '.menu-row{display:flex;gap:6px}'
    h += '.owner-badge{background:#ff4500;color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;font-weight:bold;margin-left:5px;vertical-align:middle;}'
    h += '</style></head><body>'
    
    user_display = html.escape(username)
    if username == OWNER_USERNAME:
        user_display += ' <span class="owner-badge">👑 ВЛАДЕЛЕЦ</span>'

    h += '<header><span>🔥 <b>BR MARKET</b></span><span><a href="/my" style="color:#ff4500;text-decoration:none;font-weight:bold;">' + user_display + '</a> | <a href="/logout" style="color:#888;text-decoration:none;">Выйти</a></span></header>'
    
    h += '<div class="hero-banner">'
    h += '<h1>BLACK RUSSIA MARKET</h1>'
    h += '<p>Официальная площадка под управлением ' + OWNER_USERNAME + '</p>'
    h += '</div>'

    h += '<div class="box" style="margin-top:5px;"><a href="/add" class="btn">⚡ РАЗМЕСТИТЬ АВТОМОБИЛЬ</a>'
    
    h += '<form method="GET">'
    h += '<input type="text" name="q" placeholder="🔍 Поиск по названию..." value="' + html.escape(search_query) + '">'
    h += '<select name="server" onchange="this.form.submit()">'
    h += '<option value="All">🌐 Все сервера (91)</option>'
    
    for s, color in SERVERS:
        sel = ' selected' if selected_server == s else ''
        h += '<option value="' + s + '" style="color:' + color + '"' + sel + '>' + s + '</option>'
        
    h += '</select>'
    h += '<div class="menu-row"><select name="sort" onchange="this.form.submit()">'
    h += '<option value="new"' + (' selected' if sort_order == 'new' else '') + '>🕒 Сначала новые</option>'
    h += '<option value="cheap"' + (' selected' if sort_order == 'cheap' else '') + '>📉 Сначала дешевые</option>'
    h += '<option value="expensive"' + (' selected' if sort_order == 'expensive' else '') + '>📈 Сначала дорогие</option>'
    h += '</select></div></form><h2 style="color:#ff4500;border-left:3px solid #ff4500;padding-left:6px;margin-top:15px;font-size:15px;">Активные объявления</h2>'

    if filtered:
        for item in filtered:
            susp_str = ", ".join(item['suspension']) if item['suspension'] else "Стоковая"
            formatted_p = format_price(item['price'])
            h += '<div class="card">'
            if item['image']:
                h += '<img src="' + url_for('static', filename='uploads/' + item['image']) + '">'
            h += '<span style="color:' + item['server_color'] + ';font-weight:bold;font-size:12px;">■ Сервер: ' + item['server'] + '</span>'
            h += '<a href="/item/' + str(item['id']) + '" class="title">' + html.escape(item['title']) + '</a>'
            h += '<div class="specs">⚡ Прошивка: <b>' + item['firmware'] + '</b> | Подвеска: <b>' + susp_str + '</b></div>'
            h += '<div class="price">' + formatted_p + ' руб.</div>'
            
            seller_txt = html.escape(item['seller'])
            if item['seller'] == OWNER_USERNAME:
                seller_txt += ' <span class="owner-badge" style="font-size:9px;">ВЛАДЕЛЕЦ</span>'
            h += '<small style="color:#888">Продавец: ' + seller_txt + '</small>'
            
            if username == OWNER_USERNAME or item['seller'] == username:
                h += '<form action="/delete/' + str(item['id']) + '" method="POST" style="margin-top:6px;"><button type="submit" style="background:#cc2222;color:#fff;border:none;padding:5px 10px;border-radius:4px;font-size:11px;cursor:pointer;font-weight:bold;">Удалить</button></form>'

            h += '</div>'
    else:
        h += '<div style="background:rgba(21,21,21,0.85);padding:20px;text-align:center;border-radius:8px;color:#777;border:1px dashed #333;font-size:12px;">Пока нет активных объявлений. Будьте первыми!</div>'

    h += '</div></body></html>'
    return render_template_string(h)

@app.route('/login', methods=['GET', 'POST'])
def login():
    err = ""
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '')
        if u in users and users[u] == p:
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', u)
            return resp
        err = "Неверный ник или пароль!"

    h = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Вход</title>'
    h += '<style>body{font-family:Arial,sans-serif; background: linear-gradient(rgba(13, 13, 13, 0.85), rgba(13, 13, 13, 0.92)), url("https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed; background-size: cover; color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-size:13px}'
    h += '.wrap{background:rgba(22,22,22,0.9);backdrop-filter: blur(5px);padding:25px;border-radius:12px;width:85%;max-width:300px;border:1px solid #333;box-shadow:0 6px 20px rgba(0,0,0,0.6)}'
    h += 'input{width:100%;padding:10px;margin:8px 0;background:#222;border:1px solid #444;color:#fff;border-radius:6px;box-sizing:border-box;font-size:13px}'
    h += 'button{background:linear-gradient(90deg, #ff4500, #ff6a00);color:#fff;border:none;padding:10px;width:100%;border-radius:6px;font-weight:bold;cursor:pointer;margin-top:8px;box-shadow:0 3px 8px rgba(255,69,0,0.3);font-size:13px}'
    h += 'a{color:#ff4500;text-decoration:none}</style></head><body>'
    h += '<div class="wrap"><h2 style="color:#ff4500;text-align:center;margin-top:0;font-size:18px;">🚗 Вход</h2>'
    if err:
        h += '<div style="color:#ff4444;font-size:12px;text-align:center;margin-bottom:8px">' + err + '</div>'
    h += '<form method="POST"><input type="text" name="username" placeholder="Ваш ник" required>'
    h += '<input type="password" name="password" placeholder="Пароль" required>'
    h += '<button type="submit">Войти</button></form>'
    h += '<div style="text-align:center;margin-top:12px;font-size:13px">Нет аккаунта? <a href="/register">Регистрация</a></div></div></body></html>'
    return render_template_string(h)

@app.route('/register', methods=['GET', 'POST'])
def register():
    err = ""
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '')
        if not u or not p:
            err = "Заполните все поля!"
        elif len(u) < 3:
            err = "Ник должен быть длиннее 2 символов!"
        elif u in users:
            err = "Этот ник уже занят!"
        else:
            users[u] = p
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', u)
            return resp

    h = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Регистрация</title>'
    h += '<style>body{font-family:Arial,sans-serif; background: linear-gradient(rgba(13, 13, 13, 0.85), rgba(13, 13, 13, 0.92)), url("https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed; background-size: cover; color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-size:13px}'
    h += '.wrap{background:rgba(22,22,22,0.9);backdrop-filter: blur(5px);padding:25px;border-radius:12px;width:85%;max-width:300px;border:1px solid #333;box-shadow:0 6px 20px rgba(0,0,0,0.6)}'
    h += 'input{width:100%;padding:10px;margin:8px 0;background:#222;border:1px solid #444;color:#fff;border-radius:6px;box-sizing:border-box;font-size:13px}'
    h += 'button{background:linear-gradient(90deg, #ff4500, #ff6a00);color:#fff;border:none;padding:10px;width:100%;border-radius:6px;font-weight:bold;cursor:pointer;margin-top:8px;box-shadow:0 3px 8px rgba(255,69,0,0.3);font-size:13px}'
    h += 'a{color:#ff4500;text-decoration:none}</style></head><body>'
    h += '<div class="wrap"><h2 style="color:#ff4500;text-align:center;margin-top:0;font-size:18px;">⚡ Регистрация</h2>'
    if err:
        h += '<div style="color:#ff4444;font-size:12px;text-align:center;margin-bottom:8px">' + err + '</div>'
    h += '<form method="POST"><input type="text" name="username" placeholder="Придумайте ник" required>'
    h += '<input type="password" name="password" placeholder="Пароль" required>'
    h += '<button type="submit">Создать аккаунт</button></form>'
    h += '<div style="text-align:center;margin-top:12px;font-size:13px">Есть аккаунт? <a href="/login">Войти</a></div></div></body></html>'
    return render_template_string(h)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route('/my')
def my_items():
    username = check_auth()
    if not username: return redirect(url_for('login'))
    
    my_list = [i for i in items if i['seller'] == username]

    h = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Мои объявления</title>'
    h += '<style>body{font-family:Arial,sans-serif; background: linear-gradient(rgba(13, 13, 13, 0.85), rgba(13, 13, 13, 0.92)), url("https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed; background-size: cover; color:#fff;margin:0;padding:0;font-size:13px}'
    h += '.box{padding:12px;max-width:550px;margin:auto}'
    h += '.card{background:rgba(22,22,22,0.9);backdrop-filter: blur(4px);padding:12px;margin-bottom:10px;border-radius:8px;border:1px solid #333}'
    h += '.card img{width:100%;height:140px;object-fit:cover;border-radius:5px;margin-bottom:8px}'
    h += '.btn-del{background:#ff3333;color:white;border:none;padding:8px 12px;border-radius:5px;font-weight:bold;cursor:pointer;margin-top:6px;font-size:12px}'
    h += '.price{color:#00ff73;font-weight:bold;font-size:16px}.title{color:#fff;text-decoration:none;font-size:16px;font-weight:bold;display:block;margin:4px 0}'
    h += '</style></head><body>'
    h += '<div class="box"><h2 style="color:#ff4500;font-size:18px;">📦 Мои объявления</h2>'
    
    if my_list:
        for item in my_list:
            formatted_p = format_price(item['price'])
            h += '<div class="card">'
            if item['image']:
                h += '<img src="' + url_for('static', filename='uploads/' + item['image']) + '">'
            h += '<a href="/item/' + str(item['id']) + '" class="title">' + html.escape(item['title']) + '</a>'
            h += '<div class="price">' + formatted_p + ' руб.</div>'
            h += '<form action="/delete/' + str(item['id']) + '" method="POST"><button type="submit" class="btn-del">Удалить объявление</button></form>'
            h += '</div>'
    else:
        h += '<p style="color:#777">У вас нет активных объявлений.</p>'
        
    h += '<a href="/" style="display:block;margin-top:15px;color:#ff4500;text-decoration:none;font-weight:bold;">← На главную</a></div></body></html>'
    return render_template_string(h)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    username = check_auth()
    if not username: return redirect(url_for('login'))
    global items
    if username == OWNER_USERNAME:
        items = [i for i in items if i['id'] != item_id]
    else:
        items = [i for i in items if not (i['id'] == item_id and i['seller'] == username)]
    return redirect(request.referrer or url_for('index'))

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    username = check_auth()
    if not username: return redirect(url_for('login'))
    item = next((i for i in items if i['id'] == item_id), None)
    if not item: return "Не найдено", 404

    if request.method == 'POST':
        msg = request.form.get('message', '').strip()
        if msg:
            safe_msg = html.escape(msg)
            item['messages'].append(html.escape(username) + ": " + safe_msg)
        return redirect(url_for('item_detail', item_id=item_id))

    msgs = ""
    for m in item['messages']:
        msgs += '<div style="font-size:12px;margin-bottom:5px;border-bottom:1px solid #222;padding-bottom:3px;color:#ddd">' + m + '</div>'
    if not msgs: msgs = '<div style="color:#666;font-size:12px;">Сообщений пока нет</div>'

    susp_str = ", ".join(item['suspension']) if item['suspension'] else "Стоковая"
    formatted_p = format_price(item['price'])

    h = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Товар</title>'
    h += '<style>body{font-family:Arial,sans-serif; background: linear-gradient(rgba(13, 13, 13, 0.85), rgba(13, 13, 13, 0.92)), url("https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed; background-size: cover; color:#fff;margin:0;padding:0;font-size:13px}'
    h += '.wrap{background:rgba(22,22,22,0.9);backdrop-filter: blur(5px);padding:15px;margin:10px auto;border-radius:10px;border:1px solid #333;max-width:500px}'
    h += '.wrap img{width:100%;max-height:240px;object-fit:cover;border-radius:6px;margin-bottom:12px;border:1px solid #444}'
    h += 'input{width:68%;padding:10px;background:#222;border:1px solid #444;color:#fff;border-radius:5px;font-size:12px}'
    h += 'button{background:linear-gradient(90deg, #ff4500, #ff6a00);color:#fff;border:none;padding:10px 12px;border-radius:5px;font-weight:bold;cursor:pointer;font-size:12px}'
    h += '</style></head><body><div class="wrap">'
    if item['image']:
        h += '<img src="' + url_for('static', filename='uploads/' + item['image']) + '">'
    h += '<h2 style="color:#ff4500;margin-top:0;font-size:18px;">' + html.escape(item['title']) + '</h2>'
    h += '<div style="color:#00ff73;font-size:20px;font-weight:bold;margin:8px 0">' + formatted_p + ' руб.</div>'
    h += '<p>⚡ Прошивка: <b>' + item['firmware'] + '</b></p>'
    h += '<p>⚙ Подвеска: <b>' + susp_str + '</b></p>'
    h += '<p>💡 Страбы: ' + item['strob'] + ' | Свет: ' + item['light'] + ' | Гудок: ' + item['horn'] + '</p>'
    h += '<p style="background:rgba(34,34,34,0.8);padding:8px;border-radius:5px;"><b>Описание:</b><br>' + html.escape(item['desc']) + '</p>'
    
    seller_txt = html.escape(item['seller'])
    if item['seller'] == OWNER_USERNAME:
        seller_txt += ' <span style="background:#ff4500;color:#fff;font-size:9px;padding:2px 5px;border-radius:3px;font-weight:bold;">ВЛАДЕЛЕЦ</span>'
    h += '<p style="color:#888;font-size:12px;">Продавец: ' + seller_txt + '</p><hr style="border-color:#333">'
    
    h += '<h3 style="color:#ff4500;font-size:15px;">💬 Чат с продавцом:</h3><div style="background:rgba(17,17,17,0.9);padding:8px;border-radius:5px;max-height:140px;overflow-y:auto;border:1px solid #333">' + msgs + '</div>'
    h += '<form method="POST" style="margin-top:10px;display:flex;gap:6px">'
    h += '<input type="text" name="message" placeholder="Сообщение..." required><button type="submit">Отправить</button></form>'
    
    if username == OWNER_USERNAME or item['seller'] == username:
        h += '<form action="/delete/' + str(item['id']) + '" method="POST" style="margin-top:10px;"><button type="submit" style="background:#cc2222;width:100%;padding:10px;font-size:13px;">Удалить это объявление</button></form>'

    h += '<a href="/" style="display:block;margin-top:15px;color:#ff4500;text-decoration:none;font-weight:bold;">← На главную</a></div></body></html>'
    return render_template_string(h)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    username = check_auth()
    if not username: return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        server_full = request.form.get('server')
        firmware = request.form.get('firmware')
        suspension = request.form.getlist('suspension')
        strob = request.form.get('strob')
        light = request.form.get('light')
        horn = request.form.get('horn')
        price_str = request.form.get('price', '0').strip()
        desc = request.form.get('desc', '').strip()
        
        image_filename = ""
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

        try:
            price_num = int(''.join(filter(str.isdigit, price_str)))
        except:
            price_num = 0

        col = "#ffffff"
        for s, c in SERVERS:
            if s == server_full: col = c

        items.append({
            "id": len(items) + 1,
            "title": title,
            "server": server_full,
            "server_color": col,
            "firmware": firmware,
            "suspension": suspension,
            "strob": strob,
            "light": light,
            "horn": horn,
            "price": price_str,
            "price_num": price_num,
            "desc": desc,
            "seller": username,
            "image": image_filename,
            "messages": []
        })
        return redirect(url_for('index'))

    opts = ""
    for s, c in SERVERS:
        opts += '<option value="' + s + '" style="color:' + c + '">' + s + '</option>'

    h = '<!DOCTYPE html><html><head><meta charset="UTF-8">'
    h += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    h += '<title>Разместить авто</title>'
    h += '<style>'
    h += 'body{font-family:Arial,sans-serif; background: linear-gradient(rgba(13, 13, 13, 0.85), rgba(13, 13, 13, 0.92)), url("https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed; background-size: cover; color:#fff;margin:0;padding:0;font-size:13px}'
    h += '.wrap{padding:12px;max-width:480px;margin:auto}'
    h += 'input,select,textarea{width:100%;padding:10px;margin-bottom:10px;background:rgba(22,22,22,0.9);border:1px solid #444;color:#fff;border-radius:6px;box-sizing:border-box;font-size:13px}'
    h += 'button{background:linear-gradient(90deg, #ff4500, #ff6a00);color:#fff;border:none;padding:12px;width:100%;border-radius:6px;font-weight:bold;cursor:pointer;font-size:14px;box-shadow:0 3px 8px rgba(255,69,0,0.3)}'
    h += 'label{font-size:12px;color:#ff4500;display:block;margin-bottom:4px;font-weight:bold;}'
    h += '.checkbox-group{margin-bottom:10px;background:rgba(22,22,22,0.9);padding:10px;border:1px solid #444;border-radius:6px}'
    h += '.checkbox-group label{color:#fff;display:inline;margin-left:6px;font-size:13px;font-weight:normal;}'
    h += '</style></head><body><div class="wrap"><h2 style="color:#ff4500;text-align:center;font-size:18px;">🚘 Новое объявление</h2><form method="POST" enctype="multipart/form-data">'
    h += '<label>Название машины:</label><input type="text" name="title" placeholder="Например: BMW M5 F90" required>'
    h += '<label>Фото машины:</label><input type="file" name="image" accept="image/*">'
    h += '<label>Сервер:</label><select name="server">' + opts + '</select>'
    
    h += '<label>Прошивка:</label><select name="firmware">'
    h += '<option value="Stock">Stock (Сток)</option>'
    h += '<option value="Comfort">Comfort</option>'
    h += '<option value="Sport">Sport</option>'
    h += '<option value="Sport+">Sport+</option>'
    h += '<option value="Drift">Drift</option>'
    h += '</select>'

    h += '<label>Подвеска:</label>'
    h += '<div class="checkbox-group">'
    h += '<input type="checkbox" name="suspension" value="Пневма" id="pnevma">'
    h += '<label for="pnevma">Пневма</label><br><br>'
    h += '<input type="checkbox" name="suspension" value="Гидравлика" id="hydra">'
    h += '<label for="hydra">Гидравлика</label>'
    h += '</div>'

    h += '<label>Донатные стробоскопы:</label><select name="strob">'
    h += '<option value="Нет">Нет</option><option value="Да">Да</option>'
    h += '</select>'

    h += '<label>Донатный свет:</label><select name="light">'
    h += '<option value="Нет">Нет</option><option value="Да">Да</option>'
    h += '</select>'

    h += '<label>Донатный гудок:</label><select name="horn">'
    h += '<option value="Нет">Нет</option><option value="Да">Да</option>'
    h += '</select>'

    h += '<label>Цена (цифрами):</label>'
    h += '<input type="text" name="price" placeholder="45000000" required>'
    h += '<label>Описание:</label>'
    h += '<textarea name="desc" placeholder="Состояние, ПТС, торг..." rows="3"></textarea>'
    h += '<button type="submit">Опубликовать</button></form>'
    h += '<a href="/" style="display:block;margin-top:12px;color:#ff4500;text-decoration:none;font-weight:bold;text-align:center;">← На главную</a></div></body></html>'
    return render_template_string(h)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
