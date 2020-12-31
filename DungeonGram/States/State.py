class State:
    def update(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def should_transition(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()