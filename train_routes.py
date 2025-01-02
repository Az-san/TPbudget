import tkinter as tk

def save_route():
    from_station = entry_from.get()
    to_station = entry_to.get()
    fare = entry_fare.get()
    if from_station and to_station and fare:
        # Shift_JISで保存
        with open("db/routes.csv", "a", encoding="shift_jis") as f:
            f.write(f"{from_station},{to_station},{fare}\n")
        label.config(text=f"区間を保存しました: {from_station} -> {to_station} ({fare}円)")
        entry_from.delete(0, tk.END)
        entry_to.delete(0, tk.END)
        entry_fare.delete(0, tk.END)


def main():
    root = tk.Tk()
    root.title("電車区間登録")

    # 入力フィールド
    tk.Label(root, text="出発駅").pack()
    global entry_from, entry_to, entry_fare, label
    entry_from = tk.Entry(root, width=20)
    entry_from.pack()

    tk.Label(root, text="到着駅").pack()
    entry_to = tk.Entry(root, width=20)
    entry_to.pack()

    tk.Label(root, text="料金 (円)").pack()
    entry_fare = tk.Entry(root, width=20)
    entry_fare.pack()

    # 保存ボタン
    save_button = tk.Button(root, text="保存", command=save_route)
    save_button.pack(pady=5)

    # メッセージ表示
    label = tk.Label(root, text="")
    label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
