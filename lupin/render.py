
import ast

def parse(source):
    return ast.parse(source)



def renderToHtml(tree, results=[]):
    print(dir(tree))
    
    htmls = []
    for obj in tree.body:

        # render functions with one line as f(x)=2*x    
        if (
            type(obj) == ast.FunctionDef and
            len(obj.body) == 1
            ):
            htmls.append('funktion på en linje')

        elif type(obj) == ast.FunctionDef:
            
            renderToHtml(obj)


    return htmls
