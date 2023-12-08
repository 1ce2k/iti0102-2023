from spaceship_op import OPSpaceship
from spaceship import Crewmate
from spaceship import Impostor


def test__spaceship_basic():
    spaceship = OPSpaceship('easy')
    assert spaceship.difficulty == 'easy'
    assert spaceship.meeting is False
    assert spaceship.game is False
    assert spaceship.votes == {}
    assert spaceship.ejected_players == []
    spaceship1 = OPSpaceship('hard')
    assert spaceship1.difficulty == 'hard'
    spaceship2 = OPSpaceship("hferhgjvbhjg")
    assert spaceship2.difficulty == 'hard'


def test__start_game_succes():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    black = Impostor('black')
    spaceship = OPSpaceship('easy')
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(red)
    spaceship.add_impostor(black)
    spaceship.start_game()
    assert spaceship.game is True


def test__start_game_failed():
    green = Crewmate('green', 'crewmate')
    black = Impostor('black')
    spaceship = OPSpaceship('easy')
    spaceship.add_crewmate(green)
    spaceship.add_impostor(black)
    spaceship.start_game()
    assert spaceship.game is False


def test__add_crewmate_when_not_game():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    spaceship = OPSpaceship('easy')
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(red)
    assert spaceship.crewmate_list == [green, red]


def test__add_crewmate_when_game():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    yellow = Crewmate('yellow', 'crewmate')
    black = Impostor('black')
    spaceship = OPSpaceship('easy')
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(red)
    spaceship.add_impostor(black)
    spaceship.start_game()
    spaceship.add_crewmate(yellow)
    assert yellow not in spaceship.crewmate_list


def test__add_impostor_when_not_game():
    green = Impostor("green")
    red = Impostor('red')
    spaceship = OPSpaceship('easy')
    spaceship.impostor_list = [green, red]
    assert spaceship.impostor_list == [green, red]


def test__add_impostor_when_game():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    black = Impostor('black')
    pink = Impostor('pink')
    spaceship = OPSpaceship('easy')
    spaceship.crewmate_list = [green, red]
    spaceship.add_impostor(black)
    spaceship.start_game()
    spaceship.add_impostor(pink)
    assert pink not in spaceship.impostor_list


def test__kill_crewmate_game_has_not_begun():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    black = Impostor('black')
    spaceship = OPSpaceship("easy")
    spaceship.crewmate_list = [green, red]
    spaceship.add_impostor(black)
    spaceship.kill_crewmate(black, 'red')
    assert red not in spaceship.dead_players


def test__kill_crewmate_can_not_kill_during_meeting():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    black = Impostor('black')
    spaceship = OPSpaceship("easy")
    spaceship.crewmate_list = [green, red]
    spaceship.add_impostor(black)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.kill_crewmate(black, 'red')
    assert red not in spaceship.dead_players


def test__kill_crewmate_game_ends():
    green = Crewmate('green', 'crewmate')
    red = Crewmate('red', 'crewmate')
    black = Impostor('black')
    spaceship = OPSpaceship("easy")
    spaceship.crewmate_list = [green, red]
    spaceship.add_impostor(black)
    spaceship.start_game()
    spaceship.game = False
    spaceship.kill_crewmate(black, 'red')
    assert spaceship.game is False


def test__kill_impostor_basic():
    green = Crewmate("green", "Sheriff")
    red = Crewmate("red", "Sheriff")
    yellow = Crewmate("yellow", "Sheriff")
    black = Impostor("black")
    purple = Impostor("purple")
    spaceship = OPSpaceship('easy')
    spaceship.add_impostor(black)
    spaceship.add_impostor(purple)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    spaceship.kill_impostor(green, 'black')
    assert black in spaceship.dead_players
    assert black not in spaceship.impostor_list
    assert spaceship.game is True


def test__kill_impostor_game_ends():
    green = Crewmate("green", "Sheriff")
    red = Crewmate("red", "Sheriff")
    black = Impostor("black")
    spaceship = OPSpaceship('easy')
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    spaceship.kill_impostor(green, 'black')
    assert spaceship.game is False


def test__check_if_game_ended_crew_win():
    green = Crewmate("green", "Sheriff")
    red = Crewmate("red", "Sheriff")
    black = Impostor("black")
    spaceship = OPSpaceship('easy')
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    spaceship.kill_impostor(green, 'black')
    assert spaceship.check_if_game_ended() is True


def test__check_if_game_ended_impostor_win():
    green = Crewmate("green", "Sheriff")
    red = Crewmate("red", "Sheriff")
    black = Impostor("black")
    spaceship = OPSpaceship('easy')
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    spaceship.kill_crewmate(black, 'green')
    assert spaceship.check_if_game_ended() is True


def test__who_won_impostors_won():
    green = Crewmate("green", "Sheriff")
    red = Crewmate("red", "Sheriff")
    black = Impostor("black")
    spaceship = OPSpaceship('easy')
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    assert spaceship.kill_crewmate(black, 'green') == 'Impostors won.'
    assert spaceship.game is False
    assert spaceship.meeting is False
    assert spaceship.difficulty == ''
    assert spaceship.is_anyone_protected is False
    assert spaceship.crewmate_list == []
    assert spaceship.impostor_list == []
    assert spaceship.dead_players == []
    assert spaceship.ejected_players == []
    assert spaceship.votes == {}


def test__who_won_crewmates_won():
    green = Crewmate("green", "Sheriff")
    red = Crewmate("red", "Sheriff")
    black = Impostor("black")
    spaceship = OPSpaceship('easy')
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    assert spaceship.kill_impostor(green, 'black') == 'Crewmates won.'
    assert spaceship.game is False
    assert spaceship.meeting is False
    assert spaceship.difficulty == ''
    assert spaceship.is_anyone_protected is False
    assert spaceship.crewmate_list == []
    assert spaceship.impostor_list == []
    assert spaceship.dead_players == []
    assert spaceship.ejected_players == []
    assert spaceship.votes == {}


def test__report_dead_body_dead_reporting():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.kill_crewmate(black, 'red')
    spaceship.report_dead_body(red, red)
    assert spaceship.meeting is False


def test__report_dead_body():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.kill_crewmate(black, 'red')
    spaceship.report_dead_body(yellow, red)
    assert spaceship.meeting is True


def test__report_dead_body_no_body_to_report():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    blue = Crewmate("blue", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.kill_crewmate(black, 'red')
    spaceship.report_dead_body(yellow, blue)
    assert spaceship.meeting is False


def test__report_dead_body_dead_reporting():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.report_dead_body(red, red)
    assert spaceship.meeting is False


def test__cast_vote():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(black, 'red')
    assert spaceship.votes == {'Black': 'Red'}


def test__cast_vote_no_body_to_report():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(black, 'green')
    assert spaceship.votes == {}


def test__cast_vote_no_game():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.cast_vote(black, 'green')
    assert spaceship.votes == {}


def test__cast_vote_duplicate_vote():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(black, 'yellow')
    spaceship.cast_vote(black, 'red')
    assert spaceship.votes == {'Black': 'Yellow'}


def test__cast_vote_player_not_in_deadlist():
    black = Impostor('black')
    red = Crewmate("red", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.add_crewmate(green)
    spaceship.start_game()
    spaceship.kill_crewmate(black, 'green')
    spaceship.cast_vote(black, 'green')
    assert spaceship.votes == {}
    spaceship.cast_vote(green, 'black')
    assert spaceship.votes == {}


def test__end_meeting_game_continues_easy():
    black = Impostor('black')
    pink = Impostor('pink')
    blue = Impostor('blue')
    red = Crewmate("red", 'crew')
    orange = Crewmate("orange", 'crew')
    white = Crewmate("white", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("easy")
    spaceship.add_impostor(black)
    spaceship.add_impostor(pink)
    spaceship.add_impostor(blue)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(black, 'red')
    spaceship.cast_vote(green, 'red')
    spaceship.cast_vote(yellow, 'red')
    spaceship.cast_vote(white, 'red')
    spaceship.cast_vote(orange, 'red')
    assert spaceship.end_meeting() == 'Red was not an Impostor. 3 Impostors remain.'
    assert spaceship.votes == {}
    assert red in spaceship.ejected_players
    assert red not in spaceship.crewmate_list
    assert spaceship.meeting is False

    spaceship.meeting = True
    spaceship.cast_vote(black, 'blue')
    spaceship.cast_vote(orange, 'blue')
    spaceship.cast_vote(white, 'blue')
    spaceship.cast_vote(yellow, 'blue')
    assert spaceship.end_meeting() == 'Blue was an Impostor. 2 Impostors remain.'
    assert blue in spaceship.ejected_players

    spaceship.meeting = True
    spaceship.cast_vote(black, 'black')
    spaceship.cast_vote(yellow, 'black')
    spaceship.cast_vote(orange, 'black')
    spaceship.cast_vote(white, 'black')
    assert spaceship.end_meeting() == "Black was an Impostor. 1 Impostor remains."
    assert black in spaceship.ejected_players

    spaceship.meeting = True
    spaceship.cast_vote(black, 'white')
    spaceship.cast_vote(yellow, 'white')
    spaceship.cast_vote(green, 'white')
    spaceship.cast_vote(orange, 'white')
    assert spaceship.end_meeting() == 'White was not an Impostor. 1 Impostor remains.'
    assert white in spaceship.ejected_players


def test__end_meeting_hard():
    black = Impostor('black')
    pink = Impostor('pink')
    blue = Impostor('blue')
    red = Crewmate("red", 'crew')
    orange = Crewmate("orange", 'crew')
    white = Crewmate("white", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("hard")
    spaceship.add_impostor(black)
    spaceship.add_impostor(pink)
    spaceship.add_impostor(blue)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(red, 'black')
    spaceship.cast_vote(yellow, 'black')
    spaceship.cast_vote(green, 'black')
    spaceship.cast_vote(orange, 'black')
    spaceship.cast_vote(white, 'black')
    spaceship.cast_vote(blue, 'black')
    assert spaceship.end_meeting() == 'Black was ejected.'

    spaceship.meeting = True
    spaceship.cast_vote(green, 'red')
    spaceship.cast_vote(blue, 'red')
    spaceship.cast_vote(orange, 'red')
    spaceship.cast_vote(white, 'red')
    spaceship.cast_vote(green, 'red')
    spaceship.cast_vote(yellow, 'red')
    assert spaceship.end_meeting() == "Red was ejected."


def test__end_meeting_skipped():
    black = Impostor('black')
    pink = Impostor('pink')
    blue = Impostor('blue')
    red = Crewmate("red", 'crew')
    orange = Crewmate("orange", 'crew')
    white = Crewmate("white", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("hard")
    spaceship.add_impostor(black)
    spaceship.add_impostor(pink)
    spaceship.add_impostor(blue)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    assert spaceship.end_meeting() == 'No one was ejected. (Skipped)'
    spaceship.meeting = True
    spaceship.cast_vote(white, 'red')
    spaceship.cast_vote(orange, 'red')
    spaceship.cast_vote(black, 'red')
    assert spaceship.end_meeting() == 'No one was ejected. (Skipped)'


def test__end_meeting_tie():
    black = Impostor('black')
    pink = Impostor('pink')
    blue = Impostor('blue')
    red = Crewmate("red", 'crew')
    orange = Crewmate("orange", 'crew')
    white = Crewmate("white", 'crew')
    yellow = Crewmate("yellow", 'crew')
    green = Crewmate("green", 'crew')
    spaceship = OPSpaceship("hard")
    spaceship.add_impostor(black)
    spaceship.add_impostor(pink)
    spaceship.add_impostor(blue)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(yellow)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(white, 'red')
    spaceship.cast_vote(orange, 'red')
    spaceship.cast_vote(black, 'red')
    spaceship.cast_vote(green, 'red')
    assert spaceship.end_meeting() == 'No one was ejected. (Tie)'

    spaceship.meeting = True
    spaceship.cast_vote(white, 'red')
    spaceship.cast_vote(orange, 'red')
    spaceship.cast_vote(black, 'red')
    spaceship.cast_vote(green, 'white')
    spaceship.cast_vote(pink, 'white')
    spaceship.cast_vote(blue, 'white')
    assert spaceship.end_meeting() == 'No one was ejected. (Tie)'


def test__get_vote():
    red = Crewmate('red', 'crew')
    blue = Crewmate('blue', 'crew')
    pink = Impostor("pink")
    spaceship = OPSpaceship('hard')
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(pink)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(pink, 'red')
    spaceship.cast_vote(blue, 'pink')
    spaceship.cast_vote(red, 'blue')
    assert spaceship.get_vote('red') == 'Blue'
    assert spaceship.get_vote('pink') == 'Red'
    assert spaceship.get_vote('blue') == 'Pink'


def test__get_votes():
    red = Crewmate('red', 'crew')
    blue = Crewmate('blue', 'crew')
    pink = Impostor("pink")
    spaceship = OPSpaceship('hard')
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(pink)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(pink, 'red')
    spaceship.cast_vote(blue, 'pink')
    spaceship.cast_vote(red, 'blue')
    assert spaceship.get_votes() == {'Pink': 'Red', 'Blue': 'Pink', 'Red': 'Blue'}


def test__is_meeting():
    red = Crewmate('red', 'crew')
    blue = Crewmate('blue', 'crew')
    pink = Impostor("pink")
    spaceship = OPSpaceship('hard')
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(pink)
    assert spaceship.is_meeting() is False
    spaceship.start_game()
    spaceship.meeting = True
    assert spaceship.is_meeting() is True


def test__get_ejected_players():
    red = Crewmate("red", 'crew')
    green = Crewmate("green", 'crew')
    blue = Crewmate("blue", 'crew')
    orange = Crewmate("orange", 'crew')
    black = Impostor("black")
    pink = Impostor("pink")
    spaceship = OPSpaceship('hard')
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(orange)
    spaceship.add_impostor(black)
    spaceship.add_impostor(pink)
    spaceship.start_game()
    spaceship.meeting = True
    spaceship.cast_vote(blue, 'pink')
    spaceship.cast_vote(orange, 'pink')
    spaceship.cast_vote(pink, 'pink')
    spaceship.cast_vote(red, 'pink')
    spaceship.end_meeting()
    spaceship.meeting = True
    spaceship.cast_vote(blue, 'green')
    spaceship.cast_vote(black, 'green')
    spaceship.cast_vote(red, 'green')
    spaceship.end_meeting()
    assert spaceship.get_ejected_players() == [pink, green]
