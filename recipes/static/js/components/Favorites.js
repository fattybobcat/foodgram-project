class Favorites {
    constructor(config, api, csrf_token ) {
        this.config = config;
        this.api = api;
        this.csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }

    addFavorites (target,cardId,callBack) {
        target.setAttribute('disabled', true)
        this.api.addFavorites(cardId)
            .then( e => {
                target.innerHTML = this.config.active.text;
                target.removeAttribute(this.config.attr);
                callBack&&callBack()
            })
            .finally(e => {
                target.removeAttribute('disabled');
            })
    };
    removeFavorites (target,cardId,callBack) {
        target.setAttribute('disabled', true)
        this.api.removeFavorites(cardId)
            .then( e => {
                target.innerHTML = this.config.default.text;
                target.setAttribute(this.config.attr, true);
                callBack&&callBack()
            })
            .finally(e => {
                target.removeAttribute('disabled');
            })
    };
}
