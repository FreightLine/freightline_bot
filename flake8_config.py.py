# run_flake8.py

import subprocess

def main():
    print("🔍 Запускаем flake8 проверку...")
    result = subprocess.run(
        ["flake8", "."],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Ошибок не найдено!")
    else:
        print("❌ Обнаружены ошибки:\n")
        print(result.stdout)

if __name__ == "__main__":
    main()
