// https://stackoverflow.com/questions/14570058/chrome-content-script-de-activate
var ba = chrome.browserAction;
const url = chrome.runtime.getURL('style.css');
var style = fetch(url)

ba.onClicked.addListener(function () {
    if (api.enabled) {
        settings.set('enabled', false);
    } else {
        settings.set('enabled', true);
    }
});


function inject_css () {
    if (settings.get('enabled')) {
        var node = document.createElement('style');
        node.innerHTML = style;
        document.body.appendChild(node);
    }
}
// content_scripts