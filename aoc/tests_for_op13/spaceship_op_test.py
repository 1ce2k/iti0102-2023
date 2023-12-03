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
    assert red not in spaceship.dead_players


