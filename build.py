import argparse
from asyncio import constants
import io
import json
import os
import time
from typing import Iterable
import uuid
import webbrowser
from datetime import datetime
from glob import glob
from shutil import rmtree
from zipfile import ZipFile

import jwt
import pyperclip
import requests
from git import Repo

parser = argparse.ArgumentParser(description="Google Dark Theme Build & Upload Script")
parser.add_argument(
    "--upload",
    "-u",
    default=False,
    action="store_true",
    help="Upload to mozilla addons after",
)
args = parser.parse_args()

top_level_domains = {
    "com.pk",
    "mk",
    "com.bz",
    "gg",
    "com.gi",
    "co.zw",
    "com.mm",
    "sm",
    "ee",
    "lt",
    "rs",
    "dz",
    "com.pg",
    "be",
    "ga",
    "cl",
    "sr",
    "com.sv",
    "ro",
    "co.ug",
    "dk",
    "com.kh",
    "com.pe",
    "at",
    "co.ck",
    "gy",
    "com.et",
    "hu",
    "co.zm",
    "nl",
    "rw",
    "nu",
    "cv",
    "gr",
    "co.ke",
    "com.pr",
    "com.ai",
    "com.sb",
    "com.tr",
    "com.ua",
    "cd",
    "tt",
    "lv",
    "ca",
    "nr",
    "com",
    "jo",
    "ws",
    "cf",
    "lu",
    "cz",
    "com.qa",
    "si",
    "co.za",
    "co.bw",
    "tn",
    "com.ar",
    "gm",
    "ie",
    "com.ni",
    "tm",
    "ps",
    "com.vn",
    "co.nz",
    "ge",
    "is",
    "co.cr",
    "so",
    "com.gr",
    "com.fj",
    "co.mz",
    "by",
    "it",
    "ae",
    "com.ag",
    "sc",
    "com.eg",
    "com.hk",
    "pt",
    "bj",
    "com.bo",
    "ms",
    "ci",
    "es",
    "co.th",
    "ch",
    "co.il",
    "co.uk",
    "com.ph",
    "bg",
    "com.uy",
    "ad",
    "se",
    "ba",
    "no",
    "co.tz",
    "kg",
    "li",
    "com.sa",
    "ml",
    "com.mt",
    "com.co",
    "gl",
    "de",
    "mw",
    "cat",
    "co.jp",
    "la",
    "com.cy",
    "as",
    "mv",
    "bf",
    "je",
    "am",
    "hr",
    "al",
    "com.mx",
    "com.sl",
    "com.ly",
    "com.my",
    "com.cu",
    "co.kr",
    "com.ec",
    "cn",
    "co.ve",
    "co.vi",
    "com.au",
    "vu",
    "bi",
    "tg",
    "fi",
    "co.ao",
    "com.do",
    "to",
    "co.in",
    "mu",
    "pn",
    "com.kw",
    "com.tj",
    "com.br",
    "com.gh",
    "com.om",
    "com.py",
    "ki",
    "iq",
    "fm",
    "td",
    "vg",
    "im",
    "me",
    "com.jm",
    "co.id",
    "co.ls",
    "sh",
    "com.np",
    "com.lb",
    "com.tw",
    "bt",
    "lk",
    "cm",
    "com.af",
    "dm",
    "pl",
    "mn",
    "com.sg",
    "sn",
    "com.ng",
    "com.bd",
    "com.gt",
    "kz",
    "mg",
    "ht",
    "com.bh",
    "com.pa",
    "ru",
    "st",
    "az",
    "co.uz",
    "hn",
    "com.na",
    "com.bn",
    "co.ma",
    "ne",
    "sk",
    "tl",
    "cg",
    "dj",
    "fr",
    "com.vc",
    "md",
    "bs",
}

match_bases = [
    "*://www.google.TLD/",
    "*://www.google.TLD/?*",
    "*://www.google.TLD/imghp*",
    "*://www.google.TLD/webhp*",
    "*://www.google.TLD/videohp*",
    "*://www.google.TLD/search*",
    "*://www.google.TLD/preferences*",
    "*://www.google.TLD/shopping*",
    "*://ogs.google.TLD/*",
    "*://images.google.TLD/*",
    "*://books.google.TLD/*",
    "*://scholar.google.TLD/*",
    "*://translate.google.TLD/*",
    "*://news.google.TLD/",
]

matches = [
    match_base.replace("TLD", tld)
    for tld in top_level_domains
    for match_base in match_bases
]
matches.append("*://drive.google.com/drive*")
GUID = "{000a8ba3-ef46-40fd-a51c-daf19e7c00e7}"  # Firefox
ITEM_ID = "ohhpliipfhicocldcakcgpbbcmkjkian"  # Chrome Web Store
addon_files = ["manifest.json", "style.css"] + glob("icons/*.png")
with open("style.css") as f:
    style = f.read()

# read environmental variables
with open(".env") as f:
    line = f.readline()
    while line:
        k, v = line.split("=", 1)
        os.environ[k] = v.strip()
        line = f.readline()


def is_ahead(repo):
    # if local repo/branch is ahead of origin
    return sum(1 for c in repo.iter_commits("origin/master..master"))


def create_zip(file):
    """file: filename or file-type object"""
    with ZipFile(file, "w") as zf:
        for file in addon_files:
            zf.write(file)


def upload_mozilla(file: io.BytesIO):
    # create auth JWT token
    jwt_secret = os.environ["jwt_secret"]
    jwt_issuer = os.environ["jwt_issuer"]
    jwt_obj = {
        "iss": jwt_issuer,
        "jti": str(uuid.uuid4()),
        "iat": time.time() - 100,
        "exp": time.time() + 60,
    }
    jwt_obj = jwt.encode(jwt_obj, jwt_secret, algorithm="HS256")

    data = {"upload": ("manifest.zip", file.getvalue()), "channel": "listed"}
    headers = {"Authorization": f"JWT {jwt_obj}"}
    url = f"https://addons.mozilla.org/api/v4/addons/{GUID}/versions/{version}/"
    r = requests.put(url, data, headers=headers, files=data)
    print(r.text)


def upload_chrome(file: io.BytesIO):
    client_id = os.environ["client_id"]
    data = {
        "client_id": client_id,
        "client_secret": os.environ["client_secret"],
        "grant_type": "refresh_token",
        "redirect_uri": "http://127.0.0.1:8080",
    }

    initial_request = (
        "refresh_token" not in os.environ or os.environ["refresh_token"] == "NONE"
    )
    try:
        r = requests.post(
            "https://accounts.google.com/o/oauth2/token",
            data={**data, "refresh_token": os.environ["refresh_token"]},
        ).json()
        access_token = r["access_token"]
    except KeyError:
        initial_request = True
    if initial_request:
        webbrowser.open(
            f"https://accounts.google.com/o/oauth2/auth?response_type=code&access_type=offline&scope=https://www.googleapis.com/auth/chromewebstore&client_id={client_id}&redirect_uri=http://127.0.0.1:8080"
        )
        data["code"] = input("Enter code: ")
        data["grant_type"] = "authorization_code"
        print(data)
        r = requests.post(
            "https://accounts.google.com/o/oauth2/token", data=data
        ).json()
        if "error" in r:
            print(r["error_description"])
            raise AssertionError(r["error"])
        access_token = r["access_token"]
        print("new refresh token:", r["refresh_token"])
    headers = {"Authorization": f"Bearer {access_token}", "x-goog-api-version": "2"}
    requests.put(
        f"https://www.googleapis.com/upload/chromewebstore/v1.1/items/{ITEM_ID}",
        headers=headers,
        data=file.getvalue(),
    )
    requests.post(
        f"https://www.googleapis.com/chromewebstore/v1.1/items/{ITEM_ID}/publish",
        headers=headers,
    )


def upload(version):
    # e.g. version = '1.1.1.1'
    print(f"uploading version {version}")
    file = io.BytesIO()
    create_zip(file)

    upload_mozilla(file)
    # upload_chrome(file)


if __name__ == "__main__":
    rmtree("builds", ignore_errors=True)
    os.makedirs("builds")

    with open("manifest.json") as f:
        manifest = json.load(f)

    manifest["content_scripts"][0]["matches"] = matches
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

    # versioning: year.month.day.builds
    repo = Repo(".git")
    origin = repo.remote(name="origin")
    commits_behind = len(list(repo.iter_commits("master..origin/master")))
    if commits_behind:
        # if origin has changes
        paths: Iterable[str] = filter(
            lambda x: x is not None, (item.a_path for item in repo.index.diff(None))
        )  # type: ignore
        commit_message = ", ".join(paths)
        repo.git.add(update=True)
        repo.index.commit(f"Updated {commit_message}")
        origin.pull()
    if is_ahead(repo) or repo.is_dirty():
        # if need to push or any changes were made
        date = datetime.today().strftime("%Y.%#m.%#d")
        changed_files = {item.a_path for item in repo.index.diff(None)}
        build_no = int(manifest["version"].split(".")[-1])
        if (
            "style.css" in changed_files
            or "manifest.json" in changed_files
            or "Icons/icon16.png" in changed_files
        ):
            # only update build if style.css, manifest.json, or icons have changed
            build_no += 1
        version = f"{date}.{build_no}"
        regex_com = "|".join(
            [tld.split("com.", 1)[1] for tld in top_level_domains if "com." in tld]
        )
        regex_co = "|".join(
            [tld.split("co.", 1)[1] for tld in top_level_domains if "co." in tld]
        )
        regex_other = "|".join(
            [tld for tld in top_level_domains if "com" not in tld and "co" not in tld]
        )
        style_regex = (
            r'@-moz-document regexp("https?://(www|scholar|translate|ogs)\\.google\\.((com(\\.('
            + regex_com
            + r"))?)|(co\\.("
            + regex_co
            + "))|("
            + regex_other
            + r'))/((webhp|videohp|imghp|search|\\?.*).*)?") {'
        )
        user_style = (
            "/* ==UserStyle==\n"
            + "@name Google Dark Theme\n"
            + f"@version {date}\n"
            + "@description A dark theme for Google (currently only supports searches).\n"
            + "@author Elijah Lopez\n"
            + "@namespace elibroftw\n"
            + "@homepageURL https://github.com/elibroftw/google-dark-theme\n"
            + "@supportURL https://github.com/elibroftw/google-dark-theme/issues/\n"
            + "@updateURL https://github.com/elibroftw/google-dark-theme/raw/master/style.user.css\n"
            + "@preprocessor stylus\n"
            + "==/UserStyle== */\n\n"
            + style_regex
            + f"\n\n{style}\n"
            + "}\n"
        )
        with open("style.user.css", "w") as f:
            user_style = user_style.replace(
                "alpha(opacity=25) invert()", "unquote('alpha(opacity=25) invert()')"
            )
            f.write(user_style)
        pyperclip.copy(user_style)
        manifest["version"] = version
        with open("manifest.json", "w") as fp:
            json.dump(manifest, fp, indent=4)
        if args.upload:
            changed_paths_for_commit = [
                item.a_path for item in repo.index.diff(None) if item.a_path is not None
            ]
            commit_message = ", ".join(changed_paths_for_commit)
            repo.git.add(update=True)
            repo.index.commit(f"Updated {commit_message}")
            origin = repo.remote(name="origin")
            origin.push()
    else:
        version = manifest["version"]

    name = manifest["short_name"]
    filename = f"{name} {version}.zip"
    create_zip(f"builds/{filename}")

    print(f"Build successful. Version: {version}\nTimestamp: {datetime.now().time()}")
    url_name = "dark-theme-for-google-searches"
    print("https://userstyles.org/styles/180957/edit")
    print(
        "https://chrome.google.com/webstore/devconsole/d9cb1dfc-39c3-47c1-83ca-1ec7b4652439/ohhpliipfhicocldcakcgpbbcmkjkian/edit/package"
    )
    if args.upload:
        upload(version)
    else:
        print(
            f"https://addons.mozilla.org/en-CA/developers/addon/{url_name}/versions/submit/"
        )
