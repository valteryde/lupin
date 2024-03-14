
from typing import Any, Callable
from inspect import getsource
from .document import Document
from .render import render, renderToHtml

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

    
    def add(self, f:Callable):
        
        results = []
        for res in f():
            results.append(res)
        
        source = getsource(f)
        lines = render(source)

        # insert yields at top level
        c = 0
        for line in lines:
            
            if line["type"] == "undefined" and line["raw"][:5] == "yield":
                line["raw"] = results[c]
                c += 1
        
        # insert into document
        htmls = renderToHtml(lines)

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
        self.doc.render(fpath)
