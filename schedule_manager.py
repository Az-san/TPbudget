import tkinter as tk
from tkcalendar import Calendar

def save_schedule():
    date = cal.get_date()
    schedule = entry.get()
    if date and schedule:
        with open("db/schedules.txt", "a", encoding="utf-8") as f:
            f.write(f"{date}: {schedule}\n")
        label.config(text=f"予定を保存しました: {date} - {schedule}")
        entry.delete(0, tk.END)

def main():
    global cal, entry, label
    root = tk.Tk()
    root.title("スケジュール管理")

    # カレンダー
    cal = Calendar(root, selectmode="day", date_pattern="yyyy/mm/dd")
    cal.pack(pady=10)

    # スケジュール入力
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    # 保存ボタン
    save_button = tk.Button(root, text="保存", command=save_schedule)
    save_button.pack(pady=5)

    # メッセージラベル
    label = tk.Label(root, text="")
    label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
