import random

from flask import Flask, request, render_template, flash, redirect, url_for, abort
from forms import CardForm, RequirementsForm
import os
from random import choice

# config
DEBUG = True
SECRET_KEY = 'cat'

app = Flask(__name__)
app.config.from_object(__name__)

menu = [{'name': 'Главная', 'url': '/'},
        {'name': 'Правила', 'url': '/rules'},
        {'name': 'Играть', 'url': '/game'},
        {'name': 'Карты', 'url': '/select-card'},
        {'name': 'Требования', 'url': '/requirements'}]
all_the_cards = {"6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Валет": 2, "Дама": 3, "Король": 4, "Туз": 11}
player_cards, bot_cards, score, win = [], [], [0, 0], ''


@app.route('/')
def index():
    return render_template('index.html', title='Главная', menu=menu)


@app.route('/rules')
def rules():
    return render_template('rules.html', title='Правила', menu=menu)


@app.route('/game', methods=['POST', 'GET'])
def game():
    global player_cards, bot_cards, score, win
    if request.method == 'POST':
        if request.form['index'] == 'start_the_game':
            # игроки берут по 2 карты, в html передаётся лист, там считается сумма листа
            player_cards.append(choice(list(all_the_cards)))
            player_cards.append(choice(list(all_the_cards)))
            bot_cards.append(choice(list(all_the_cards)))
            bot_cards.append(choice(list(all_the_cards)))
            score[0] = sum(all_the_cards[i] for i in player_cards)
            score[1] = sum(all_the_cards[i] for i in bot_cards)
        elif request.form['index'] == 'take_a_card':
            player_cards.append(choice(list(all_the_cards)))
            bot_cards.append(choice(list(all_the_cards)))
            score[0] = sum(all_the_cards[i] for i in player_cards)
            score[1] = sum(all_the_cards[i] for i in bot_cards)
        elif request.form['index'] == 'end_the_game':
            if score[0] == score[1]:
                win = 'd'
            elif (score[0] <= 21 and (score[0] > score[1])) or (
                    (score[0] > 21 or score[1] > 21) and (score[0] < score[1])):
                win = 'w'
            else:
                win = 'l'
            if len(player_cards) == 2 and (score[0] == 22 or score[1] == 22):
                if score[0] == 22:
                    win = 'w'
                elif score[1] == 2:
                    win = 'l'
        else:
            player_cards, bot_cards, score = [], [], [0, 0]
            win = ''
    return render_template('game.html', menu=menu, player_cards=player_cards, bot_cards=bot_cards, score=score, win=win)


@app.route('/select-card/', methods=['POST', 'GET'])
def select_card():
    form = CardForm()
    card = ''
    if form.validate_on_submit() and request.method == 'POST':
        card = request.form['card']
    return render_template('select_card.html', title="Карты", form=form, card=card, menu=menu, all_the_cards=all_the_cards)


@app.route('/cards/<string:value>')
def cards(value):
    p = os.getcwd() + r'\static\img\cards'
    if value + '.png' in os.listdir(p):
        return redirect(url_for('static', filename='img/cards/' + value + '.png'))
    return abort(404)


@app.route('/requirements', methods=['GET', 'POST'])
def requirements():
    form = RequirementsForm()
    if form.validate_on_submit():
        flash('Ура, поля совпадают!')
    return render_template('requirements.html', title="Требования", menu=menu, form=form)


if __name__ == '__main__':
    app.run()
