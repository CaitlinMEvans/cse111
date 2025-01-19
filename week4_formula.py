class FormulaError(ValueError):
    """FormulaError is the type of error that the parse_formula
    function will raise if a formula is invalid.
    """

def parse_formula(formula, periodic_table_dict):
    """Convert a chemical formula for a molecule into a compound
    list that stores the quantity of atoms of each element."""
    def parse_quant(formula, index):
        quant = 1
        if index < len(formula) and formula[index].isdigit():
            start = index
            while index < len(formula) and formula[index].isdigit():
                index += 1
            quant = int(formula[start:index])
        return quant, index

    def parse_r(formula, index, level):
        start_level = level
        elem_dict = {}
        while index < len(formula):
            ch = formula[index]
            if ch == "(":
                group_dict, index = parse_r(formula, index + 1, level + 1)
                quant, index = parse_quant(formula, index)
                for symbol in group_dict:
                    elem_dict[symbol] = elem_dict.get(symbol, 0) + group_dict[symbol] * quant
            elif ch.isalpha():
                symbol = formula[index:index+2]
                if symbol not in periodic_table_dict:
                    symbol = formula[index:index+1]
                if symbol not in periodic_table_dict:
                    raise FormulaError(f"Unknown element symbol: {symbol}")
                index += len(symbol)
                quant, index = parse_quant(formula, index)
                elem_dict[symbol] = elem_dict.get(symbol, 0) + quant
            elif ch == ")":
                if level == 0:
                    raise FormulaError("Unmatched close parenthesis")
                level -= 1
                index += 1
                break
            else:
                raise FormulaError(f"Illegal character: {ch}")
        if level > 0 and level >= start_level:
            raise FormulaError("Unmatched open parenthesis")
        return elem_dict, index

    elem_dict, _ = parse_r(formula, 0, 0)
    return list(elem_dict.items())