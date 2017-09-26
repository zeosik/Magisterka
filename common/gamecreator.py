from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.placepicker.placepicker import PlacePicker
from common.model.places.cardline import FaceUpCardLine
from common.model.places.place import Place
from common.model.playerchooser.currentplayerchooser import CurrentPlayerChooser
from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.playerchooser.tableplayerchooser import TablePlayerChooser
from common.model.playertype import PlayerType
from common.model.rules.changephase import ChangePhase


class TypeCreator:

    def __init__(self, model: GameModel, type: PlayerType):
        self.model = model
        self.type = type

    def add_phase(self, name) -> Phase:
        phase = Phase(name)
        self.type.add_phase(phase)
        return phase

    def add_start_phase(self, name) -> Phase:
        ret = self.add_phase(name)
        self.model.start_phase = ret
        return ret

    def add_end_phase(self, name) -> Phase:
        ret = self.add_phase(name)
        self.model.end_phase = ret
        return ret

    def add_place(self, name) -> (Place, PlacePicker):
        place = FaceUpCardLine(name)
        self.type.add_place(place)
        place_picker = PlacePicker(CurrentPlayerChooser(self.type), place)
        return place, place_picker

class GameCreator:

    def __init__(self, name):
        self.model = GameModel(name)

    def add_player_type(self, name) -> (PlayerType, PlayerChooser, TypeCreator):
        type = PlayerType(name)
        self.model.add_player_type(type)
        type_picker = CurrentPlayerChooser(type)
        type_creator = TypeCreator(self.model, type)
        return type, type_picker, type_creator

    def add_table_type(self, name = "Table type") -> (PlayerType, PlayerChooser, TypeCreator):
        type = PlayerType(name)
        self.model.add_table_type(type)
        type_picker = TablePlayerChooser()
        type_creator = TypeCreator(self.model, type)
        return type, type_picker, type_creator

