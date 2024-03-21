
import pdfkit
from .fileloader import loadFile
import os
from .render import images

# HTML
class Document:

    def __init__(self) -> None:
        self.lines = []


    def writeLine(self, s:str) -> None:
        self.lines.append(s)


    def renderToPdf(self, output:str="output.pdf") -> None:
        pdfkit.from_file(self.renderToHTML(output), output, options={'enable-local-file-access':"", "debug-javascript": ""} )

    
    def renderToHTML(self, output="output") -> None:
        # create folder
        folder = output.split('.')[0] # for en sikkerheds skyld
        if not os.path.isdir(folder): os.mkdir(folder)

        base = loadFile('base.html')
        basehtml = base.read().decode()
        base.close()
        html = basehtml.replace('{{body}}','\n'.join(self.lines))
        html = html.replace('{{folderpath}}', '') # kan være relevant til pdf (husk "/")

        for filename, img in images:
            img.save(os.path.join(folder, filename))

        fname = os.path.join(folder, 'index.html')
        f = open(fname, 'w')
        f.write(html)
        f.close()

        return fname
