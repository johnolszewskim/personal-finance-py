from itertools import cycle
class Console:

    def __init__(self, functions: []):

        # self.functions = cycle(functions)
        self.functions = functions
        self.func_index = 0

    def run(self):
        print('Console.run()')



