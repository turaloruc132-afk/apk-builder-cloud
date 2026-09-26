import json
import os

def inject():
    config_path = 'config.json'
    if not os.path.exists(config_path):
        print("Config.json tapılmadı!")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    app_name = config.get('appName', 'HTML to APK')
    pkg_name = config.get('packageName', 'com.example.app')
    version_code = config.get('versionCode', 1)
    version_name = config.get('versionName', '1.0.0')

    print(f"Konfiqurasiya tətbiq edilir: {app_name} ({pkg_name})")

if __name__ == '__main__':
    inject()
