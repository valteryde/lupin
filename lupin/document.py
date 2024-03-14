
import pdfkit
from .fileloader import loadFile


# HTML
class Document:

    def __init__(self) -> None:
        self.lines = []


    def writeLine(self, s:str) -> None:
        self.lines.append(s)


    def render(self, output="output.pdf") -> None:
        base = loadFile('base.html')
        basehtml = base.read().decode()
        base.close()
        html = basehtml.replace('{{body}}',''.join(self.lines))
        pdfkit.from_string(html, output)

