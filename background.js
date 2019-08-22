// https://stackoverflow.com/questions/14570058/chrome-content-script-de-activate
var ba = chrome.browserAction;
ba.onClicked.addListener(function () {
    if (api.enabled) {
        settings.set('enabled', false);
        api.disable();
    } else {
        settings.set('enabled', true);
        api.enable();
    }
});
content_scripts