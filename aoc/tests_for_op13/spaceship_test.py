from OP.op13_spaceship.spaceship import Spaceship
from OP.op13_spaceship.spaceship import Crewmate
from OP.op13_spaceship.spaceship import Impostor


def test__crewmate_basic():
    green = Crewmate("Green", 'Crewmate', 2)
    blue = Crewmate("Blue", 'Impostor')
    assert green.__repr__() == "Green, role: Crewmate, tasks left: 2."
    assert blue.__repr__() == "Blue, role: Crewmate, tasks left: 10."


def test__impostor_basic():
    black = Impostor('black')
    assert black.__repr__() == 'Impostor Black, kills: 0.'


def test__crewmate_tasks():
    green = Crewmate('green', 'crewmate', 2)
    green.complete_task()
    assert green.tasks_left == 1
    green.complete_task()
    green.complete_task()
    green.complete_task()
    assert green.tasks_left == 0


def test__add_crewmate():
    green = Crewmate('green', 'crewmate', 2)
    green1 = Crewmate("green", 'Impostor')
    spaceship = Spaceship()
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(green1)
    assert green in spaceship.crewmate_list
    assert green1 not in spaceship.crewmate_list


def test__add_impostor():
    black = Impostor("black")
    purple = Impostor("purple")
    spaceship = Spaceship()
    spaceship.add_impostor(black)
    spaceship.add_impostor(purple)
    assert black in spaceship.impostor_list
    assert black not in spaceship.crewmate_list


def test__add_impostor_to_crewmates():
    green = Crewmate("green", 'crewmate')
    black = Impostor("black")
    spaceship = Spaceship()
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(black)
    assert black not in spaceship.crewmate_list
    assert green in spaceship.crewmate_list


def test__add_crewmate_to_impostors():
    green = Crewmate("green", 'crewmate')
    black = Impostor("black")
    spaceship = Spaceship()
    spaceship.add_impostor(green)
    spaceship.add_impostor(black)
    assert green not in spaceship.impostor_list
    assert black in spaceship.impostor_list


def test__kill_crewmate_basic():
    black = Impostor("black")
    red = Crewmate("red", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_impostor(black)
    spaceship.kill_crewmate(black, 'red')
    assert red in spaceship.dead_players
    assert red not in spaceship.crewmate_list
    assert black.__repr__() == 'Impostor Black, kills: 1.'


def test__kill_crewmate_both_impostors():
    black = Impostor("black")
    purple = Impostor("purple")
    spaceship = Spaceship()
    spaceship.add_impostor(black)
    spaceship.add_impostor(purple)
    spaceship.kill_crewmate(black, 'purple')
    assert purple not in spaceship.dead_players
    assert black.__repr__() == 'Impostor Black, kills: 0.'


def test__kill_crewmate_killer_not_impostor():
    green = Crewmate("green", 'crewmate')
    purple = Impostor("purple")
    spaceship = Spaceship()
    spaceship.add_crewmate(green)
    spaceship.add_impostor(purple)
    spaceship.kill_crewmate(green, 'purple')
    assert purple not in spaceship.dead_players


def test__kill_impostor_basic():
    purple = Impostor("purple")
    green = Crewmate("green", 'sheriff')
    spaceship = Spaceship()
    spaceship.add_impostor(purple)
    spaceship.add_crewmate(green)
    spaceship.kill_impostor(green, 'purple')
    assert purple in spaceship.dead_players
    assert purple not in spaceship.impostor_list
    assert green not in spaceship.dead_players
    assert green in spaceship.crewmate_list


def test__kill_impostor_wrong_guess():
    purple = Impostor("purple")
    green = Crewmate("green", 'sheriff')
    red = Crewmate("red", 'sheriff')
    spaceship = Spaceship()
    spaceship.add_impostor(purple)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(red)
    spaceship.kill_impostor(green, 'red')
    assert red not in spaceship.dead_players
    assert red in spaceship.crewmate_list
    assert green not in spaceship.crewmate_list
    assert green in spaceship.dead_players


def test__kill_impostor_not_sheriff():
    purple = Impostor("purple")
    green = Crewmate("green", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_impostor(purple)
    spaceship.add_crewmate(green)
    spaceship.kill_impostor(green, 'purple')
    assert purple not in spaceship.dead_players
    assert purple in spaceship.impostor_list
    assert green not in spaceship.dead_players
    assert green in spaceship.crewmate_list


def test__protect_crewmate_basic():
    red = Crewmate("red", 'Guardian Angel')
    blue = Crewmate('blue', 'crewmate')
    black = Impostor('black')
    spaceship = Spaceship()
    spaceship.add_impostor(black)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.kill_crewmate(black, 'red')
    assert blue.protected is False
    spaceship.protect_crewmate(red, blue)
    assert blue.protected is True


def test__protect_crewmate_someone_already_protected():
    red = Crewmate("red", 'guardian angel')
    blue = Crewmate('blue', 'crewmate')
    green = Crewmate('green', 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_crewmate(green)
    spaceship.protect_crewmate(red, blue)
    spaceship.protect_crewmate(red, green)
    assert green.protected is False


def test__kill_crewmate_protected():
    red = Crewmate("red", 'guardian angel')
    blue = Crewmate('blue', 'crewmate')
    black = Impostor('black')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(black)
    spaceship.kill_crewmate(black, 'red')
    spaceship.protect_crewmate(red, blue)
    spaceship.kill_crewmate(black, 'blue')
    assert blue in spaceship.crewmate_list
    assert blue not in spaceship.dead_players
    assert blue.protected is False


def test__revive_crewmate():
    red = Crewmate("red", 'altruist')
    blue = Crewmate('blue', 'crewmate')
    black = Impostor('black')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(black)
    spaceship.kill_crewmate(black, 'blue')
    spaceship.revive_crewmate(red, blue)
    assert blue not in spaceship.dead_players
    assert blue in spaceship.crewmate_list
    assert red not in spaceship.crewmate_list
    assert red in spaceship.dead_players


def test__get_crewmate_list():
    green = Crewmate("green", "crewmate")
    blue = Crewmate("blue", "crewmate")
    red = Crewmate("red", "crewmate")
    spaceship = Spaceship()
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(blue)
    spaceship.add_crewmate(red)
    assert spaceship.get_crewmate_list() == [green, blue, red]


def test__get_crewmate_list():
    green = Impostor("green")
    blue = Impostor("blue")
    red = Impostor("red")
    spaceship = Spaceship()
    spaceship.add_impostor(green)
    spaceship.add_impostor(blue)
    spaceship.add_impostor(red)
    assert spaceship.get_impostor_list() == [green, blue, red]


def test__get_dead_players():
    black = Impostor("black")
    red = Crewmate("red", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_impostor(black)
    spaceship.kill_crewmate(black, 'red')
    assert spaceship.get_dead_players() == [red]


def test__sort_crewmates_by_tasks():
    red = Crewmate("red", 'crewmate', 4)
    orange = Crewmate("orange", 'crewmate', 7)
    black = Crewmate("black", 'crewmate', 0)
    blue = Crewmate("blue", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(black)
    spaceship.add_crewmate(blue)
    assert spaceship.sort_crewmates_by_tasks() == [black, red, orange, blue]


def test__get_crewmate_with_most_tasks_done():
    blue = Crewmate("blue", 'crewmate', 4)
    red = Crewmate("red", 'crewmate', 1)
    yellow = Crewmate("yellow", 'crewmate', 7)
    green = Crewmate("green", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(blue)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.add_crewmate(green)
    assert spaceship.get_crewmate_with_most_tasks_done() == red


def test__get_rergular_crewmates():
    red = Crewmate("red", 'crewmate', 4)
    orange = Crewmate("orange", 'sheriff', 7)
    black = Crewmate("black", 'altruist', 0)
    blue = Crewmate("blue", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(black)
    spaceship.add_crewmate(blue)
    assert spaceship.get_regular_crewmates() == [red, blue]


def test__get_impostor_with_most_kills():
    purple = Impostor("purple")
    pink = Impostor("pink")
    red = Crewmate("red", 'crewmate', 4)
    orange = Crewmate("orange", 'sheriff', 7)
    black = Crewmate("black", 'altruist', 0)
    blue = Crewmate("blue", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(black)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(purple)
    spaceship.add_impostor(pink)
    spaceship.kill_crewmate(purple, 'red')
    spaceship.kill_crewmate(purple, 'blue')
    spaceship.kill_crewmate(purple, 'orange')
    spaceship.kill_crewmate(pink, 'black')
    assert spaceship.get_impostor_with_most_kills() == purple


def test__sort_impostors_by_kills():
    purple = Impostor("purple")
    pink = Impostor("pink")
    red = Crewmate("red", 'crewmate', 4)
    orange = Crewmate("orange", 'sheriff', 7)
    black = Crewmate("black", 'altruist', 0)
    blue = Crewmate("blue", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(black)
    spaceship.add_crewmate(blue)
    spaceship.add_impostor(purple)
    spaceship.add_impostor(pink)
    spaceship.kill_crewmate(purple, 'red')
    spaceship.kill_crewmate(purple, 'blue')
    spaceship.kill_crewmate(purple, 'orange')
    spaceship.kill_crewmate(pink, 'black')
    assert spaceship.sort_impostors_by_kills() == [purple, pink]


def test__get_role_of_player():
    purple = Impostor("purple")
    orange = Crewmate("orange", 'sheriff', 7)
    red = Crewmate("red", 'crewmate')
    spaceship = Spaceship()
    spaceship.add_crewmate(orange)
    spaceship.add_crewmate(red)
    spaceship.add_impostor(purple)
    assert spaceship.get_role_of_player('red') == red.role
    assert spaceship.get_role_of_player('orange') == orange.role
    assert spaceship.get_role_of_player('purple') == purple.role
