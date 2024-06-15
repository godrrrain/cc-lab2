from typing import List


class Rule:
    def __init__(self, left, right: List[str]):    # list[list[str]]
        self.left = left
        self.right = right.copy()


class Grammar:
    def __init__(self, non_terms, terms, rules, start):
        self.non_terms = non_terms
        self.terms = terms
        self.rules = rules
        self.start = start

    def print(self, msg="", grammar_name="G", is_print_gaps=True):
        print("\n"+msg)
        output = grammar_name + ' = '
        output += "{{[{:}], [{:}], {:}}}".format(",".join(sorted(self.non_terms)), ",".join(sorted(self.terms)), self.start)

        for non_term in sorted(self.non_terms):
            rules = list(filter(lambda x: x.left == non_term, self.rules))
            if not len(rules):
                continue

            if is_print_gaps:
                output += '\n' + (non_term + " -> " + " | ".join(sorted(map(lambda x: " ".join(x.right) if len(x.right) else 'ε', rules))))
            else:
                output += '\n' + (non_term + " -> " + "|".join(sorted(map(lambda x: "".join(x.right) if len(x.right) else 'ε', rules))))

        print(output)

    def remove_left_rec(self):
        new_rules = self.rules.copy()
        new_non_terms = self.non_terms.copy()

        for i, nt_i in enumerate(self.non_terms):

            # удаление косвенной рекурсии
            for nt_j in self.non_terms[:i]:
                rules = filter(lambda x: x.left == nt_i and len(x.right) and x.right[0] == nt_j, new_rules)
                for rule in rules:
                    new_rules.remove(rule)
                    tmp_rules = list(filter(lambda x: x.left == nt_j, new_rules))
                    for rule_2 in tmp_rules:
                        new_rules.append(
                            Rule(
                                nt_i, rule_2.right + rule.right[1:]
                            )
                        )

            # удаление прямой рекурсии
            rules = list(filter(lambda x: x.left == nt_i, new_rules))
            is_dir_rec = False
            for rule in rules:
                if len(rule.right) and rule.right[0] == nt_i:
                    is_dir_rec = True
                    break

            if is_dir_rec:
                new_non_term = nt_i + "'"
                new_non_terms += [new_non_term]
                alpha = list(filter(lambda x: len(x.right) and x.right[0] == nt_i, rules))
                beta = list(filter(lambda x: len(x.right) == 0 or (len(x.right) and x.right[0] != nt_i), rules))

                for rule in rules:
                    new_rules.remove(rule)
                for rule in beta:
                    new_rules.append(Rule(left=nt_i, right=rule.right + [new_non_term]))
                for rule in alpha:
                    new_rules.append(Rule(left=new_non_term, right=rule.right[1:] + [new_non_term]))
                new_rules.append(Rule(left=new_non_term, right=[]))

        return Grammar(new_non_terms, self.terms.copy(), new_rules, self.start)

    @staticmethod
    def _add_rules_family(left_terminal, right, N, new_rules, current_pos=0):
        new_rules.append(Rule(left=left_terminal, right=right))
        for idx in range(current_pos, len(right)):
            if right[idx] in N:
                new_right = right[:idx]
                if idx < len(right) - 1:
                    new_right += right[idx + 1:]
                    Grammar._add_rules_family(left_terminal, new_right, N, new_rules, idx)
                else:
                    new_rules.append(Rule(left=left_terminal, right=new_right))

    def remove_eps(self):
        eps_rules = list(filter(lambda x: len(x.right) == 0, self.rules))
        N_eps = set()   # множество ε-пораждающих нетерминалов
        for rule in eps_rules:
            N_eps.add(rule.left)

        new_non_terms = self.non_terms.copy()
        new_rules = []
        for rule in self.rules:
            if len(rule.right) == 0:
                continue
            self._add_rules_family(rule.left, rule.right, N_eps, new_rules)

        if self.start in N_eps:
            new_start_non_term = self.start + "1"
            new_non_terms.append(new_start_non_term)
            new_rules.append(Rule(left=new_start_non_term, right=[self.start]))
            new_rules.append(Rule(left=new_start_non_term, right=[]))
            return Grammar(new_non_terms, self.terms.copy(), new_rules, new_start_non_term)

        return Grammar(new_non_terms, self.terms.copy(), new_rules, self.start)

    @staticmethod
    def inp_form_console():
        print("Введите нетерминалы (через пробел):")
        non_terms = input().split(' ')
        
        print("Введите терминалы (через пробел):")
        terms = input().split(' ')

        print("Введите количество продукций:")
        num_of_rules = int(input())
        rules = []
        print("Вводите каждую продукцию с новой строки:")
        for i in range(num_of_rules):
            rule = input()
            left, right = rule.split(' -> ')
            for rule in right.split(' | '):
                if len(rule) and rule[0] == 'ε':
                    rules.append(Rule(left=left, right=[]))
                    continue
                rules.append(Rule(left=left, right=rule.split(' ')))

        print("Определите стартовый символ:")
        start = input()
        return Grammar(non_terms=non_terms, terms=terms, rules=rules, start=start)
