import json
import re

import telebot
from telebot import types


token = open('src/token.txt', 'r').read()
bot = telebot.TeleBot(token)


def find_name(message):
    pkmn = re.sub('/data ', '', message.text)
    pkmn = re.sub('♀', '-f', pkmn)  # For Nidoran♀
    pkmn = re.sub('♂', '-m', pkmn)  # For Nidoran♂
    pkmn = re.sub('[èé]', 'e', pkmn)  # For Flabébé
    pkmn = re.sub(' ', '-', pkmn)
    pkmn = re.sub('[^A-Za-z-]', '', pkmn)
    return pkmn


def set_message(pkmn_data):
    base_text = '''<b>{}</b>\n
National: {}
Type(s): {}
Ability(ies): {}\n
Base stats:
{}
'''
    name = pkmn_data['name']
    national = pkmn_data['national']
    typee = ''
    for i in pkmn_data['type'].values():
        typee += '/' + i
    typee = typee[1:]
    ability = ''
    for i, j in pkmn_data['abilities'].items():
        if i == 'hidden_ability':
            ability += '\n' + 'Hidden Ability: ' + j
        else:
            ability += '/' + j
    ability = ability[1:]
    base_stats = ''
    stats = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']
    for base, minn, maxx, stat in zip(
        pkmn_data['base_stats'].values(),
        pkmn_data['base_stats'].values(),
        pkmn_data['base_stats'].values(),
        stats
    ):
        base_stats += stat + ': ' + base + ' (' + minn + '-' + maxx + ')\n'
    text = base_text.format(
        name,
        national,
        typee,
        ability,
        base_stats,
    )
    return text


@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    bot.send_message(cid, 'Hello Trainer!')


@bot.message_handler(commands=['data'])
def pkmn_search(message):
    cid = message.chat.id
    pkmn = find_name(message)

    with open('dist/pkmn.json', 'r') as f:
        data = json.load(f)
    if pkmn in data:
        pkmn_data = data[pkmn]
    else:
        bot.send_message(cid, 'Pokémon not found :(')
        return None

    text = set_message(pkmn_data)
    bot.send_message(cid, text, parse_mode='HTML')


bot.polling(none_stop=True)
