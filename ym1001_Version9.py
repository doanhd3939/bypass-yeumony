from flask import Flask, request, jsonify, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests, re, asyncio, threading, time
import os

# === CẤU HÌNH ===
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8029254946:AAE8Upy5LoYIYsmcm8Y117Esm_-_MF0-ChA')
app = Flask(__name__)

TASKS = [
    {"label": "Bypass M88", "type": "m88"},
    {"label": "Bypass FB88", "type": "fb88"},
    {"label": "Bypass 188BET", "type": "188bet"},
    {"label": "Bypass W88", "type": "w88"},
    {"label": "Bypass V9BET", "type": "v9bet"},
    {"label": "Bypass BK8", "type": "bk8"},
    {"label": "Bypass VN88", "type": "vn88"},
]
HELP_BUTTON = {"label": "📖 Hướng dẫn / Hỗ trợ", "callback": "help"}

# CẤU HÌNH NHIỆM VỤ/LOẠI - ĐÃ CẬP NHẬT CODE MỚI CHO V9BET VÀ BK8
BYPASS_CONFIG = {
    'm88':   ('M88', 'https://bet88ec.com/cach-danh-bai-sam-loc', 'https://bet88ec.com/', 'taodeptrai'),
    'fb88':  ('FB88', 'https://fb88mg.com/ty-le-cuoc-hong-kong-la-gi', 'https://fb88mg.com/', 'taodeptrai'),
    '188bet':('188BET', 'https://88betag.com/cach-choi-game-bai-pok-deng', 'https://88betag.com/', 'taodeptrailamnhe'),
    'w88':   ('W88', 'https://188.166.185.213/tim-hieu-khai-niem-3-bet-trong-poker-la-gi', 'https://188.166.185.213/', 'taodeptrai'),
    'v9bet': ('V9BET', 'https://v9betvi.com/kinh-nghiem-ca-do-bong-da', 'https://v9betvi.com/', 'bomaydeptrai'),
    'bk8':   ('BK8', 'https://bk8vi.com/bang-xep-hang-bong-da', 'https://bk8vi.com/', 'bomaylavua'),
    'vn88':  ('VN88', 'https://vn88no.com/keo-chap-1-trai-la-gi', 'https://vn88no.com/', 'bomaydeptrai'),
}

BYPASS_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>BYPASS TRAFFIC | YM5 Tool</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;500&display=swap" rel="stylesheet">
    <style>
        body, html {
            height: 100%; margin: 0; padding: 0;
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
            overflow-x: hidden;
        }
        body {
            min-height: 100vh;
            background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=80') no-repeat center center fixed;
            background-size: cover;
            position: relative;
        }
        .overlay {
            position: fixed; left:0; top:0; right:0; bottom:0; z-index:0;
            background: linear-gradient(120deg, #000a 50%, #1a162cbb 100%);
            pointer-events: none;
        }
        .glass {
            background: rgba(255, 255, 255, 0.19);
            margin: 60px 0 0 0;
            border-radius: 28px;
            box-shadow: 0 12px 48px #000a, 0 2px 10px #8efcff22;
            max-width: 430px; width: 95vw;
            padding: 42px 32px 30px 32px;
            position: relative;
            z-index: 2;
            backdrop-filter: blur(10px);
            border: 2.5px solid rgba(255,255,255,0.23);
            animation: fadeInUp 1.2s cubic-bezier(.29,1.29,.77,1.03);
        }
        @keyframes fadeInUp {
            0% { transform: translateY(80px); opacity: 0;}
            100% { transform: translateY(0); opacity: 1;}
        }
        .brand { text-align: center; margin-bottom: 17px;}
        .brand img {
            width: 84px; height: 84px;
            border-radius: 18px;
            box-shadow: 0 2px 32px #6ff6ffcc;
            animation: logoPop 1.2s cubic-bezier(.22,1.11,.77,1.01);
        }
        @keyframes logoPop {
            0% { transform: scale(.2) rotate(-13deg);}
            70% { transform: scale(1.15) rotate(7deg);}
            100% { transform: scale(1) rotate(0);}
        }
        .brand h1 {
            font-size: 2.2rem;
            margin: 14px 0 0 0;
            color: #fff;
            font-weight: 800;
            text-shadow: 0 2px 24px #29e5ff33, 0 2px 3px #1a162c4a;
            letter-spacing: 3px;
            text-transform: uppercase;
            background: linear-gradient(90deg,#ff8a00,#e52e71,#43cea2,#185a9d,#f158ff,#00f2fe);
            background-size: 200% 200%;
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            animation: gradtxt 4s linear infinite alternate;
        }
        @keyframes gradtxt {
            0% {background-position:0 0;}
            100% {background-position:100% 100%;}
        }
        .desc {
            color: #fff;
            font-size: 1.13rem;
            text-align: center;
            margin-bottom: 20px;
            font-weight: 600;
            line-height: 1.6;
            letter-spacing: 0.01em;
            text-shadow: 0 2px 14px #0006;
        }
        select, button {
            width: 100%; padding: 15px;
            margin-top: 21px; border: none; border-radius: 13px;
            font-size: 1.18rem; font-family: inherit;
            transition: background .19s, box-shadow .23s;
            outline: none;
        }
        select {
            background: #ffffff33; color: #31344b;
            box-shadow: 0 2px 12px #3fafff1c;
            font-weight: 600;
        }
        button {
            background: linear-gradient(90deg,#ff8a00,#e52e71,#43cea2,#185a9d,#f158ff,#00f2fe);
            background-size: 300% 300%;
            color: #fff; font-weight: bold; cursor: pointer;
            margin-bottom: 12px; letter-spacing: 2.1px;
            box-shadow: 0 3px 18px #ffb34736;
            border: 2.5px solid #fff9;
            position: relative; overflow: hidden;
            animation: btnGlow 2.2s infinite alternate;
        }
        @keyframes btnGlow {
            0% { box-shadow: 0 0 18px #ff8a0092;}
            100% { box-shadow: 0 0 32px #43cea2e0;}
        }
        button:disabled {
            background: #283c53bb;
            color: #eee;
            cursor: not-allowed;
            box-shadow: none;
        }
        #result {
            margin-top: 22px;
            padding: 22px 6px;
            border-radius: 13px;
            background: rgba(255,255,255, 0.16);
            font-size: 1.22rem;
            min-height: 36px;
            text-align: center;
            font-family: 'Montserrat', monospace, sans-serif;
            font-weight: 700;
            word-break: break-word;
            animation: fadeInResult 0.85s;
        }
        @keyframes fadeInResult {
            0% { opacity:0; transform: scale(0.9);}
            100% { opacity:1; transform: scale(1);}
        }
        .spinner {
            border: 4px solid #eee;
            border-top: 4px solid #00eaff;
            border-radius: 50%;
            width: 38px; height: 38px;
            animation: spin 0.8s linear infinite;
            display: inline-block;
            margin-bottom: -9px;
            margin-right: 6px;
            vertical-align: middle;
            box-shadow: 0 2px 16px #44f6ff44;
        }
        @keyframes spin {
            0% { transform: rotate(0);}
            100% { transform: rotate(360deg);}
        }
        .footer {
            margin-top: 40px; color: #fafffc;
            font-size: 1rem;
            text-align: center; padding-bottom: 20px;
            z-index: 2; position: relative;
            text-shadow: 0 2px 10px #0006;
        }
        .footer a {
            color: #ffd9fa; text-decoration: none; font-weight: 700;
            transition: color .18s;
        }
        .footer a:hover { color: #00e4ff; text-decoration: underline;}
        .timer {
            font-size: 1.11rem; color: #ffd97e;
            font-weight: 700; letter-spacing: 1px;
        }
        .pulse { animation: pulse 1s infinite; }
        @keyframes pulse {
            0% { color: #ffd97e;}
            50% { color: #fff0a8;}
            100% { color: #ffd97e;}
        }
        .click-effect {
            position: absolute; pointer-events: none;
            border-radius: 50%;
            background: rgba(255,120,255,0.23);
            animation: clickpop 0.6s linear forwards;
            z-index: 4;
        }
        @keyframes clickpop {
            0% { opacity:1; transform: scale(0);}
            80% { opacity:0.8; }
            100% { opacity:0; transform: scale(2.9);}
        }
        @media (max-width: 540px) {
            .glass { padding: 16px 2vw 16px 2vw; }
            .brand h1 { font-size: 1.07rem; }
            .footer { font-size: 0.91rem;}
        }
    </style>
</head>
<body>
    <div class="overlay"></div>
    <div class="glass">
        <div class="brand">
            <img src="https://i.imgur.com/9q7g6pK.png" alt="Anime" />
            <h1>BYPASS YEUMONY BÓNG X</h1>
        </div>
        <div class="desc">
            Bypass Tự Động Chuyên Tính Chính Xác Cao.<br>
            <span style="background:linear-gradient(90deg,#ff8a00,#e52e71,#43cea2,#185a9d,#f158ff,#00f2fe);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:1.09em;">Siêu đơn giản, không cần tài khoản!</span>
        </div>
        <select id="type">
            <option value="m88">M88</option>
            <option value="fb88">FB88</option>
            <option value="188bet">188BET</option>
            <option value="w88">W88</option>
            <option value="v9bet">V9BET</option>
            <option value="bk8">BK8</option>
            <option value="vn88">VN88</option>
        </select>
        <button id="getBtn" onclick="submitForm(event)">LẤY MÃ BÓNG X</button>
        <div id="result"></div>
    </div>
    <div class="footer">
        YM5 Tool &copy; 2025 &ndash; Design by <a href="https://t.me/doanh444" target="_blank">Bóng X Telegram</a>
    </div>
    <!-- Hiệu ứng click + âm thanh -->
    <audio id="sndClick" src="https://cdn.pixabay.com/audio/2022/07/26/audio_124bfa8b0a.mp3"></audio>
    <audio id="sndBoop" src="https://cdn.pixabay.com/audio/2022/03/15/audio_117d8b7d9d.mp3"></audio>
<script>
let countdownInterval = null;
let sndClick = document.getElementById('sndClick');
let sndBoop = document.getElementById('sndBoop');

function playClickSound() {
    sndClick.currentTime = 0;
    sndClick.play();
}
function playBoop() {
    sndBoop.currentTime = 0;
    sndBoop.play();
}
function clickEffect(e, target) {
    const rect = target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const effect = document.createElement('div');
    effect.className = 'click-effect';
    effect.style.left = (x-18) + 'px';
    effect.style.top = (y-18) + 'px';
    effect.style.width = effect.style.height = '36px';
    target.appendChild(effect);
    setTimeout(() => target.removeChild(effect), 700);
}

function submitForm(e) {
    var type = document.getElementById('type').value;
    var resultDiv = document.getElementById('result');
    var btn = document.getElementById('getBtn');
    btn.disabled = true;
    let counter = 75;
    resultDiv.innerHTML = '<div class="spinner"></div> <span class="timer pulse" id="timer">Đang lấy mã... Vui lòng chờ 75 giây</span>';
    countdownInterval = setInterval(function() {
        counter--;
        document.getElementById('timer').innerHTML = "Vui lòng chờ " + counter + " giây...";
        if (counter === 5) playBoop();
        if (counter <= 0) {
            clearInterval(countdownInterval);
        }
    }, 1000);

    if(e) {
        playClickSound();
        clickEffect(e, btn);
    }

    fetch('/bypass', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: type})
    })
    .then(res => res.json())
    .then(data => {
        clearInterval(countdownInterval);
        btn.disabled = false;
        resultDiv.innerHTML = formatResult(data.msg);
        playBoop();
    })
    .catch(e => {
        clearInterval(countdownInterval);
        btn.disabled = false;
        resultDiv.innerHTML = "<span style='color:#ff6f6f;'>Lỗi: Không thể kết nối máy chủ.</span>";
    });
}

function formatResult(msg) {
    if(msg.includes('✅')) {
        return `<span style="color:#31ff8a;font-weight:bold;font-size:1.24rem;">${msg}</span>`;
    } else if(msg.includes('⚠️')) {
        return `<span style="color:#ffd166;">${msg}</span>`;
    } else if(msg.includes('❌')) {
        return `<span style="color:#ff6f6f;">${msg}</span>`;
    } else {
        return msg;
    }
}
</script>
</body>
</html>
"""

def beautify_result(type, result):
    # Nhận diện loại kết quả và lấy màu, icon động
    type_label = type.upper()
    icons = {
        "✅": "🎉",
        "⚠️": "⚠️",
        "❌": "💥",
    }
    color_borders = {
        "✅": "#31ff8a",
        "⚠️": "#ffd166",
        "❌": "#ff6f6f",
    }
    titles = {
        "✅": "THÀNH CÔNG",
        "⚠️": "CẢNH BÁO",
        "❌": "THẤT BẠI",
    }
    for key in icons:
        if key in result:
            icon = icons[key]
            border_color = color_borders[key]
            big_title = titles[key]
            break
    else:
        icon = "🔔"
        border_color = "#00eaff"
        big_title = "THÔNG BÁO"
    # Khung gradient + icon + animation Telegram (dùng emoji và unicode cho bắt mắt)
    border = f'<span style="color:{border_color};font-size:1.45em;">{"━" * 16}</span>'
    title_html = (
        f'<b><span style="font-size:2em">{icon}</span> <span style="color:{border_color};font-size:1.25em;">{big_title}</span></b>'
    )
    task_html = (
        f'<b>🎯 Nhiệm vụ:</b> <span style="color:#00eaff;font-weight:bold;font-size:1.13em">{type_label}</span>'
    )
    admin_html = (
        '<b>👨‍💻 Hỗ trợ:</b> <a href="https://t.me/doanhvip1">@doanhvip1</a>'
    )
    note_html = '<i>💡 Bạn có thể tiếp tục chọn nhiệm vụ khác hoặc nhấn <b>/start</b> để quay lại menu chính.</i>'
    # Chèn hiệu ứng nổi cho mã code
    result = result.replace(
        "Mã</b>:", 'Mã</b>: <span style="background:linear-gradient(90deg,#31ff8a,#ffd166,#ff6f6f);'
        'padding:2px 6px;border-radius:8px;font-weight:bold;">'
    ).replace("</code>", "</span></code>")
    return (
        f"{title_html}\n"
        f"{border}\n"
        f"{result}\n"
        f"{border}\n"
        f"{task_html}\n"
        f"{admin_html}\n"
        f"{note_html}"
    )

def bypass(type):
    if type not in BYPASS_CONFIG:
        return f'❌ Sai loại: <code>{type}</code>'
    name, url, ref, code_key = BYPASS_CONFIG[type]
    try:
        res = requests.post(f'https://traffic-user.net/GET_MA.php?codexn={code_key}&url={url}&loai_traffic={ref}&clk=1000')
        match = re.search(r'<span id="layma_me_vuatraffic"[^>]*>\s*(\d+)\s*</span>', res.text)
        if match:
            return f'✅ <b>{name}</b> | <b style="color:#32e1b7;">Mã</b>: <code>{match.group(1)}</code>'
        else:
            return f'⚠️ <b>{name}</b> | <span style="color:#ffd166;">Không tìm thấy mã</span>'
    except Exception as e:
        return f'❌ <b>Lỗi khi lấy mã:</b> <code>{e}</code>'

@app.route('/bypass', methods=['POST'])
def handle_api():
    json_data = request.get_json()
    type = (json_data.get('type') or '').strip().lower()
    time.sleep(75)
    result = bypass(type)
    return jsonify({'msg': result})

@app.route('/bypass-cli', methods=['POST'])
def bypass_cli():
    json_data = request.get_json(force=True)
    type = (json_data.get('type') or '').strip().lower()
    time.sleep(75)
    if type not in BYPASS_CONFIG:
        return jsonify({'ok': False, 'error': f'Sai loại: {type}'})
    name, url, ref, code_key = BYPASS_CONFIG[type]
    try:
        res = requests.post(f'https://traffic-user.net/GET_MA.php?codexn={code_key}&url={url}&loai_traffic={ref}&clk=1000')
        match = re.search(r'<span id="layma_me_vuatraffic"[^>]*>\s*(\d+)\s*</span>', res.text)
        if match:
            return jsonify({'ok': True, 'type': type, 'code': match.group(1)})
        else:
            return jsonify({'ok': False, 'error': 'Không tìm thấy mã'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/', methods=['GET'])
def index():
    return render_template_string(BYPASS_TEMPLATE)

def start_flask():
    app.run(host="0.0.0.0", port=5000, threaded=True)

# ==== TELEGRAM BOT CẢI TIẾN THÔNG BÁO ====
async def send_main_menu(chat_id, context):
    keyboard = []
    for i in range(0, len(TASKS), 2):
        line = []
        for task in TASKS[i:i+2]:
            line.append(InlineKeyboardButton(task["label"], callback_data=f"bypass:{task['type']}"))
        keyboard.append(line)
    keyboard.append([InlineKeyboardButton(HELP_BUTTON["label"], callback_data=HELP_BUTTON["callback"])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="<b>🔰 CHỌN NHIỆM VỤ BYPASS-BÓNG X:</b>\nBạn có thể tiếp tục chọn nhiệm vụ khác hoặc xem hướng dẫn 👇",
        parse_mode="HTML", reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "mainmenu":
        await send_main_menu(query.message.chat_id, context)
        return

    if data == "contact_admin":
        await query.edit_message_text(
            "<b>💬 Liên hệ hỗ trợ:</b>\nBạn có thể nhắn trực tiếp cho <b>@doanhvip12</b> qua Telegram:\n<a href='https://t.me/doanhvip1'>@doanhvip1</a>\n\nHoặc tham gia nhóm <b>...</b>",
            parse_mode="HTML", disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Quay lại hướng dẫn", callback_data="help")],
                [InlineKeyboardButton("🏠 Quay lại Menu", callback_data="mainmenu")]
            ])
        )
        return
    if data == HELP_BUTTON["callback"]:
        help_text = (
            "<b>📖 HƯỚNG DẪN SỬ DỤNG BOT BYPASS & HỖ TRỢ</b>\n"
            "• Bypass traffic (lấy mã) cho các loại: <b>M88, FB88, 188BET, W88, V9BET, BK8, VN88</b>.\n"
            "• Giao diện Telegram cực dễ dùng, thao tác nhanh chóng.\n"
            "━━━━━━━━━━━━━\n"
            "<b>2. CÁCH SỬ DỤNG:</b>\n"
            "– Dùng các NÚT NHIỆM VỤ hoặc lệnh <code>/ym &lt;loại&gt;</code>\n"
            "Ví dụ: <code>/ym m88</code> hoặc <code>/ym bk8</code>\n"
            "━━━━━━━━━━━━━\n"
            "<b>5. HỖ TRỢ & LIÊN HỆ:</b>\n"
            "• Admin: <a href='https://t.me/doanhvip1'>@doanhvip12</a> | Nhóm: <a href='https://t.me/doanhvip1'>https://t.me/doanhvip1</a>\n"
            "<i>Chúc bạn thành công! 🚀</i>"
        )
        help_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Quay lại Menu", callback_data="mainmenu")],
            [InlineKeyboardButton("💬 Liên hệ Admin & Nhóm", callback_data="contact_admin")]
        ])
        await query.edit_message_text(
            help_text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=help_keyboard
        )
        return

    if data.startswith("bypass:"):
        type = data.split(":", 1)[1]
        user = query.from_user.first_name or "User"
        await query.edit_message_text(
            f"⏳ <b>Đang thực hiện nhiệm vụ:</b> <code>{type}</code>\n<i>Vui lòng chờ 75 giây để lấy kết quả...</i>",
            parse_mode="HTML"
        )
        async def delay_and_reply():
            await asyncio.sleep(75)
            result = bypass(type)
            beautified = beautify_result(type, result)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=beautified,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            await send_main_menu(query.message.chat_id, context)
        asyncio.create_task(delay_and_reply())

async def ym_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_html(
            "📌 <b>Hướng dẫn sử dụng:</b>\n<b>/ym &lt;loại&gt;</b>\nVí dụ: <code>/ym m88</code>\n<b>Các loại hợp lệ:</b> <i>m88, fb88, 188bet, w88, v9bet, bk8, vn88</i>"
        )
        return
    type = context.args[0].lower()
    user = update.effective_user.first_name or "User"
    await update.message.reply_html(
        f"🕒 <b>Xin chào {user}!</b>\nĐang xử lý, vui lòng đợi <b>75 giây</b> để lấy mã...\n<i>Bạn sẽ nhận được thông báo kết quả tự động.</i>"
    )
    async def delay_and_reply():
        await asyncio.sleep(75)
        result = bypass(type)
        beautified = beautify_result(type, result)
        await update.message.reply_html(
            beautified,
            disable_web_page_preview=True
        )
        await send_main_menu(update.effective_chat.id, context)
    asyncio.create_task(delay_and_reply())

if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", lambda update, ctx: send_main_menu(update.effective_chat.id, ctx)))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("ym", ym_command))
    application.run_polling()