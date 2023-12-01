"""EX 13."""


class Crewmate:
    def __init__(self, color: str, role: str, tasks = 10):
        """Init crewmate."""
        self.color = color.capitalize()
        self.role = role.title() if role.title() != 'Impostor' else 'Crewmate'
        self.tasks_left = tasks
        self.alive = True
        self.protected = False
        self.guardian = True if role == "Guardian Angel" else False

    def complete_task(self):
        """Complete task."""
        self.tasks_left -= 1

    # def get_role

    # Red, role: Crewmate, tasks left: 10.
    def __repr__(self):
        """Return str repr of obj."""
        return f"{self.color}, role: {self.role}, tasks left: {self.tasks_left}."


class Impostor(Crewmate):
    def __init__(self, color):
        """Init impostor."""
        super().__init__(color, 'Impostor', 0)
        self.kills = 0

    def add_kill(self):
        """Add kill to impostor."""
        self.kills += 1

    def __repr__(self):
        """Return str repr of impostor."""
        return f"Impostor {self.color}, kills: {self.kills}."


class Spaceship:
    def __init__(self):
        """Init spaceship."""
        self.players = []
        self.crewmate = []
        self.impostors = []
        self.dead_players = []

    def get_dead_players(self):
        """Return dead players list."""
        return self.dead_players

    def add_crewmate(self, crewmate: Crewmate):
        """Add new crewmate."""
        if crewmate not in self.crewmate and not isinstance(crewmate, Impostor):
            self.crewmate.append(crewmate)
            self.players.append(crewmate)

    def get_crewmate_list(self):
        """Return crewmate list."""
        return self.crewmate

    def add_impostor(self, impostor: Impostor):
        """Add new impostor."""
        if isinstance(impostor, Impostor) and impostor.color not in [x.color for x in self.crewmate] and len(
                self.impostors) <= 2:
            self.impostors.append(impostor)
            self.players.append(impostor)

    def get_impostor_list(self):
        """Return impostor list."""
        return self.impostors

    def kill_crewmate(self, killer, killed):
        """Kill crewmate."""
        matched_killed = [x for x in self.crewmate if x.color == killed.capitalize()]
        if matched_killed and isinstance(killer, Impostor) and not matched_killed[0].protected and not isinstance(matched_killed[0], Impostor):
            killer.kills += 1
            self.dead_players.append(matched_killed[0])
            self.crewmate.remove(matched_killed[0])
            matched_killed[0].alive = False

        elif matched_killed and isinstance(killer, Impostor) and matched_killed[0].protected:
            matched_killed[0].protected = False

    def protect_crewmate(self, guardian, crewmate):
        """Protect crewmate."""
        if guardian.guardian and crewmate.alive and not guardian.alive:
            crewmate.protected = True
    def revive_crewmate(self, altruist, killed):
        if killed in self.dead_players and altruist.role == "Altruist":
            self.dead_players.remove(killed)
            self.crewmate.append(killed)
            self.dead_players.append(altruist)

    def get_role_of_player(self, color):
        for player in self.players:
            if player.color == color.capitalize():
                return player.role

    def sort_crewmates_by_tasks(self):
        return sorted(self.crewmate, key=lambda x: x.tasks_left)

    def get_regular_crewmates(self):
        return [x for x in self.crewmate if x.role == "Crewmate"]

    def get_impostor_with_most_kills(self):
        return sorted(self.impostors, key=lambda x: -x.kills)[0]

    def get_crewmate_with_most_tasks_done(self):
        return sorted(self.crewmate, key=lambda x: x.tasks_left)[0]

    def sort_impostors_by_kills(self):
        return sorted(self.impostors, key=lambda x: -x.kills)


if __name__ == "__main__":
    print("Spaceship.")

    spaceship = Spaceship()
    print(spaceship.get_dead_players())  # -> []
    print()

    print("Let's add some crewmates.")
    red = Crewmate("Red", "Crewmate")
    white = Crewmate("White", "Impostor")
    yellow = Crewmate("Yellow", "Guardian Angel", tasks=5)
    green = Crewmate("green", "Altruist")
    blue = Crewmate("BLUE", "Sheriff", tasks=0)

    print(red)  # -> Red, role: Crewmate, tasks left: 10.
    print(white)  # -> White, role: Crewmate, tasks left: 10.
    print(yellow)  # -> Yellow, role: Guardian Angel, tasks left: 5.
    print(blue)  # -> Blue, role: Sheriff, tasks left: 0.
    print()

    print("Let's make Yellow complete a task.")
    yellow.complete_task()
    print(yellow)  # ->  Yellow, role: Guardian Angel, tasks left: 4.
    print()

    print("Adding crewmates to Spaceship:")
    spaceship.add_crewmate(red)
    spaceship.add_crewmate(white)
    spaceship.add_crewmate(yellow)
    spaceship.add_crewmate(green)
    print([x.color for x in spaceship.get_crewmate_list()])  # -> Red, White, Yellow and Green

    spaceship.add_impostor(blue)  # Blue cannot be an Impostor.
    print([x.color for x in spaceship.get_impostor_list()])  # -> []
    spaceship.add_crewmate(blue)
    print()

    print("Now let's add impostors.")
    orange = Impostor("orANge")
    black = Impostor("black")
    purple = Impostor("Purple")
    spaceship.add_impostor(orange)
    spaceship.add_impostor(black)

    spaceship.add_impostor(Impostor("Blue"))  # Blue player already exists in Spaceship.
    spaceship.add_impostor(purple)
    spaceship.add_impostor(Impostor("Pink"))  # No more than three impostors can be on Spaceship.
    print(spaceship.get_impostor_list())  # -> Orange, Black and Purple
    print()

    print("The game has begun! Orange goes for the kill.")
    spaceship.kill_crewmate(orange, "yellow")
    print(orange)  # -> Impostor Orange, kills: 1.
    spaceship.kill_crewmate(black, "purple")  # You can't kill another Impostor, silly!
    print(spaceship.get_dead_players())  # -> Yellow
    print()

    print("Yellow is a Guardian angel, and can protect their allies when dead.")
    spaceship.protect_crewmate(yellow, green)
    print(green.protected)  # -> True
    spaceship.kill_crewmate(orange, "green")
    print(green in spaceship.dead_players)  # -> False
    print(green.protected)  # -> False
    print()

    print("Green revives their ally.")
    spaceship.kill_crewmate(purple, "RED")
    spaceship.revive_crewmate(green, red)
    print(red in spaceship.dead_players)  # -> False
    print()

    print("Let's check if the sorting and filtering works correctly.")

    red.complete_task()
    print(spaceship.get_role_of_player("Blue"))  # -> Sheriff
    spaceship.kill_crewmate(purple, "blue")
    print(spaceship.sort_crewmates_by_tasks())  # -> Red, White
    print(spaceship.sort_impostors_by_kills())  # -> Purple, Orange, Black
    print(spaceship.get_regular_crewmates())  # -> White, Red

