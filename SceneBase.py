
class Scene(object):
    def __init__(self):
        self.next = self

    def ProcessInput(self, events):
        raise NotImplementedError

    def Update(self):
        raise NotImplementedError

    def Render(self, screen):
        raise NotImplementedError

    def SwitchToScene(self, next_scene):
        self.next = next_scene
