import os

# 作りたいディレクトリ構造
structure = {
    "myapp": {
        "templates": ["index.html", "schedule.html", "train_routes.html"],
        "static": {
            "css": ["styles.css"]
        }
    }
}

def create_structure(base_path, structure):
    for folder, content in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        if isinstance(content, dict):
            # サブディレクトリがある場合
            create_structure(folder_path, content)
        elif isinstance(content, list):
            # ファイルを作成
            for file in content:
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'w') as f:
                    f.write("")  # 空ファイルを作成

# 現在のディレクトリに作成
base_dir = os.getcwd()
create_structure(base_dir, structure)
print("ディレクトリ構造を作成しました。")
