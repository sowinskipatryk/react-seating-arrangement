import asyncio
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

REFRESH_RATE = 5  # in seconds
RUNTIME = 1  # in minutes

guests = [
  "Kasia Zdunek","Patryk Sowiński",
  "Małgorzata Zdunek","Sławomir Zdunek",
  "Małgorzata Sowińska","Krzysztof Sowiński",
  "Józefa Zdunek",
  "Mirosław Zdunek",
  "Małgorzata Zdunek","Krzysztof Zdunek",
  "Joanna Zdunek","Jarosław Dąbrowski",
  "Magdalena Zdunek","Oskar Szuprytowski",
  "Cezary Zdunek",
  "Maria Wiklandt","Adam Wiklandt",
  "Estera Wiklandt","Wiesław Wiklandt",
  "Weronika Hein","Maciej Wiklandt",
  "Barbara Dubiel","Andrzej Dubiel",
  "Paulina Dubiel","Łukasz Dubiel",
  "Magdalena Wesołowska","Daniel Wesołowski",
  "Agnieszka Kozłowska","Radosław Kozłowski",
  "Joanna Dubiel","Marcin Kawczyński",
  "Paulina Sowińska","Michał Rychert",
  "Wojciech Krawczyk","Ruslana Shvorak",
  "Natalia Krawczyk",
  "Weronika Krawczyk","Hubert Gorlewski",
  "Wiesław Sowiński",
  "Mirosława Sowińska",
  "Aneta Konopka","Maciej Konopka",
  "Aleksandra Piwowarczyk","Bartłomiej Sowiński",
  "Joanna Sowińska","Łukasz Sowiński",
  "Teresa Sowińska","Zdzisław Sowiński",
  "Magdalena Mazur","Damian Mazur",
  "Karolina Sowińska","Damian Danielewicz",
  "Anna Jach","Andrzej Jach",
  "Aleksandra Szybalska","Łukasz Tański",
  "Weronika Wojtala",
  "Bartłomiej Wenta",
  "Sandra Piór","Kamil Piór",
  "Agnieszka Wysocka","Jacek Żak",
  "Martyna Wyszyńska","Rafał Gawędzki",
  "Małgorzata Jajeśniak","Jakub Kędziora",
  "Paula Banasik","Łukasz Reszetow",
  "Sandra Drozdowska","Karol Wrzeszcz",
  "Sylwia Lisak","Mateusz Matuła",
  "Sebastian Firlej",
  "Zofia Wykrzykowska","Bartosz Tymiński",
  "Krzysztof Hajduk",
  "Maria Świerżewska","Rafał Sitkiewicz",
  "Natalia Głaz","Oskar Głaz",
  "Anna Vygovska","Wiktor Wieliczko",
  "Ewelina Wilanowska","Joao Lima",
  "Mateusz Lademann",
  "Szymon Szulc",
  "Julia Tkacz","Krzysztof Gapanowicz",
  "Aneta Rogaczewska","Paweł Biniarz",
  ]

class CalculationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        if text_data == 'start calculation':
            for i in range(RUNTIME * 60 // REFRESH_RATE):
                random.shuffle(guests)
                result = {'probabilities': [round(random.random(), 2) for _ in range(98)], 'guests': guests}
                await self.send(json.dumps(result))
                # result = [round(random.random(), 2) for _ in range(98)]
                # await self.send(json.dumps(result))
                await asyncio.sleep(REFRESH_RATE)
