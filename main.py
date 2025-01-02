import tkinter as tk
from train_routes import main as train_routes_main
from schedule_manager import main as schedule_manager_main

def open_train_routes():
    train_routes_main()

def open_schedule_manager():
    schedule_manager_main()

# メインメニュー
root = tk.Tk()
root.title("管理アプリ")

tk.Label(root, text="管理アプリ").pack(pady=10)

# 電車区間登録ボタン
btn_train_routes = tk.Button(root, text="電車区間登録", command=open_train_routes)
btn_train_routes.pack(pady=5)

# スケジュール管理ボタン
btn_schedule_manager = tk.Button(root, text="スケジュール管理", command=open_schedule_manager)
btn_schedule_manager.pack(pady=5)

root.mainloop()
