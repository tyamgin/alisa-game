# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

SONGS = [
"""
Кошка сдохла, хвост облез.
Кто промолвит, тот и съест!
""",
"""
Чок, чок, чок,
Зубы на крючок,
Кто слово скажет,
Тому в лоб щелчок!
""",
"""
Шел Молчан
По крутым горам.
Кто не молчал -
Того за уши драл!
"""
]

class Dialog:
    def __init__(self, id):
        self.id = id
        self.repIdx = 1
        self.gameStarted = False
        self.losesCount = 0

    def process(self, req, res):
        self.req = req


        if self.repIdx == 1:
            res['response']['text'] = 'Привет! Правила игры очень просты. Кто первый произнесёт хоть одно слово, тот проиграл. Начнём?'
            res['response']['buttons'] = [{
                "title": "Да",
                "hide": True
            }]
        elif not self.gameStarted:
            if self.saysYes():
                res['response']['text'] = self.selectSong()
                self.gameStarted = True
            else:
                res['response']['text'] = 'Напомню правила игры. Кто первый произнесёт слово, тот проиграл. Скажите, когда будете готовы.'
                res['response']['buttons'] = [{
                    "title": "Готов",
                    "hide": True
                }]
        else:
            res['response']['text'] = self.loseMessage()
            res['response']['buttons'] = [{
                "title": "Давай",
                "hide": True
            }]
            self.losesCount += 1
            self.gameStarted = False

        self.repIdx += 1

    def saysYes(self):
        msg = self.req['request']['original_utterance'].lower().replace('ё', 'е')
        return msg in ['готов', 'да', 'давай', 'начнем', 'поехали']

    def selectSong(self):
        return SONGS[self.losesCount % len(SONGS)]

    def loseMessage(self):
        if self.losesCount == 0:
            return 'Ха-ха-ха. Вы проиграли. Сыграем ещё разок?'
        if self.losesCount == 1:
            return 'А Вы не умеете держать язык за зубами. Попробуем ещё раз?'
        return 'Опять проигрыш. Ещё раз?'