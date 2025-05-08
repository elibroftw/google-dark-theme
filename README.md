# Google Dark Theme

[![Chrome](https://img.shields.io/chrome-web-store/users/ohhpliipfhicocldcakcgpbbcmkjkian.svg?color=black&label=Chrome&style=for-the-badge)](https://chrome.google.com/webstore/detail/dark-theme-for-google-sea/ohhpliipfhicocldcakcgpbbcmkjkian)
[![Firefox](https://img.shields.io/amo/users/dark-theme-for-google-searches.svg?label=Firefox&style=for-the-badge&color=black)](https://addons.mozilla.org/firefox/addon/dark-theme-for-google-searches/)
[![Userstyle](https://img.shields.io/badge/dynamic/json?label=Userstyle&query=version&url=https://raw.githubusercontent.com/elibroftw/google-dark-theme/master/manifest.json&style=for-the-badge&color=black)](https://raw.githubusercontent.com/elibroftw/google-dark-theme/master/style.user.css)
[![Userstyles](https://img.shields.io/badge/dynamic/json?label=Stylish&query=version&url=https://raw.githubusercontent.com/elibroftw/google-dark-theme/master/manifest.json&style=for-the-badge&color=black)](https://userstyles.org/styles/180957/google-searches-dark-theme)

A dark theme for Google (searches and translate).
Click Chrome or Firefox labels above to install.

## Screenshots

![Chromium](https://lh3.googleusercontent.com/XO7DZfVu8nJzBdxhl50Oe4t-YJBSrWNn5wAMgAijoEvxJ1qKvX9ziiwWGpY3e56jlS5oq_XybkhhxnwvUGXeQ1vr=w640-h400-e365-rj-sc0x00ffffff)
![FireFox](https://addons.cdn.mozilla.net/user-media/previews/full/249/249303.png?modified=1608598871)

## Assets

If you are interested in how the promototional images and icons were made,
 the source files are in my [browser themes repo](https://github.com/elibroftw/matte-black-theme/tree/master/Resources).

## Instructions

```cmd
pip install -r requirements.txt
build.cmd -u
# python build.py -u
```

## How to get Environment Variables

- [Firefox](https://addons.mozilla.org/en-US/developers/addon/api/key/)
- [Chrome](https://console.cloud.google.com/marketplace/product/google/chromewebstore.googleapis.com)
  - Enable Chrome Web Store API
  - Click download OAuth client (copy information to GitHub secrets) or create a new one
  - For Refresh token, you need to run locally once first just to go through the process
