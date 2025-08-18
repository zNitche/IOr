class I18n {
    constructor() {
        this.translations_obj = {};
    }

    setTranslations(translations_obj) {
        this.translations_obj = translations_obj
    }

    t(label) {
        return this.translations_obj[label];
    }
}
