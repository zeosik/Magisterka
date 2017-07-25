from typing import Tuple

import logging

from simulator.gamestate import GameState


class PlayerInput:

    def __init__(self, name):
        self.log = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.choices = None
        self.required = []

    #wszystkie mozliwe wybory
    def all_choices(self, gamestate: GameState) -> list:
        return []

    #inne PlayerInput ktore sa potrzebne do obsluzenia tego
    #np najpierw wybieramy gracza a potem jego stos a nastepnie karty ze stosu
    def required_inputs(self):
        return self.required

    def append_required_inputs(self, other): #other: PlayerInput
        self.required += other.required_inputs()
        self.required.append(other)


    #Jeżeli nie chcemy pytać gracza o wartości musimy je udostępnic tutaj
    # czasami nie chcemy aby gracz cos wybieral bo zawsze jest takie samo
    def auto_submitted_values(self, gamestate: GameState) -> list:
        pass

    #Czy wymagamy czegos od gracza
    def requires_player_input(self, gamestate: GameState) -> bool:
        values = self.auto_submitted_values(gamestate)
        auto_submitted = values is not None and self.submit_choices(values)
        return not auto_submitted

    #walidujemy to co wybiera gracz
    #True jezeli mu sie udalo
    #False i Komunikat jezeli mu sie nie udalo
    def submit_choices(self, choices: list) -> Tuple[bool, str]:
        self.choices = choices
        return True, ''

    #zwracamy ostatnio wybrane wartosci w celu wykonania reguly
    def submitted_choice(self) -> list:
        return self.choices

    #pojedyncza ostatnio wybrana wartosc
    def submitted(self):
        submitted = self.submitted_choice()
        if len(submitted) == 1:
            return submitted[0]
        self.log.error('submitted is not a single value: {0}'.format(submitted))
        raise Exception()
