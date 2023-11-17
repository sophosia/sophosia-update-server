from flask import Flask
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

GITHUB_RELEASE_URL = f'https://api.github.com/repos/sophosia/sophosia/releases/latest'

PLATFORMS = [ # platform, extension
    (('linux-x86_64',), 'amd64.AppImage.tar.gz'),
    (('darwin-x86_64', 'darwin-aarch64'), 'app.tar.gz'),
    (('windows-x86_64',), 'x64_en-US.msi.zip'),
]


def get_latest_gh_release() -> dict:
    """
        repo: username/project-name
        Return format:
        Note darwin-aarch64 is silicon macOS. Supposed to seperate file but assumed that x64 would work due to Rosetta Stone 2
        {
          "version": "v0.1.0",  (can be any string)
          "notes": "- Test updater",
          "pub_date": "2022-11-13T03:20:32Z",
          "platforms": {
            "linux-x86_64": {
              "url": "https://github.com/sophosia/sophosia/releases/download/v0.1.0/sophosia_0.1.0_amd64.AppImage.tar.gz",
              "signature": "content of .sig file"
            },
            "darwin-x86_64": {
              "url": "https://github.com/sophosia/sophosia/releases/download/v0.1.0/sophosia_x64.app.tar.gz",
              "signature": "content of .sig file"
            },
            "darwin-aarch64": {
              "url": "https://github.com/sophosia/sophosia/releases/download/v0.1.0/sophosia_x64.app.tar.gz",
              "signature": "content of .sig file"
            },
            "windows-x86_64": {
              "url": "https://github.com/elibroftw/google-keep-desktop-app/releases/download/v1.0.8/sophosia_0.1.0_x64_en-US.msi.zip",
              "signature": "content of .sig file"
            }
          }
        }
    """
    try:
        release = requests.get(GITHUB_RELEASE_URL).json()
    except requests.RequestException:
        return {}
    release_response = {
        'version': release['tag_name'],
        'notes': release['body'].rstrip('\r\n '),
        'pub_date': release['published_at'],
        'platforms': {}
        }
    for asset in release.get('assets', []):
        for for_platforms, extension in PLATFORMS:
            if asset['name'].endswith(extension):
                for platform in for_platforms:
                    release_response['platforms'][platform] = {**release_response['platforms'].get(platform, {}), 'url': asset['browser_download_url']}
            elif asset['name'].endswith(f'{extension}.sig'):
                try:
                    sig = requests.get(asset['browser_download_url']).text
                except requests.RequestException:
                    sig = ''
                for platform in for_platforms:
                    release_response['platforms'][platform] = {**release_response['platforms'].get(platform, {}), 'signature': sig}
    return release_response

class UpdateInfo(Resource):
    def get(self, platform: str, current_version: str):
        latest_release = get_latest_gh_release()
        if not latest_release:
            return '', 204
        try:
            # version checks
            latest_version = latest_release['version']
            latest_maj, latest_min, latest_patch = latest_version.lstrip('v').split('.')
            cur_maj, cur_min, cur_patch = current_version.lstrip('v').split('.')
            if cur_maj == latest_maj and cur_min == latest_min and cur_patch == latest_patch:
                raise ValueError
        except ValueError:
            return '', 204
        return latest_release

api.add_resource(UpdateInfo, "/<platform>/<current_version>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
