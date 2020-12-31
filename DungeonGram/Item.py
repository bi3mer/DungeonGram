class Item:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    def use(self, target):
        if target.type not in self.info:
            raise TypeError(f'{self.name} cannot act on type {target.type}')

        if self.info.effect_type == 'heal':
            target.health += self.info[target.type].value
        elif self.info.effect_type == 'heal':
            target.health -= self.info[target.type].value
        else:
            raise TypeError(f'{self.name} has unhandled {self.info.effect_type}')
