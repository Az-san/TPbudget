import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# フォントディレクトリのパス
FONT_DIR = "static/fonts"
SETTINGS_FILE = "db/settings.txt"
SCHEDULES_FILE = "db/schedules.txt"

# 初期設定
if not os.path.exists(FONT_DIR):
    print(f"警告: フォントディレクトリ '{FONT_DIR}' が存在しません。")
if not os.path.exists("db"):
    os.makedirs("db")

def get_current_font():
    FONT_FILE = 'db/settings.txt'
    current_font = "Arial"
    try:
        with open(FONT_FILE, 'r', encoding='utf-8') as f:
            current_font = f.read().strip()
    except FileNotFoundError:
        pass
    return current_font


@app.route("/")
def home():
    current_font = get_current_font()
    return render_template("index.html", current_font=current_font)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        content = request.form.get('content')

        if date and time and content:
            with open(SCHEDULES_FILE, 'a', encoding='shift-jis') as f:
                f.write(f'{date} {time} {content}\n')
        return redirect('/schedule')

    schedules = []
    try:
        with open(SCHEDULES_FILE, 'r', encoding='shift-jis') as f:
            schedules = f.readlines()
    except FileNotFoundError:
        schedules = ["スケジュールファイルが見つかりません。"]
    except UnicodeDecodeError:
        schedules = ["ファイルのエンコーディングに問題があります。"]

    current_font = get_current_font()
    return render_template('schedule.html', schedules=schedules, current_font=current_font)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        selected_font = request.form.get('font')
        if selected_font:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                f.write(selected_font)
        return redirect('/settings')

    current_font = get_current_font()

    fonts = ["Arial", "Times New Roman"]
    try:
        local_fonts = [folder for folder in os.listdir(FONT_DIR) if os.path.isdir(os.path.join(FONT_DIR, folder))]
        fonts.extend(local_fonts)
    except FileNotFoundError:
        print("フォントディレクトリが見つかりません。")

    return render_template('settings.html', fonts=fonts, current_font=current_font)

@app.route('/train_routes', methods=['GET', 'POST'])
def train_routes():
    ROUTES_FILE = 'db/routes.csv'  # ファイルパスの定義

    if request.method == 'POST':
        from_station = request.form.get('from')
        to_station = request.form.get('to')
        fare = request.form.get('fare')

        if from_station and to_station and fare:  # 入力データの検証
            try:
                with open(ROUTES_FILE, 'a', encoding='shift-jis') as f:
                    f.write(f'{from_station},{to_station},{fare}\n')
            except FileNotFoundError:
                return "ルート保存ファイルが見つかりません。", 500
        return redirect('/train_routes')

    routes = []
    try:
        with open(ROUTES_FILE, 'r', encoding='shift-jis') as f:
            for line in f:
                from_station, to_station, fare = line.strip().split(',')
                routes.append(f"{from_station} → {to_station}: {fare}円")
    except FileNotFoundError:
        routes = ["登録済みの区間はありません。"]
    except UnicodeDecodeError:
        routes = ["ファイルのエンコーディングに問題があります。"]

    current_font = get_current_font()
    return render_template('train_routes.html', routes=routes, current_font=current_font)



if __name__ == "__main__":
    app.run(debug=True)
