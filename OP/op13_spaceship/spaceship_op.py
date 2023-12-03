"""OP13."""
from spaceship import Spaceship
from spaceship import Impostor
from spaceship import Crewmate


class OPSpaceship(Spaceship):
    """Class spaceship for op task."""

    def __init__(self, difficulty):
        super().__init__()
        self.difficulty = difficulty.lower() if difficulty.lower() == 'easy' else 'hard'
        self.ejected_players = []
        self.meeting = False
        self.votes = {}
        self.game = False

    def add_crewmate(self, crewmate):
        if not self.game:
            super().add_crewmate(crewmate)

    def add_impostor(self, impostor):
        if not self.game:
            super().add_impostor(impostor)

    def kill_crewmate(self, killer, target_name):
        if self.game and not self.meeting:
            super().kill_crewmate(killer, target_name)
        if self.check_if_game_ended():
            return self.who_won()

    def kill_impostor(self, killer, target_name):
        if self.game and not self.meeting:
            super().kill_impostor(killer, target_name)
        self.check_if_game_ended()

    def check_if_game_ended(self):
        if len(self.impostor_list) == 0 or len(self.impostor_list) == len(self.crewmate_list) <= 3:
            self.game = False
            return True

    def who_won(self):
        if len(self.impostor_list) == 0:
            return 'Crewmates won.'
        elif len(self.impostor_list) == len(self.crewmate_list) <= 3:
            return "Impostors won."


    def start_game(self):
        if len(self.impostor_list) >= 1 and len(self.crewmate_list) >= 2 and len(self.crewmate_list) > len(self.impostor_list):
            self.game = True



if __name__ == "__main__":
    orange = Crewmate("orange", 'Crewmate')
    red = Crewmate("red", 'Sheriff')
    blue = Crewmate("blue", 'Crewmate')
    black = Impostor("black")

    spaceship = OPSpaceship('easy')
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(black)

    print(spaceship.get_crewmate_list())
    print(spaceship.get_impostor_list())

    spaceship.start_game()
    spaceship.kill_crewmate(black, 'blue')
    print(blue in spaceship.dead_players)
    spaceship.kill_impostor(red, 'black')
    green = Crewmate("green", "Guardian angel")

