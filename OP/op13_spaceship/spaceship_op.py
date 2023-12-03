"""OP13."""
from collections import Counter

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
        self.players = []

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

    def cast_vote(self, player, target_name):
        target = next((target for target in (self.crewmate_list + self.impostor_list) if target.name == target_name.capitalize()), None)
        if self.meeting and player not in self.dead_players and player.name not in self.votes and target and self.game:
            self.votes[player.name] = target.name

    def end_meeting(self):
        if self.meeting:
            vote_counts = Counter(self.votes.values())
            max_votes = max(vote_counts.values(), default=0)
            if max_votes == 0:
                self.meeting = False
                return "No one was ejected. (Skipped)"

    def get_vote(self, color: str):
        if color.capitalize() in self.votes:
            return self.votes[color.capitalize()]
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
    green = Crewmate('green', 'crewmate')
    pink = Crewmate("pink", 'Crewmate')
    purple = Crewmate("purple", 'Sheriff')
    dunk = Crewmate("dunk", 'Crewmate')
    yellow = Crewmate('yellow', 'crewmate')
    black = Impostor("black")

    spaceship = OPSpaceship('easy')
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(black)
    # spaceship.add_crewmate(green)
    # spaceship.add_crewmate(pink)
    # spaceship.add_crewmate(purple)
    # spaceship.add_crewmate(dunk)
    # spaceship.add_crewmate(yellow)

    print(spaceship.get_crewmate_list())
    print(spaceship.get_impostor_list())

    spaceship.start_game()
    spaceship.kill_crewmate(black, 'orange')
    # print(yellow in spaceship.dead_players)
    spaceship.report_dead_body(black, orange)
    spaceship.cast_vote(black, 'red')
    spaceship.cast_vote(blue, 'red')
    # spaceship.cast_vote(pink, 'black')
    # spaceship.cast_vote(blue, 'black')
    # spaceship.cast_vote(red, 'black')
    # spaceship.cast_vote(dunk, 'red')
    # spaceship.cast_vote(green, 'red')
    # spaceship.cast_vote(purple, 'red')

    print(spaceship.get_votes())

    print(spaceship.end_meeting())

