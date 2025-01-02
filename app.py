from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # フォームから日付、時間、内容を取得
        date = request.form.get('date')
        time = request.form.get('time')
        content = request.form.get('content')
        
        # スケジュールを保存
        if date and time and content:  # 入力値の検証
            with open('db/schedules.txt', 'a', encoding='shift-jis') as f:
                f.write(f'{date} {time} {content}\n')
        
        # 保存後にスケジュールページにリダイレクト
        return redirect('/schedule')
    
    # 保存済みスケジュールを読み込む
    schedules = []
    try:
        with open('db/schedules.txt', 'r', encoding='shift-jis') as f:
            schedules = f.readlines()
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        schedules = ["ファイルのエンコーディングに問題があります。"]

    return render_template('schedule.html', schedules=schedules)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # ユーザーが選択したフォントを保存
        selected_font = request.form.get('font')
        with open('db/settings.txt', 'w', encoding='utf-8') as f:
            f.write(selected_font)
        return redirect('/settings')

    # 現在のフォント設定を読み込む
    current_font = "default"
    try:
        with open('db/settings.txt', 'r', encoding='utf-8') as f:
            current_font = f.read().strip()
    except FileNotFoundError:
        pass

    # フォントリスト
    fonts = [
        "Arial", "Verdana", "Times New Roman", 
        "Pacifico", "Lobster", "Dancing Script", 
        "Amatic SC", "Caveat"
    ]
    return render_template('settings.html', fonts=fonts, current_font=current_font)


if __name__ == "__main__":
    app.run(debug=True)
