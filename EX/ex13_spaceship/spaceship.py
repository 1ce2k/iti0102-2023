"""EX 13."""


class Spaceship:
    """Spaceship class."""

    def __init__(self):
        """Init spaceship."""
        self.crewmate_list = []
        self.impostor_list = []
        self.dead_players = []
        self.is_anyone_protected = False

    def add_crewmate(self, crewmate):
        """Add new crewmate."""
        if isinstance(crewmate, Crewmate) and crewmate.name not in [x.name for x in self.crewmate_list] and crewmate.name not in [x.name for x in self.impostor_list]:
            self.crewmate_list.append(crewmate)

    def add_impostor(self, impostor):
        """Add new impostor."""
        if isinstance(impostor, Impostor) and impostor.name not in [x.name for x in self.crewmate_list] and impostor.name not in [x.name for x in self.impostor_list] and len(self.impostor_list) < 3:
            self.impostor_list.append(impostor)

    def kill_crewmate(self, killer, target_name):
        """Kill crewmate."""
        target = next((crewmate for crewmate in self.crewmate_list if crewmate.name == target_name.capitalize()), None)
        if target and killer in self.impostor_list and target not in self.dead_players:
            if not target.protected:
                target.is_dead = True
                self.dead_players.append(target)
                self.crewmate_list.remove(target)
                killer.kills += 1
            else:
                target.protected = False
                self.is_anyone_protected = False

    def kill_impostor(self, killer, target_name):
        """Kill impostor."""
        if killer.role != "Sheriff" or killer not in self.crewmate_list:
            print(1)
            return
        target = next((x for x in (self.impostor_list + self.crewmate_list) if x.name == target_name.capitalize()), None)
        if target and target.role != 'Impostor':
            print('wrong color')
            self.crewmate_list.remove(killer)
            self.dead_players.append(killer)
            self.dead_players.append(target)
            self.crewmate_list.remove(target)

        elif target and target in self.impostor_list:
            'right color'
            self.dead_players.append(target)
            self.impostor_list.remove(target)
            self.dead_players.append(killer)
            self.crewmate_list.remove(killer)

    def protect_crewmate(self, guardian_angel, target):
        """Protect someone."""
        if guardian_angel in self.dead_players and guardian_angel.role == 'Guardian Angel' and not self.is_anyone_protected and target not in self.dead_players:
            target.protected = True
            self.is_anyone_protected = True

    def revive_crewmate(self, reviver, target):
        """Revive someone."""
        if reviver in self.crewmate_list and reviver.role == 'Altruist' and not reviver.is_dead and target in self.dead_players:
            target.is_dead = False
            reviver.is_dead = True
            self.dead_players.remove(target)
            self.crewmate_list.append(target)
            self.dead_players.append(reviver)
            self.crewmate_list.remove(reviver)

    def get_crewmate_list(self):
        """Return crewmate list."""
        return self.crewmate_list

    def get_impostor_list(self):
        """Return impostor list."""
        return self.impostor_list

    def get_dead_players(self):
        """Return dead players list."""
        return self.dead_players

    def sort_crewmates_by_tasks(self):
        """Sort crewmates by tasks."""
        return sorted(self.crewmate_list, key=lambda x: x.tasks_left)

    def get_regular_crewmates(self):
        """Return list of crewmates with role 'Crewmate'."""
        return [x for x in self.crewmate_list if x.role == "Crewmate"]

    def get_impostor_with_most_kills(self):
        """Return impostor with most kills."""
        return sorted(self.impostor_list, key=lambda x: -x.kills)[0]

    def get_crewmate_with_most_tasks_done(self):
        """Return crewmate with most tasks done."""
        return sorted(self.crewmate_list, key=lambda x: x.tasks_left)[0]

    def sort_impostors_by_kills(self):
        """Sort impostors by kills."""
        return sorted(self.impostor_list, key=lambda x: -x.kills)

    def get_role_of_player(self, name):
        """Return role of player."""
        for player in (self.impostor_list + self.crewmate_list):
            if player.name == name.capitalize():
                return player.role


class Crewmate:
    """Crewmate class."""

    def __init__(self, name, role, tasks=10):
        """Init crewmate."""
        self.name = name.capitalize()
        self.role = role.title() if role.title() != 'Impostor' else 'Crewmate'
        self.tasks_left = tasks
        self.is_dead = False
        self.protected = False

    def complete_task(self):
        """Complete task."""
        if not self.is_dead and self.tasks_left > 0:
            self.tasks_left -= 1

    def __repr__(self):
        """Return str."""
        return f"{self.name}, role: {self.role}, tasks left: {self.tasks_left}."


class Impostor:
    """Impostor class."""

    def __init__(self, name):
        """Init impostor."""
        self.name = name.capitalize()
        self.role = "Impostor"
        self.kills = 0
        self.protected = False

    def __repr__(self):
        """Return str."""
        return f"Impostor {self.name}, kills: {self.kills}."


if __name__ == "__main__":
    spaceship = Spaceship()
    blue = Crewmate("Blue", "Sheriff", 10)
    green = Crewmate("Green", "Crewmate", 10)
    red = Crewmate("Red", "Guardian angel", 10)
    yellow = Crewmate("yellow", "altruist", 10)
    impostor = Impostor("Black")
    spaceship.add_crewmate(blue)
    spaceship.add_crewmate(green)
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(yellow)
    spaceship.add_impostor(impostor)
    print(spaceship.get_crewmate_list())
    print(spaceship.get_impostor_list())
    print()
    spaceship.kill_crewmate(impostor, 'red')

    print("Test kill impostor")
    spaceship.kill_impostor(blue, "green")
    print(spaceship.dead_players)
    # print(blue in spaceship.crewmate_list)
    # print(blue in spaceship.dead_players)
    # print(impostor in spaceship.dead_players)
    # print(impostor in spaceship.impostor_list)
#