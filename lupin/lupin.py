
from typing import Any, Callable, Generator, Iterator
from types import GeneratorType
from inspect import getsource
from .document import Document
from .render import parseSourceCode, renderToHtml


class Lupin:

    def __init__(self):
        self.doc = Document()


    # def __call__(self, s) -> Any:
    #     print(s)
    #     print()

    
    def image(self, ):
        pass


    def plot(self, ):
        pass

    
    def add(self, f:Callable, run=True):
        
        results = []
        if run:
            generator = f()
            if type(generator) is GeneratorType:
                for res in generator:
                    results.append(res)

        source = getsource(f)
        lines = parseSourceCode(source)

        # insert into document
        htmls = renderToHtml(lines, results=results)

        for html in htmls:
            self.doc.writeLine(html)

        #print(lines)

    def write(self, line):
        self.doc.writeLine(line)


    # chapter, sections, subsection
    def chapter(self, s:str) -> None:
        self.doc.writeLine(f'<h1>{s}</h1>')


    def section(self, s:str) -> None:
        self.doc.writeLine(f'<h2>{s}</h2>')


    def subsection(self, s:str) -> None:
        self.doc.writeLine(f'<h3>{s}</h3>')


    # render and save
    def save(self, fpath:str):
        # self.doc.renderToHTML()
        self.doc.renderToPdf(fpath)
