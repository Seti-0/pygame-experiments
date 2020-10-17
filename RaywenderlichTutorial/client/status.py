import resources
from client import Client


class StatusScreen():

    MESSAGES = {
        Client.CONNECTING: "Searching for game...",
        Client.WAITING_ON_PLAYER: "Joined game as RED player",
        Client.DISCONNECTED: "Disconnected"
    }

    def __init___(self, target: Client):
        self.target = target

    def draw(self, screen):
        x = y = resources.margin
        color = (255, 255, 255)

        # Draw the current status message
        message = StatusScreen.MESSAGES[self.target.state]
        label = resources.font_small.render(message, 0, color)
        screen.blit(label, [x,y])