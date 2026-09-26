#!/usr/bin/env python3
"""
Reads config.json (committed at the repo root by the Android client app)
and rewrites the template-app project so it builds the user's requested app:
application id, version, name, icon, permissions, and every WebView option.
"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "template-app")


def load_config():
    with open(os.path.join(ROOT, "config.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def patch_build_gradle(cfg):
    path = os.path.join(TEMPLATE, "app", "build.gradle.kts")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("APPLICATION_ID_PLACEHOLDER", cfg["packageName"])
    content = content.replace("VERSION_NAME_PLACEHOLDER", cfg["versionName"])
    content = content.replace("VERSION_CODE_PLACEHOLDER", str(cfg["versionCode"]))

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def patch_strings(cfg):
    path = os.path.join(TEMPLATE, "app", "src", "main", "res", "values", "strings.xml")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    escaped_name = cfg["appName"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    content = content.replace("APP_NAME_PLACEHOLDER", escaped_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def patch_manifest(cfg):
    path = os.path.join(TEMPLATE, "app", "src", "main", "AndroidManifest.xml")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    perms = cfg.get("permissions", [])
    perm_block = "\n".join(f'    <uses-permission android:name="{p}" />' for p in perms)
    content = content.replace("<!-- PERMISSIONS_PLACEHOLDER -->", perm_block)

    orientation_map = {
        "portrait": "portrait",
        "landscape": "landscape",
        "sensor": "fullSensor",
        "unspecified": "unspecified",
    }
    orientation = orientation_map.get(cfg.get("orientation", "unspecified"), "unspecified")
    content = content.replace("ORIENTATION_PLACEHOLDER", orientation)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def patch_generated_config(cfg):
    """Writes a small Kotlin object with all WebView / behaviour options
    read by MainActivity at runtime, so no manual string replacement is
    needed inside the Kotlin source itself."""
    kt_dir = os.path.join(TEMPLATE, "app", "src", "main", "java", "com", "generated", "webviewapp")
    os.makedirs(kt_dir, exist_ok=True)
    remote_url = cfg.get("sourceUrl") or ""
    user_agent = (cfg.get("customUserAgent") or "").replace('"', '\\"')

    kt = f'''package com.generated.webviewapp

/** Auto-generated at build time by scripts/inject_config.py. Do not edit by hand. */
object GeneratedConfig {{
    const val REMOTE_URL: String = "{remote_url}"
    const val SPLASH_DURATION_MS: Long = {cfg.get("splashDurationMs", 1500)}L
    const val JAVASCRIPT_ENABLED: Boolean = {str(cfg.get("javascriptEnabled", True)).lower()}
    const val DOM_STORAGE_ENABLED: Boolean = {str(cfg.get("domStorageEnabled", True)).lower()}
    const val ZOOM_CONTROLS: Boolean = {str(cfg.get("zoomControls", False)).lower()}
    const val CUSTOM_USER_AGENT: String = "{user_agent}"
    const val CACHE_MODE: String = "{cfg.get("cacheMode", "LOAD_DEFAULT")}"
    const val CLEAR_DATA_ON_EXIT: Boolean = {str(cfg.get("clearDataOnExit", False)).lower()}
    const val FULLSCREEN: Boolean = {str(cfg.get("fullscreen", False)).lower()}
    const val KEEP_SCREEN_AWAKE: Boolean = {str(cfg.get("keepScreenAwake", False)).lower()}
    const val ALLOW_MIXED_CONTENT: Boolean = {str(cfg.get("allowMixedContent", False)).lower()}
    const val PULL_TO_REFRESH: Boolean = {str(cfg.get("pullToRefresh", False)).lower()}
    const val HAS_CUSTOM_ERROR_PAGE: Boolean = {str(cfg.get("hasCustomErrorPage", False)).lower()}
}}
'''
    with open(os.path.join(kt_dir, "GeneratedConfig.kt"), "w", encoding="utf-8") as f:
        f.write(kt)


def copy_www_and_assets(cfg):
    assets_dir = os.path.join(TEMPLATE, "app", "src", "main", "assets", "www")
    os.makedirs(assets_dir, exist_ok=True)

    src_www = os.path.join(ROOT, "www")
    if cfg.get("sourceType") != "URL" and os.path.isdir(src_www):
        for item in os.listdir(src_www):
            s = os.path.join(src_www, item)
            d = os.path.join(assets_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    icon_src = os.path.join(ROOT, "icon.png")
    if os.path.isfile(icon_src):
        mipmap_dir = os.path.join(TEMPLATE, "app", "src", "main", "res", "mipmap-xxxhdpi")
        os.makedirs(mipmap_dir, exist_ok=True)
        shutil.copy2(icon_src, os.path.join(mipmap_dir, "ic_launcher.png"))
        shutil.copy2(icon_src, os.path.join(mipmap_dir, "ic_launcher_round.png"))

    splash_src = os.path.join(ROOT, "splash.png")
    if os.path.isfile(splash_src):
        drawable_dir = os.path.join(TEMPLATE, "app", "src", "main", "res", "drawable")
        os.makedirs(drawable_dir, exist_ok=True)
        # Remove the default vector fallback so it doesn't collide with the
        # real PNG (both would otherwise map to the same @drawable/splash_image id).
        fallback_xml = os.path.join(drawable_dir, "splash_image.xml")
        if os.path.isfile(fallback_xml):
            os.remove(fallback_xml)
        shutil.copy2(splash_src, os.path.join(drawable_dir, "splash_image.png"))


def main():
    cfg = load_config()
    patch_build_gradle(cfg)
    patch_strings(cfg)
    patch_manifest(cfg)
    patch_generated_config(cfg)
    copy_www_and_assets(cfg)
    print("Config injected successfully for", cfg["appName"])


if __name__ == "__main__":
    main()
