from grammar_builder import Grammar

if __name__ == '__main__':
    grammar = Grammar.inp_form_console()
    grammar.print("Исходная грамматика", "G")
    g_without_left_rec = grammar.remove_left_rec()
    g_without_left_rec.print("Грамматика с удаленной левой рекурсией", "G'")

    g_without_left_rec.remove_eps().print("Грамматика без ε-правил", "G_eps")
