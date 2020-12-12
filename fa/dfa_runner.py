from compiler.fa.finite_automata_2 import FiniteAutomata


class DFARunner:
    def __init__(self, fa: FiniteAutomata):
        self.fa = fa
        self.current = fa.start

    def read(self, char: str):
        self.current = self.fa.table[self.current][char][0]

        return self

    def move(self, state):
        if not self.fa.has_state(state):
            raise KeyError('state not exists')

        self.current = state
        return self

    @property
    def accepted(self):
        return self.fa.is_terminal(self.current)

    def __repr__(self):
        return 'current: ' + self.current + ' & accepted: ' + str(self.accepted)

    @staticmethod
    def run(fa, input, on_match):
        matched = []
        i = 0

        while i < len(input):
            dfa_runner = DFARunner(fa)
            j = i
            found = ''
            accepted_string = ''

            while j < len(input):
                try:
                    dfa_runner.read(input[j])
                except Exception:
                    # print('stuck', [(found + input[j]).replace('\n', '/n'), accepted_string])
                    # if input[j] == ':':
                        # print(dfa_runner.current)
                        # print('stuck', [(found + input[j]).replace('\n', '/n'), accepted_string])
                    break

                found += (input[j])
                j += 1

                if dfa_runner.accepted:
                    accepted_string = found

            if len(accepted_string):
                if callable(on_match):
                    on_match(accepted_string, i)

                matched.append([i, accepted_string])
                i += len(accepted_string)
            else:
                i += 1

        return dict(matched)