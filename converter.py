# -*- coding: utf-8 -*-
import json

# https://github.com/Cockatrice/Cockatrice/wiki/Custom-Cards-&-Sets

# globals
tablerow = {"Follower": 2, "Spell": 3, "Amulet": 1}
# 1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
# 2 → creatures
# 3 → non-permanent cards (like Instants and Sorceries)
sets = {"Token": ("TK", "1970-01-01"),
        "Basic": ("Basic", "2016-06-21"),
        "Standard Card Pack": ("STD", "2016-06-21"),
        "Darkness Evolved": ("DE", "2016-09-29"),
        "Rise of Bahamut": ("ROB", "2016-12-29"),
        "Tempest of the Gods": ("TOTG", "2017-03-30"),
        "Wonderland Dreams": ("WLD", "2017-06-29"),
        "Starforged Legends": ("SL", "2017-09-28"),
        "Chronogenesis": ("CG", "2017-12-28"),
        "Dawnbreak Nightedge": ("DN", "2018-03-28"),
        "Granblue Fantasy": ("BOTS", "2018-06-27"),
        "Omen of the Ten": ("OOT", "2018-09-26"),
        "Altersphere": ("AS", "2018-12-26"),
        "Steel Rebellion": ("SR", "2019-03-27"),
        "Rebirth of Glory": ("ROG", "2019-06-27"),
        "Verdant Conflict": ("VC", "2019-09-25"),
        "Ultimate Colosseum": ("UC", "2019-12-27"),
        "World Uprooted": ("WU", "2020-03-29"),
        "Fate's Hand": ("FH", "2020-06-29")}
modesty_string = "<<{me.inplay.class.count}+1??<br>(Artifacts destroyed: \
<<{me.destroyed_card_list.tribe=artifact.unique_base_card_id_card.count}>>)>>"
shiva_string = "<<{me.inplay.class.count}+1??<br>(Current turn: )>>"
with open("en.json", 'r') as f:
    data = json.load(f)
# end globals
c = open("sv_cards.xml", 'w+')
t = open("sv_tokens.xml", 'w+')

c.write('''<?xml version="1.0" encoding="UTF-8"?>\n
        <cockatrice_carddatabase version="4">\n
        <sets>\n''')
t.write('''<?xml version="1.0" encoding="UTF-8"?>\n
            <cockatrice_carddatabase version="4">\n
            <cards>\n''')
for s in sets:
    c.write('\t<set>\n')
    c.write(f'\t\t<name>{sets[s][0]}</name>\n')
    c.write(f'\t\t<longname>{s}</longname>\n')
    c.write('\t\t<settype>Custom</settype>\n')
    c.write(f'\t\t<releasedate>{sets[s][1]}</releasedate>')
    c.write('\t</set>\n')
c.write('</sets>\n<cards>\n')


def clean(txt):
    try:
        return txt.replace(modesty_string, '').replace(shiva_string, '') \
            .replace('Ofcr.', "Officer").replace('Cmdr.', "Commander") \
            .replace('Nat.', 'Natura').replace('Mach.', 'Machina') \
            .replace(' /', '').replace('<br>', '\n').replace('&', 'and')
    except AttributeError:
        return txt


for i in list(data):
    card = data[i]


    def xml(field, val):
        try:
            return clean(f'\t\t<{field}>{card[val]}</{field}>\n')
        except KeyError:
            return clean(f'\t\t<{field}>{val}</{field}>\n')


    def __debug_check_attrs():
        gob = data["Robogoblin"]
        [print(f'{k} -> {gob[k]}') for k in list(gob)]


    # if card["name"] == "Robogoblin":
    #   __debug_check_attrs()

    out = ['\t<card>\n',
           xml('name', 'name'),
           xml('text', card["baseData"]["description"]),
           '\t\t<prop>\n',
           '\t' + xml('layout', 'normal'),
           '\t' + xml('side', 'front'),
           '\t' + xml('type', f'{clean(card["race"])} {card["type"]}'),
           '\t' + xml('maintype', 'type'),
           '\t' + xml('manacost', 'manaCost'),
           '\t' + xml('cmc', 'manaCost'),
           '\t' + xml('colors', 'faction'),
           '\t' + xml('coloridentity', 'faction'),
           '\t' + xml('pt', f'{card["baseData"]["attack"]}/{card["baseData"]["defense"]}'),
           '\t' + xml('format-standard', 'legal' if card["rot"] == "Rotation" else "banned"),
           '\t\t</prop>\n',
           f'\t\t<set rarity="{card["rarity"]}" uuid="{card["id"]}" num="{card["id"]}" '
           f'muid="{card["id"]}" picurl="https://sv.bagoum.com/cardF/en/c/{card["id"]}">'
           f'{sets[card["expansion"]][0]}</set>\n']
    for j in data:
        if data[j]["name"][:-1] in card["baseData"]["description"]:
            out.append(xml('related', data[j]["name"]))
    if card["type"] == "Follower":
        out.append(f'<related attach="1">{clean(card["name"]) + " Evolved"}</related>')
    out.append(xml('token', '1' if card["expansion"] == "Token" else '0'))
    out.append(xml('tablerow', tablerow[card['type']]))
    out.append('</card>\n')
    if card["expansion"] == 'Token':
        for i in range(len(out)):
            t.write(out[i])
    else:
        for i in range(len(out)):
            c.write(out[i])
        if card["type"] == "Follower":
            out[1] = xml('name', card["name"] + " Evolved")
            out[2] = xml('text', card["evoData"]["description"])
            out[5] = out[5].replace('front', 'back')
            out[12] = xml('pt', f'{card["evoData"]["attack"]}/{card["evoData"]["defense"]}')
            out[15] = f'\t\t<set rarity="{card["rarity"]}" uuid="{card["id"]}" num="{card["id"]}" muid="{card["id"]}"' \
                      f' picurl="https://sv.bagoum.com/cardF/en/e/{card["id"]}">TK</set>\n'
            for idx, line in enumerate(out):
                if "Evolved</related>" in line:
                    out.pop(idx)
                if "<token>" in line:
                    out[idx] = xml('token', '1')
            for i in range(len(out)):
                t.write(out[i])

c.write('</cards>\n</cockatrice_carddatabase>')
t.write('</cards>\n</cockatrice_carddatabase>')
c.close()
t.close()
