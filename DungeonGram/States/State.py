class State:
    def on_enter(self):
        raise NotImplementedError()

    def on_exit(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def should_transition(self):
        raise NotImplementedError()