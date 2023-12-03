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
        if self.check_if_game_ended():
            return self.who_won()

    def check_if_game_ended(self):
        if len(self.impostor_list) == 0 or len(self.impostor_list) == len(self.crewmate_list) <= 3:
            return True

    def who_won(self):
        if len(self.impostor_list) == 0:
            self.game = False
            self.meeting = False
            self.crewmate_list = []
            self.dead_players = []
            self.impostor_list = []
            self.ejected_players = []
            self.votes = {}
            self.difficulty = ''
            self.is_anyone_protected = False
            return 'Crewmates won.'
        elif len(self.impostor_list) == len(self.crewmate_list) <= 3:
            self.game = False
            self.meeting = False
            self.crewmate_list = []
            self.dead_players = []
            self.impostor_list = []
            self.ejected_players = []
            self.votes = {}
            self.difficulty = ''
            self.is_anyone_protected = False
            return "Impostors won."

    def start_game(self):
        if len(self.impostor_list) >= 1 and len(self.crewmate_list) >= 2 and len(self.crewmate_list) > len(self.impostor_list):
            self.game = True

    def report_dead_body(self, reporting_player, dead_body):
        if reporting_player not in self.dead_players and dead_body in self.dead_players and self.game:
            self.meeting = True
            self.dead_players.remove(dead_body)

    def cast_vote(self, player, target):
        if player.name not in self.votes and self.meeting and (target in self.crewmate_list or target in self.impostor_list) and self.game:
            self.votes[player.name] = target.name

    def end_meeting(self):
        pass





    def get_vote(self, color: str):
        for name in self.votes:
            if name == color.capitalize():
                return self.votes[name]
        return 'No vote found'

    def get_ejected_players(self):
        return self.ejected_players

    def get_votes(self):
        return self.votes

    def is_meeting(self):
        return self.meeting


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
    print(spaceship.kill_crewmate(black, 'blue'))
    print(spaceship.report_dead_body(black, blue))
    print(spaceship.meeting)
    print(spaceship.crewmate_list)
    print(spaceship.impostor_list)
    spaceship.cast_vote(red, red)
    print(spaceship.get_vote('red'))
    print(spaceship.votes)
    # print(spaceship.kill_crewmate(black, 'red'))

    # print(blue in spaceship.dead_players)
    # print(spaceship.kill_impostor(red, 'black'))

