import os
from argparse import ArgumentParser

try:
    import winreg as reg
except ImportError:
    import _winreg as reg


DEFAULT_CHROME_PATH = r'C:\Program Files'
CHROME_KEY = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
QUERY_AND_SET_RIGHTS = reg.KEY_QUERY_VALUE | reg.KEY_SET_VALUE
KEY_INFO = dict(
    key=reg.HKEY_LOCAL_MACHINE,
    sub_key=CHROME_KEY,
    access=QUERY_AND_SET_RIGHTS,
)


def patch(custom_path):
    with reg.OpenKeyEx(**KEY_INFO) as key:
        default_value, value_type = reg.QueryValueEx(key, '')
        if default_value.startswith(DEFAULT_CHROME_PATH):
            reg.SetValueEx(key, '', 0, value_type, custom_path)
            print('Custom Chrome App Path changed')
        else:
            print(default_value)


def is_valid(parser, file_path):
    if os.path.exists(file_path):
        return file_path
    else:
        parser.error(f'Invalid file path {file_path}')


def main():
    parser = ArgumentParser(description='Chrome Custom App Path')
    parser.add_argument(
        '-p',
        dest='custom_path',
        help='custom filename path to binary wrapper',
        required=True,
        type=lambda path: is_valid(parser, path),
    )
    args = parser.parse_args()

    try:
        patch(args.custom_path)
    except PermissionError:
        parser.exit(status=1, message='Run as Administrator\n')
    except FileNotFoundError:
        parser.exit(status=1, message='Chrome App Path key not found\n')


if __name__ == '__main__':
    exit(main())
