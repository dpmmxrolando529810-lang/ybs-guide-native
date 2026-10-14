#!/usr/bin/env python3
"""Fetch a checked Source ZIP from this repo's prerelease for phone-only setup."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import zipfile

MAX_TOTAL = 512 * 1024 * 1024
MAX_FILE = 128 * 1024 * 1024


def extract_checked(archive, destination, digest):
    with archive.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if digest != 'sha256:' + actual:
        raise ValueError('Source ZIP does not match the GitHub release asset digest')
    with zipfile.ZipFile(archive) as package:
        entries = package.infolist()
        if len(entries) > 20000 or sum(e.file_size for e in entries) > MAX_TOTAL:
            raise ValueError('Source ZIP exceeds the build limits')
        names = [e.filename for e in entries]
        if len(names) != len(set(names)):
            raise ValueError('Source ZIP contains duplicate paths')
        for entry in entries:
            name = PurePosixPath(entry.filename)
            if (name.is_absolute() or str(name) != entry.filename or entry.is_dir() or
                    '..' in name.parts or '\\' in entry.filename or
                    not name.parts or name.parts[0] != 'ybs-guide-native' or
                    'signing' in name.parts or 'tools' in name.parts or
                    stat.S_ISLNK(entry.external_attr >> 16) or entry.file_size > MAX_FILE):
                raise ValueError('Source ZIP contains an unsafe or private path')
        index = 'ybs-guide-native/SOURCE-SHA256.json'
        manifest = json.loads(package.read(index))
        if not isinstance(manifest, dict):
            raise ValueError('Source ZIP integrity manifest is invalid')
        expected = {'ybs-guide-native/' + path for path in manifest} | {index}
        if set(names) != expected:
            raise ValueError('Source ZIP file list differs from its integrity manifest')
        # Validate every entry before writing executable build sources.
        for path, sha in manifest.items():
            if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{64}', sha):
                raise ValueError('Source entry has an invalid checksum')
            if hashlib.sha256(package.read('ybs-guide-native/' + path)).hexdigest() != sha:
                raise ValueError('Source entry checksum failed')
        if destination.exists():
            raise ValueError('Use a fresh source extraction directory')
        destination.mkdir(parents=True)
        package.extractall(destination)
    root = destination / 'ybs-guide-native'
    for required in ['scripts/publish_github_release.py', 'app/build.gradle', 'gradlew', 'gradle/wrapper/gradle-wrapper.jar']:
        if not (root / required).is_file():
            raise ValueError('Source is missing the native publisher/build files')
    return root.resolve()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--release-tag', required=True)
    parser.add_argument('--asset-name', required=True)
    arguments = parser.parse_args()
    repository = os.environ.get('GITHUB_REPOSITORY', '')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', repository):
        parser.error('Use the actual GitHub Actions repository')
    if not re.fullmatch(r'source-v[0-9]+\.[0-9]+\.[0-9]+', arguments.release_tag):
        parser.error('Source tag must look like source-v1.0.11')
    if not re.fullmatch(r'YBS-Guide-Source-v[0-9]+\.[0-9]+\.[0-9]+\.zip', arguments.asset_name):
        parser.error('Select the exact YBS Source ZIP filename')
    result = subprocess.run(['gh', 'api', f'repos/{repository}/releases/tags/{arguments.release_tag}'],
                            capture_output=True, text=True, check=True)
    release = json.loads(result.stdout)
    if release.get('draft') or release.get('prerelease') is not True:
        parser.error('Publish the Source ZIP as a prerelease, so it never replaces the app update feed')
    assets = [a for a in release.get('assets', []) if a.get('name') == arguments.asset_name]
    if len(assets) != 1 or not re.fullmatch(r'sha256:[0-9a-f]{64}', assets[0].get('digest') or ''):
        parser.error('Source ZIP is missing, duplicated or lacks its GitHub upload digest')
    work = Path(tempfile.mkdtemp(prefix='ybs-source-', dir=os.environ.get('RUNNER_TEMP')))
    subprocess.run(['gh', 'release', 'download', arguments.release_tag, '--repo', repository,
                    '--pattern', arguments.asset_name, '--dir', str(work)], check=True)
    archive = work / arguments.asset_name
    if not archive.is_file() or archive.stat().st_size != assets[0].get('size'):
        parser.error('Downloaded Source ZIP size does not match its release asset')
    root = extract_checked(archive, work / 'extracted', assets[0]['digest'])
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
        output.write('directory=' + str(root) + '\n')
    print('Verified Source ZIP and all source-file checksums; native build source is ready.')


if __name__ == '__main__':
    main()
