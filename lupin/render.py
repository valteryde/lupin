from baron import parse, dumps
import fondi
from .colors import RED, BLUE, GREEN, RESET, printcolor
import pprint


# parser
def removeJunkFromTree(tree):

    offset = 0
    for j in range(len(tree)):
        i = j - offset
        branch = tree[i]

        if branch["type"] in ["if", "for", "def"]:
            removeJunkFromTree(branch["value"])

        if branch["type"] in ["endl"]:
            tree.pop(i)
            offset += 1


def parseSourceCode(source):
    
    # inject pass before comments
    newsource = []
    for line in source.split('\n'):
        if "#" in line:
            
            index = line.index('#')

            if len(line[:index].replace(' ', '')) == 0:
                newsource.append(line[:index]+'pass')
        
        newsource.append(line)

    source = '\n'.join(newsource)

    fst = parse(source)[0]["value"]
    removeJunkFromTree(fst)
    return fst


def addDollar(text, add=True):
    if add: return f'${text}$'
    return text


def substituteFunctionNameToMathNotation(name, args):
    """
    ...if posible
    """

    if name == "pow":
        return '{' + args[0] + '}^{' + args[1] + '}'


    args = ', '.join(args)
    return '\\text{'+name+'}' f'({args})'


# to html
# skal måske splittes op eller i eget dokument
def renderLine(line, ableToDropParenthesis=False, isInsideMath=False):
    """
    FST til

    10 + 5^2 + f(2)
    """

    if 'type' not in line.keys():
        return dumps(line)


    elif line["type"] == "binary_operator":
        
        if line["value"] == "/":
            return addDollar(
                '\\frac{' + renderLine(line["first"], ableToDropParenthesis=True, isInsideMath=True) + '}{' + renderLine(line["second"], ableToDropParenthesis=True, isInsideMath=True)  + '}'
            , not isInsideMath)

        elif line["value"] == "**":
            return addDollar(
                '{' + renderLine(line["first"], isInsideMath=True) + '}^{' + renderLine(line["second"], isInsideMath=True) + '}'
            , not isInsideMath)

        elif line["value"] in ['+', '-', '*']:
            return addDollar(
                renderLine(line["first"], isInsideMath=True) + line["value"] + renderLine(line["second"], isInsideMath=True)
            , not isInsideMath)

    elif line["type"] == "associative_parenthesis" and ableToDropParenthesis:

        return f'{renderLine(line["value"], isInsideMath=isInsideMath)}'

    elif line["type"] == "associative_parenthesis":

        return f'({renderLine(line["value"], isInsideMath=isInsideMath)})'
        
    elif line["type"] == "atomtrailers":
        valsbeforecall = []
        for val in line["value"]:
            
            if val["type"] == "call":
                
                # FEJL: Returnere kun sidste del
                
                args = [renderLine(arg["value"], isInsideMath=True) for arg in val["value"] if arg["type"] != "comma"] # true på grund af nedenstående linje

                if len(args) == 0: args = '\\,'

                return addDollar(
                    f'{substituteFunctionNameToMathNotation(valsbeforecall[-1]["value"], args)}', not isInsideMath
                )
            
            valsbeforecall.append(val)

    elif line["type"] in ["return", "yield"]:
        return line["type"] + ' ' + renderLine(line["value"], isInsideMath=False)

    elif line["type"] == "list_comprehension":
        # Jeg er lidt usikker på hvornår der er flere generators, men kan vel ske
        # Dette arbejdes dog ikke med nu
        
        iterator = line["generators"][0]["iterator"]
        if iterator["type"] == "tuple":
            iterators = ", ".join([i["value"] for i in iterator["value"] if i["type"] == "name"])
        else:
            iterators = iterator["value"]

        return f'seq({renderLine(line["result"])}, {iterators}={renderLine(line["generators"][0]["target"])})'
        #list_comprehension

    elif line["type"] == "name":
        pass#print(line)

    elif line["type"] == "continue":
        return 'Spring over omgang'

    elif line["type"] == "string":
        
        if isInsideMath:
            s = line["value"][1:-1].replace('$', '')
        else:
            s = line["value"][1:-1]
        s = s.replace('\\\\', '\\')
        return addDollar('\\text{"}' + f'{s}' + '\\text{"}', not isInsideMath)

    elif line["type"] in ["int", "float"]:
        return addDollar(
            f'{line["value"]}', not isInsideMath
        )
        pass#print(line["type"])


    return dumps(line)


def addIndent(depth):
    return 4 * depth * "&nbsp;"


images = []  # er ikke mere klasse constrained, eventuelt dict som small fix
count = 0


def createMath(text, color=(0,0,0,255), fontSize=1):
    global count
    """
    create MathText
    render as html image
    """
    printcolor(BLUE, text)
    filename = f"{count}.png"
    mathtext = fondi.MathText(text, round(64*fontSize), color).image
    images.append((filename, mathtext))
    r = f'<img class="math" style="height:{mathtext.height/4}px" src="!{filename}">'.replace("!", "{{folderpath}}")

    count += 1
    return r

def removeWhiteSpaceBefore(text):
    
    for i, char in enumerate(text):
        if char != " ":
            return text[i:]
    
    return text


def createText(text, fontSize=1, color=(0,0,0,255)):

    indexes = [0]
    for i, c in enumerate(text):
        if c == "$" and text[i-1] != "\\":
            indexes.append(i)
    indexes.append(len(text))

    res = ""
    for i in range(0, len(indexes) - 1):
        if len(text[indexes[i] : indexes[i + 1]].replace(' ', '')) == 0:
            continue

        if i % 2 == 0:
            res += "\\text{" + text[indexes[i] : indexes[i + 1]] + "}"
        else:
            res += text[indexes[i] + 1 : indexes[i + 1]]
            indexes[i + 1] += 1

    printcolor(RED, text)
    return createMath(res, color=color, fontSize=fontSize)


def determineResultSubstitution(res, line):
    global count

    if type(res) in [str, int, float]:
        return f'<p>{createText(renderLine(line))}</p><p class="result-math">{createMath(str(res), (0,0,255,255))}</p>'


    if hasattr(res, 'save'):

        filename = f"{count}.png"
        r = f'<img class="result-image" src="!{filename}">'.replace("!", "{{folderpath}}")
        images.append((filename, res))

        count += 1
        return r


    if type(res) in [dict, list, tuple, set]:

        return ''
        return f'<p>{createText(renderLine(line))}</p><p class="result-math">{createMath(str(res), (0,0,255,255))}</p>'


# er egentlig bare renderLines (flertal)
def renderToHtml(tree, depth=0, results=[]):
    # alt for mange gentagelser
    # skal simplficieres
    # -> hoved div (en gang for alle istedet for det her rod)
    # -> indent ? (jeg ved ikke engang selv hvad fanden der menes her)
    # -> styles og ikke bare tekst

    htmls = []
    for obj in tree:

        # render functions with one line as f(x)=2*x
        if (
            obj["type"] == "def"
            and len(obj["value"]) == 1
            and obj["value"][0]["type"] == "return"
        ):
            args = ", ".join([i["target"]["value"] for i in obj["arguments"]])

            r = f'${obj["name"]}({args})={renderLine(obj["value"][0]["value"], isInsideMath=True)}$'

            htmls.append(f"<div>{addIndent(depth)}{createText(r)}</div>")


        # normal function
        elif obj["type"] == "def":

            args = ", ".join([i["target"]["value"] for i in obj["arguments"] if i["type"] == "name"])
            s = f'Funktion $\\,{obj["name"]}({args})$' #FEJL I FONDI! HER BRUGES DÅRLIG FIKS
            
            funcinner = ''.join(renderToHtml(obj["value"], depth + 1))

            htmls.append(
                f"""<div class="function">
                    <div class="function-title">{addIndent(depth)}{createText(s)}</div>
                    <div class="function-lines">{funcinner}</div>
                </div>
                """
            )


        # comment
        elif obj["type"] == "comment":

            # add titles
            if obj["value"][1:4] == "!!!":
                htmls.append(f'<div>{addIndent(depth)}{createText(removeWhiteSpaceBefore(obj["value"][4:]), fontSize=1.5)}</div>')

            elif obj["value"][1:3] == "!!":
                htmls.append(f'<div>{addIndent(depth)}{createText(removeWhiteSpaceBefore(obj["value"][3:]), fontSize=2)}</div>')

            elif obj["value"][1] == "!":
                htmls.append(f'<div>{addIndent(depth)}{createText(removeWhiteSpaceBefore(obj["value"][2:]), fontSize=3)}</div>')

            else:
                htmls.append(f'<div>{addIndent(depth)}{createText(removeWhiteSpaceBefore(obj["value"][1:]))}</div>')


        # yield / result statements
        elif depth == 0 and obj["type"] == "yield":
            if len(results) > 0:
                htmls.append(
                    f'<div><div class="result">{determineResultSubstitution(results.pop(0), obj["value"])}</div></div></div>'
                )
            else:
                s = f'<p>{createText(renderLine(obj["value"]))}</p>'

                htmls.append(
                    f'<div><div class="result">{s}</div></div></div>'
                )


        elif obj["type"] == "assignment" and obj["value"]["type"] in ["dict"]: #pprint
            r = createText(f'{obj["target"]["value"]} = ' + '$\\{$')
            htmls.append(
                f'<div>{addIndent(depth)}{r}</div>'
            )

            # kun first niveau
            for i in obj["value"]["value"]:
                if i["type"] != "dictitem": continue
                
                dicthtml = '<div>' + addIndent(depth+1) + createText(f'{renderLine(i["key"])} : {renderLine(i["value"])}') + '</div>'
                htmls.append(dicthtml)

            s = f'<div>{addIndent(depth)}' + createText('$\\}$') + '</div>'
            htmls.append(s)


            # r = createText('')
            # htmls.append(
            #     f'<div>{addIndent(depth)}{r}</div>'
            # )


        elif obj["type"] == "assignment":
            
            r = createText(f'{renderLine(obj["target"])} = {renderLine(obj["value"])}')
            htmls.append(
                f'<div>{addIndent(depth)}{r}</div>'
            )


        elif obj["type"] in ["return", "yield"]:

            htmls.append(
                f'<div>{addIndent(depth)}{createText(renderLine(obj))}</div>'
            )
        
        elif obj["type"] in ["import", "from"]:

            htmls.append(
                f'<div>{addIndent(depth)}{createText(renderLine(obj), color=(0,0,100,255))}</div>'
            )

        elif obj["type"] == "atomtrailers":
            htmls.append(
                f'<div>{addIndent(depth)}{createText(renderLine(obj))}</div>'
            )

        elif obj["type"] == "for":
            
            if obj["iterator"]["type"] == "tuple":
                iterators = ", ".join([i["value"] for i in obj["iterator"]["value"] if i["type"] == "name"])
            else:
                iterators = obj["iterator"]["value"]


            #if obj["target"]["type"] == "atomtrailers" and obj["target"]["value"][0]["value"] == "range":    
            #    print(obj["target"]["value"][1]["value"])
            
            # ide!
            #    s = f'For ${iterators} = 1, 2, 3 ... 5$'

            s = f'For alle ${iterators}$ i {renderLine(obj["target"])}'


            funcinner = ''.join(renderToHtml(obj["value"], depth + 1))

            htmls.append(
                f"""<div class="function">
                    <div class="function-title">{addIndent(depth)}{createText(s)}</div>
                    <div class="function-lines">{funcinner}</div>
                </div>
                """
            )

        elif obj["type"] == "ifelseblock":
            printcolor(GREEN, obj)
            
            htmls.extend(renderToHtml(obj["value"], depth=depth + 1))


        elif obj["type"] == "if":
            s = createText(f'Hvis {renderLine(obj["test"])}:')

            htmls.append(f'<div>{addIndent(depth)}{s}</div>')
            
            htmls.extend(renderToHtml(obj["value"], depth=depth+1))

            printcolor(GREEN, obj)


        elif obj["type"] == "continue":
            
            htmls.append(f'<div>{addIndent(depth)}{createMath("Spring over linje")}</div>')


        else:
            pass


    return htmls

