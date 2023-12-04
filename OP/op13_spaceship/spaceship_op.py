"""OP13."""
from collections import Counter

from spaceship import Spaceship
from spaceship import Impostor
from spaceship import Crewmate


class OPSpaceship(Spaceship):
    """Class spaceship for op task."""

    def __init__(self, difficulty):
        """Init constructor."""
        super().__init__()
        self.difficulty = difficulty.lower() if difficulty.lower() == 'easy' else 'hard'
        self.ejected_players = []
        self.meeting = False
        self.votes = {}
        self.game = False

    def add_crewmate(self, crewmate):
        """Add new crewmate."""
        if not self.game:
            super().add_crewmate(crewmate)

    def add_impostor(self, impostor):
        """Add new impostor."""
        if not self.game:
            super().add_impostor(impostor)

    def kill_crewmate(self, killer, target_name):
        """Kill crewmate."""
        if self.game and not self.meeting:
            super().kill_crewmate(killer, target_name)
        if self.check_if_game_ended():
            return self.who_won()

    def kill_impostor(self, killer, target_name):
        """Kill impostor."""
        if self.game and not self.meeting:
            super().kill_impostor(killer, target_name)
        if self.check_if_game_ended():
            return self.who_won()

    def check_if_game_ended(self):
        """Check if game has ended."""
        if len(self.impostor_list) == 0 or len(self.impostor_list) == len(self.crewmate_list):
            return True

    def who_won(self):
        """Return which team has won and set all to defaults."""
        if len(self.impostor_list) == 0 and len(self.crewmate_list) >= 2:
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
        """Start the game."""
        if len(self.impostor_list) >= 1 and len(self.crewmate_list) >= 2 and len(self.crewmate_list) > len(self.impostor_list):
            self.game = True

    def report_dead_body(self, reporting_player, dead_body):
        """Report dead body."""
        if reporting_player not in self.dead_players and dead_body in self.dead_players and self.game:
            self.meeting = True

    def cast_vote(self, player, target_name):
        """Cast vote for player for current meeting."""
        target = next((target for target in (self.crewmate_list + self.impostor_list) if target.name == target_name.capitalize()), None)
        if self.meeting and player not in self.dead_players and player.name not in self.votes and target and self.game and player in (self.impostor_list + self.crewmate_list):
            self.votes[player.name] = target.name

    def end_meeting(self):
        """End meeting, and check if there is someone to eject from spaceship."""
        if self.meeting:
            self.meeting = False
            self.dead_players.clear()
            vote_count = dict(Counter(self.votes.values()))
            max_votes = max(vote_count.values(), default=0)
            skipped_voting = len(self.impostor_list + self.crewmate_list) - len(self.votes)
            players_to_eject = [x for x in (self.impostor_list + self.crewmate_list) if x.name in vote_count and vote_count[x.name] == max_votes]
            self.votes.clear()
            print(players_to_eject)
            # print(vote_count)
            # print(max_votes)
            # print(skipped_voting)
            if max_votes == 0 or max_votes < skipped_voting:
                return "No one was ejected. (Skipped)"
            elif max_votes == skipped_voting or len(players_to_eject) != 1:
                return "No one was ejected. (Tie)"
            else:
                target = players_to_eject[0]
                self.ejected_players.append(target)
                self.crewmate_list.remove(target) if isinstance(target, Crewmate) else self.impostor_list.remove(target)
                if self.check_if_game_ended():
                    return self.who_won()
                if self.difficulty == 'hard':
                    return f"{target.name} was ejected."
                elif self.difficulty == 'easy':
                    return self.easy_game_end_meeting(target)

    def easy_game_end_meeting(self, target):
        """Help func to make end meeting less complex."""
        # +
        if len(self.impostor_list) == 1 and isinstance(target, Impostor):
            return f"{target.name} was an Impostor. 1 Impostor remains."
        #
        elif len(self.impostor_list) == 1 and isinstance(target, Crewmate):
            return f"{target.name} was not an Impostor. 1 Impostor remains."
        # +
        elif len(self.impostor_list) > 1 and isinstance(target, Impostor):
            return f"{target.name} was an Impostor. {len(self.impostor_list)} Impostors remain."
        # +
        elif len(self.impostor_list) > 1 and isinstance(target, Crewmate):
            return f"{target.name} was not an Impostor. {len(self.impostor_list)} Impostors remain."

    def get_vote(self, color: str):
        """Return players vote from current meeting."""
        if color.capitalize() in self.votes:
            return self.votes[color.capitalize()]
        return 'No vote found'

    def get_ejected_players(self):
        """Return list of ejected players."""
        return self.ejected_players

    def get_votes(self):
        """Return current meeting votes."""
        return self.votes

    def is_meeting(self):
        """Return if meeting is going or not."""
        return self.meeting
