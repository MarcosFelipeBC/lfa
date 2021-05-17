import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import Frame
from tkinter import messagebox
from tkinter.constants import FALSE, X
from PIL import Image, ImageTk
from reportlab.graphics.shapes import _DrawTimeResizeable
from reportlab.platypus.doctemplate import SimpleDocTemplate
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class AFNEProcessScreen:
    def __init__(self, automata):
        self.getPng("./resources/AFNE.dot.svg")
        self.automata = automata
        efechoInicial = self.calculateEfecho(self.automata.initialState, set())
        self.stack = []
        for state in self.calculateEfecho(self.automata.initialState, set()):
            self.stack.append((state, 0))
        
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.configure(background='black')
        self.frame_information = tk.Frame(self.root, height=800, width=540, bg='lightblue')
        self.frame_image = tk.Frame(self.root, height=800, width=540, bg='white')
        self.initialWindow(efechoInicial)

    def initialWindow(self, efechoInicial):
        self.clear_frame(self.frame_information)
        self.clear_frame(self.frame_image)
        
        img = Image.open('./resources/AFNE.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        self.root.geometry("1080x720") 
        yscrollbar = ttk.Scrollbar(self.frame_image, orient=tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill="y")
        xscrollbar = ttk.Scrollbar(self.frame_image, orien=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill="x")
        canvas = tk.Canvas(self.frame_image,width=510, height=800, background='white', highlightbackground='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        yscrollbar.config(command = canvas.yview)
        xscrollbar.config(command = canvas.xview)
        
        tk.Label(self.frame_information, text="Digite a cadeia a ser consumida", bg='lightblue', font="Verdana 16 bold").place(x= 93, y=10)
        self.frame_information.pack(side=tk.LEFT)
        self.frame_image.pack(side=tk.RIGHT)
        
        chainEntry = self.chainEntry()
        self.startButton(chainEntry)

        tk.Label(self.frame_information, text=f"Possibilidades iniciais:\n {efechoInicial}", bg='lightblue', font="Verdana 12 bold").place(x= 140, y= 280)
        
        self.root.mainloop()
       

    def calculateEfecho(self, state, efechoSoFar):
        efecho = set([state])
        efechoSoFar.update(efecho)
        if (state, 'E') in self.automata.transitions:
            for nextState in self.automata.transitions[(state, 'E')]:
                if not nextState in efechoSoFar:
                    efecho.update(self.calculateEfecho(nextState, efechoSoFar))
        
        return efecho

    def processingWindow(self, chain):
        if len(self.stack) == 0:
            self.endWithFail()
            return 
        
        state, position = self.stack.pop()

        if position == len(chain):
            if state == self.automata.acceptingState:
                self.endWithSuccess(state)
            else: 
                self.processingWindow(chain)
                
        efecho = set()
        if position != len(chain):
            symbol = chain[position]
            if (state, symbol) in self.automata.transitions:
                for nextState in self.automata.transitions[(state, symbol)]:
                    efecho.update(self.calculateEfecho(nextState, set()))

                for nextFromEfecho in efecho:
                    self.stack.append((nextFromEfecho, position+1))

        self.clear_labels(self.frame_information)
        tk.Label(self.frame_information, text="Cadeia a ser consumida:", bg='lightblue', font="Verdana 16 bold").place(x= 120, y=10)
        
        if len(efecho) == 0:
            tk.Label(self.frame_information, text=f"ESTADO ATUAL: \"{state}\" | Posição: {position} | Símbolo: {chain[position]}\nPossibilidades: {{}}", bg='lightblue', font="Verdana 12 bold").place(x= 75, y= 280)
        else:
            tk.Label(self.frame_information, text=f"ESTADO ATUAL: \"{state}\" | Posição: {position} | Símbolo: {chain[position]}\nPossibilidades: {efecho}", bg='lightblue', font="Verdana 12 bold").place(x= 75, y= 280)

        self.root.geometry("1080x720")
        self.nextButton(chain)
        self.root.mainloop()
        
    def chainEntry(self):
        chainEntry = tk.StringVar()
        chainEntry = tk.Entry(self.frame_information, width=30, textvariable=chainEntry, highlightbackground="lightblue")
        chainEntry.place(x= 90, y=70)
        return chainEntry

    def nextButton(self, chain): 
        button = tk.Button(self.frame_information, text="Next", command=lambda:self.processingWindow(chain), width=7, height=2, highlightbackground="lightblue")
        button.place(x=178 , y=140)

    def startButton(self, chainEntry):
        button = tk.Button(self.frame_information, text="Start", command=lambda:self.startButtonAction(chainEntry), width=7, height=2,highlightbackground="lightblue")
        button.place(x=178 , y=140)

    def startButtonAction(self, chainEntry):
        chain = chainEntry.get()
        if self.automata.validateChain(chain) == False:
            messagebox.showinfo("Cadeia inválida", "A cadeia possui símbolos inválidos")
            chainEntry.delete(0, 'end')
        else:
            self.processingWindow(chain)

    def endWithSuccess(self, state):
        messagebox.showinfo("Resultado:", "Estado final: " + state + "\nCADEIA ACEITA!")
        self.stack = []
        efechoInicial = self.calculateEfecho(self.automata.initialState, set())
        for state in efechoInicial:
            self.stack.append((state, 0))
        self.initialWindow(efechoInicial)

    def endWithFail(self):
        messagebox.showinfo("Resultado:", "CADEIA REJEITADA!")
        efechoInicial = self.calculateEfecho(self.automata.initialState, set())
        for state in efechoInicial:
            self.stack.append((state, 0))
        self.initialWindow(efechoInicial)
    
    def getPng(self, svg_file):
        drawing = svg2rlg(svg_file)
        renderPM.drawToFile(drawing, "./resources/AFNE.png", fmt="PNG")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def clear_labels(self, frame):
        for widget in frame.winfo_children():
            if widget.winfo_class() == "Label":
                widget.destroy()
                