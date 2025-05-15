import json
import os

from flask import request, session


def load_i18n(lang: str, fallback="en", base_dir="translations") -> dict:
    def load(path):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}

    primary = load(f"{base_dir}/{lang}.json")
    fallback_data = load(f"{base_dir}/{fallback}.json") if lang != fallback else {}
    return {**fallback_data, **primary}


def get_translator(lang: str):
    translations = load_i18n(lang)
    return lambda key: translations.get(key, f"[{key}]")


def get_locale(fallback="en", supported=None):
    supported = supported or []
    # 1. session
    if "lang" in session:
        return session["lang"]
    # 2. ?lang query
    lang = request.args.get("lang")
    if lang:
        session["lang"] = lang
        return lang
    # 3. browser Accept-Language
    accept = request.headers.get("Accept-Language", "")
    for part in accept.split(","):
        code = part.split(";")[0].strip().lower().split("-")[0]
        if code in supported:
            return code
    return fallback
