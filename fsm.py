from transitions.extensions import GraphMachine

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def to_a(self, update):
        text = update.message.text
        return text == '加行程'

    def to_b(self, update):
        text = update.message.text
        return text == '查行程'

    def a_to_c(self, update):
        text = update.message.text
        return text == 'A go to C'

    def on_enter_state1(self, update):
        update.message.reply_text("state A here")
        update.message.reply_photo(open('test.gif', 'rb'))
        # self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("state B here")
        # self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("state C here")