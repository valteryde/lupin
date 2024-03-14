
import ast

print(ast.dump(ast.parse('2+5', mode='eval'), indent=4))
