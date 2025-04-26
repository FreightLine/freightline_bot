import os
import ast

def check_imports(file_path):
    print(f"\n🔍 Проверка файла: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"❌ SyntaxError: {e}")
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                print(f"✅ Импорт: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            for alias in node.names:
                print(f"✅ Из модуля '{module}' импортировано: {alias.name}")

def check_all(project_path):
    print(f"🚀 Старт проверки совместимости в {project_path}")
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                check_imports(path)

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.abspath(__file__))
    check_all(project_path)
