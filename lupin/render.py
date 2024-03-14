
def getFunctions(lines):
    # sammenkobel funktioner
    source = []
    currentIndent = 0
    for indent, line in lines:
        linesplit = line.split(' ')

        if currentIndent > indent:
            currentIndent = indent
            
            
        if linesplit[0] == "def" and currentIndent == 0:
            currentIndent = indent+1
            source.append({
                "type": "function",
                "name": linesplit[1],
                "lines": []
            })
            
        elif currentIndent == 0:
            source.append({"type":"undefined", "raw":line, "indent":indent-currentIndent})

        elif currentIndent > 0:
            source[-1]["lines"].append((indent-currentIndent, line))


    # find resten af funktionerne (rekursivt)
    for line in source:

        if line["type"] == "function":
            line["lines"] = getFunctions(line["lines"])

    return source


def render(source):
    source = source.split('\n')[1:]
    source = [line for line in source if line.replace(' ', '')]

    # beregn indentationer
    lines = []
    for line in source:
            
        for i, char in enumerate(line):
            if char != ' ': break

        lines.append((i//4-1, line[i:]))

    lines = getFunctions(lines)

    # erstat kommentare
    for line in lines:
        if line["type"] == "undefined" and line["raw"].replace(' ', '')[0] == "#":
            line["type"] = "text"

    return lines


def getFirstKeyWord(line):
            
    for i, char in enumerate(line):
        if char != ' ': break
    
    if ' ' in line[i:]:
        j = line[i:].index(' ')
        return line[i:line[i:].index(' ')], j

    return line[i:], len(line)-1

    

def renderToHtml(lines):
    
    html = []
    for line in lines:

        # plain text
        if line["type"] == "text":
            s = line["raw"].replace('#', '', 1)
            html.append(f'<p>{s}</p>')


        # functions with one line
        # shortens to f(x)=2*x
        if (
            line["type"] == "function" and 
            len(line["lines"]) == 1 and 
            line["lines"][0]["type"] == "undefined" and
            getFirstKeyWord(line["lines"][0]["raw"])[0] == "return"
            ):
            
            i = getFirstKeyWord(line["lines"][0]["raw"])[1]
            s = line["name"].replace(':', '')
            html.append(f'<p>{s}={line["lines"][0]["raw"][i:]}</p>')

        
        elif line["type"] == "function" and len(line["lines"]) > 1:
            pass
            #s = html.append(f'')


    print(html)
    return html

