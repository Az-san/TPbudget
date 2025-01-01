import pandas as pd
import tkinter as tk
from tkinter import ttk
from google.cloud import storage

# 入力データのテンプレート作成
def create_input_data():
    return pd.DataFrame({
        "日付": pd.date_range(start="2025-01-01", end="2025-01-31").strftime('%Y/%m/%d'),
        "発": [None] * 31,
        "着": [None] * 31,
        "片道/往復": [None] * 31,
        "料金 (円)": [None] * 31
    })

input_df = create_input_data()

# Google Cloud Storageに保存
def save_to_gcs(bucket_name, file_name, df):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(df.to_csv(index=False), "text/csv")
    print(f"File saved to GCS: gs://{bucket_name}/{file_name}")

# GUIアプリケーション
class TransportationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("交通費管理")

        # DataFrame初期化
        self.data = create_input_data()

        # テーブル作成
        self.tree = ttk.Treeview(root, columns=list(self.data.columns), show='headings')
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # データの挿入
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

        # 編集ボタン
        edit_button = tk.Button(root, text="編集", command=self.edit_row)
        edit_button.pack(pady=5)

        # 保存ボタン
        save_button = tk.Button(root, text="Google Cloudに保存", command=self.save_data)
        save_button.pack(pady=5)

    def edit_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            print("行が選択されていません")
            return

        def save_changes():
            row_index = self.tree.index(selected_item[0])
            self.data.at[row_index, "発"] = dep_var.get()
            self.data.at[row_index, "着"] = arr_var.get()
            self.data.at[row_index, "片道/往復"] = type_var.get()
            self.data.at[row_index, "料金 (円)"] = float(fare_var.get()) if fare_var.get().isdigit() else None

            self.tree.item(selected_item[0], values=list(self.data.loc[row_index]))
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("行編集")

        dep_var = tk.StringVar(value=self.data.loc[self.tree.index(selected_item[0]), "発"])
        arr_var = tk.StringVar(value=self.data.loc[self.tree.index(selected_item[0]), "着"])
        type_var = tk.StringVar(value=self.data.loc[self.tree.index(selected_item[0]), "片道/往復"])
        fare_var = tk.StringVar(value=self.data.loc[self.tree.index(selected_item[0]), "料金 (円)"])

        tk.Label(edit_window, text="発").pack()
        dep_entry = ttk.Entry(edit_window, textvariable=dep_var)
        dep_entry.pack()

        tk.Label(edit_window, text="着").pack()
        arr_entry = ttk.Entry(edit_window, textvariable=arr_var)
        arr_entry.pack()

        tk.Label(edit_window, text="片道/往復").pack()
        type_menu = ttk.Combobox(edit_window, textvariable=type_var, values=["片道", "往復"])
        type_menu.pack()

        tk.Label(edit_window, text="料金 (円)").pack()
        fare_entry = ttk.Entry(edit_window, textvariable=fare_var)
        fare_entry.pack()

        save_button = tk.Button(edit_window, text="保存", command=save_changes)
        save_button.pack()

    def save_data(self):
        for i, item in enumerate(self.tree.get_children()):
            row_data = self.tree.item(item)['values']
            self.data.iloc[i] = row_data

        # Google Cloud Storageに保存
        bucket_name = "your-bucket-name"  # GCSのバケット名
        file_name = "transportation_data.csv"
        save_to_gcs(bucket_name, file_name, self.data)

# アプリケーション実行
def main():
    root = tk.Tk()
    app = TransportationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
