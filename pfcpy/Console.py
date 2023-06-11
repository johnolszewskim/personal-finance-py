from prompt_toolkit.key_binding import KeyBindings
class Console:

    def __init__(self, functions: []):

        # self.functions = cycle(functions)
        self.functions = functions
        self.func_index = 0

    def run(self):
        print('Console.run()')

    def next(self) -> int:

        return 1





