import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from automata import Automata
from partialAutomata import PartialAutomata

class Screen:
    def __init__(self, filename, automata):
        self.getPng(filename)
        self.automata = automata
        self.partialAutomata = PartialAutomata(self.automata)
        self.root = tk.Tk()
        self.initialWindow()

    def initialWindow(self):
        self.cleanScreen()
        self.root.configure(bg='white')
        img = Image.open('./resources/tmp.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        canvas = tk.Canvas(self.root, width=size[0], height=size[1], bg='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        self.root.geometry("1080x720")

        tk.Label(self.root, text="Digite a cadeia a ser consumida", bg='white', font="Verdana 16 bold", pady=10).place(x= 2, y=20)

        chainEntry = self.chainEntry()
        self.startButton(chainEntry)
        self.root.mainloop()
        
    def updateImage(self):
        self.partialAutomata.createImage()
        self.getPng("./resources/partialAutomata.dot.svg")

    def startProcessingWindow(self, chain):
        self.cleanScreen()
        self.root.configure(bg='white')
        self.updateImage()
        img = Image.open('./resources/tmp.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        canvas = tk.Canvas(self.root, width=size[0], height=size[1], bg='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        self.root.geometry("1080x720")
        self.nextButton(chain, -1)
        self.root.mainloop()

    def processingWindow(self, chain, position):
        if position == len(chain):
            self.endConsumption()
            return
            
        self.partialAutomata.consumeChain(chain, position)
        self.updateImage()
        self.cleanScreen()
        self.root.configure(bg='white')
        img = Image.open('./resources/tmp.png')

        
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        canvas = tk.Canvas(self.root, width=size[0], height=size[1], bg='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        
        label = tk.Label(self.root, text=f"Cadeia: \"{chain}\" | Símbolo: {chain[position]} | Posição: {position}", bg='white', font="Verdana 12 bold")
        label.pack(side = tk.LEFT)

        self.root.geometry("1080x720")
        self.nextButton(chain, position)
        self.root.mainloop()

    def endConsumption(self):
        if self.partialAutomata.currentState in self.automata.acceptingStates:
            messagebox.showinfo("Resultado:", "CADEIA ACEITA!")
        else:
            messagebox.showinfo("Resultado:", "CADEIA REJEITADA!")
        
        self.partialAutomata = PartialAutomata(self.automata)
        self.getPng("./resources/AFD.dot.svg")
        self.initialWindow()
        
    def cleanScreen(self):
        _list = self.root.winfo_children()

        for item in _list:
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        for item in _list:
            item.pack_forget()

    def chainEntry(self):
        chainEntry = tk.StringVar()
        chainEntry = tk.Entry(self.root, width=30, textvariable=chainEntry)
        chainEntry.place(x=5, y=90)
        return chainEntry

    def nextButton(self, chain, position): 
        button = tk.Button(self.root, text="Next", command=lambda:self.processingWindow(chain, position+1), width=7, height=2)
        button.place(x=10, y=200)

    def startButton(self, chainEntry):
        button = tk.Button(self.root, text="Start", command=lambda:self.startButtonAction(chainEntry), width=7, height=2)
        button.place(x=10, y=200)

    def startButtonAction(self, chainEntry):
        chain = chainEntry.get()
        if self.automata.validateChain(chain) == False:
            messagebox.showinfo("Cadeia inválida", "A cadeia possui símbolos inválidos")
            chainEntry.delete(0, 'end')
        else:
            self.startProcessingWindow(chain)

    def getPng(self, svg_file):
        drawing = svg2rlg(svg_file)
        renderPM.drawToFile(drawing, "./resources/tmp.png", fmt="PNG")