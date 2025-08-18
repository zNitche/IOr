from typing import Any
import os
import json
from flask import Flask, has_app_context, session


class I18n:
    def __init__(self, translations_path: str, default_lang: str = "en"):
        self.default_lang = default_lang
        self.translations_path = translations_path

        self.__translations: dict[str, dict[str, Any]] = {}

    def __load_translations(self):
        if not os.path.exists(self.translations_path):
            raise Exception(
                f"translations directory {self.translations_path} doesn't exist")

        for file in os.listdir(self.translations_path):
            if file.endswith(".json"):
                translation_label = file.replace(".json", "")
                file_path = os.path.join(self.translations_path, file)

                with open(file_path, "r") as i18n_file:
                    json_content = json.loads(i18n_file.read())

                self.__translations[translation_label] = json_content

    def t(self, i18n_key: str, format: dict[str, str | int] | None = None):
        if not has_app_context():
            raise Exception(
                "i18n context processor called outside app context")

        language_key = session.get("lang")

        if not language_key:
            return i18n_key

        language_data = self.__translations.get(language_key)

        if not language_data:
            return i18n_key

        split_i18n_key = i18n_key.split(".")

        current_i18n_item = language_data.get(split_i18n_key[0])
        split_i18n_key.pop(0)

        if not current_i18n_item:
            return i18n_key

        for key in split_i18n_key:
            current_i18n_item = current_i18n_item.get(key)

            if current_i18n_item is None:
                break

        if current_i18n_item is None:
            return i18n_key

        if format is not None and isinstance(current_i18n_item, str):
            return current_i18n_item.format(**format)

        return current_i18n_item

    def before_request(self):
        if not has_app_context():
            raise Exception(
                "i18n before request handler called outside app context")

        language_key = session.get("lang")

        if not language_key or language_key not in self.__translations.keys():
            session["lang"] = self.default_lang

    def setup(self, app: Flask):
        self.__load_translations()
        app.logger.info(
            f"[I18n] {len(self.__translations.keys())} translation files has been loaded")

        app.context_processor(lambda: {"i18n": self.t})

        app.logger.info("[I18n] has been initialized")
