from random import choice

art = [
"""
[c].--'''''''''--.
[c].'     .---.    '.
[c]/  .-----------.  \\
[c]/       .-----.        \\
[c]|        .-.   .-.        |
[c]|      /   \ /   \      |
[c]\    | .-. | .-. |    /
[c]`-.| |  || |  | |.-´
[c]| '-' |  '-' |
[c]\_/ \__/
[c]_.-'  /   \  '-._
[c].' _.--|     |--._ '.
[c]' _...-|     |-..._ '
[c]|     |
[c]'.__.'
""",
"""
[c] .-----.
[c] .´  -   -  `.
[c] /   .-. .-.   \\
[c]  |  |    ||    |   |
[c] \ \o/ \o/ /
[c] _/     ^     \_
[c] |  \  '---'  /  |
[c] /  /`--. .--`\  \\
[c]/   /'---' '---'\   \\
[c]'.__.       .__.'
[c] `|     |`
[c] |      \\
[c]      \       '--.
[c]        '.        `\\
[c]           `'---.   |
[c]                ) /
[c]              \/
"""
]

# Helper 'help' function
def help(data):
    result = f'{choice(art)}\n[BC]Antibot skills\n\n'
    skillList = [
        f"- ${skill}: {skills[skill]['desc']}" for skill in skills
    ]
    result += '\n'.join(sorted(skillList))
    result += '\n\n[I]The skill names are case-insensitive.'
    return {'message': result}

# Basic skills
skills = {
    'bye': {
        'desc': 'Says bye.',
        'run': lambda x: {'message': 'See you later, alligator.'}
    },
    'hi': {
        'desc': 'Says hi.',
        'run': lambda x: {'message': 'Hi.'}
    },
    'help': {
        'desc': 'Shows this help message.',
        'run': help
    }
}
