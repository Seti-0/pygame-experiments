from PodSixNet.Channel import Channel

class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        BoxesGame: self.game = None

    def Network(self, data):
        print(f"[{self.addr}] {data}")

    def Network_requestPlace(self, data):
        print(f"[{self.addr}] {data}")

        if self.game is None:
            print("(Channel is not assigned to a game, no action taken)")
            return

        try:
            i = int(data["i"])
            j = int(data["j"])
            horizontal = bool(int(data["horizontal"]))
        except NameError as err:
            print(err)
            return
        except ValueError as err:
            print(err)
            return

        self.game.AddLine(i, j, horizontal, self)

    def to_bool(self, target) -> bool:
        if type(target) == bool:
            return target
        elif target == "True":
            return True
        elif target == "False":
            return False
        else:
            raise ValueError("Target {")
