from tkinter import *
from tkinter import font, filedialog
from tkinter import messagebox as mbox
from markdown2 import Markdown
from tkhtmlview import HTMLLabel
from tkinter.scrolledtext import ScrolledText
from os.path import splitext,basename


class BookWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Helvetica", size=14)
        self.init_window()

    def init_window(self):
        self.master.title("Book Viewer and Editor")
        self.pack(fill=BOTH, expand=1)
        self.inputeditor = ScrolledText(self, width="1", font=self.myfont)
        self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT)
        self.outputbox = HTMLLabel(
            self, width="1", background="white", html="""<h1>Preview Pane</h1><p>Markdown is supported here</p>
            <p>Special thanks to <a href="https://github.com/bauripalash">bauripalash</a> for the markdown</p>
            """)
        self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)
        self.outputbox.fit_height()
        self.inputeditor.bind("<<Modified>>", self.onInputChange)
        self.mainmenu = Menu(self)
        self.filemenu = Menu(self.mainmenu)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Save as", command=self.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.mainmenu.add_cascade(label="File", menu=self.filemenu)
        self.master.config(menu=self.mainmenu)

    def onInputChange(self, event):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        # self.outputbox.set_html(md2html.convert(self.inputeditor.get("1.0" , END)))
        markdownText = self.inputeditor.get("1.0", END)
        html = md2html.convert(markdownText)
        self.outputbox.set_html(html)

    def openfile(self,directory=None):
        if directory is None:
            openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),
                                                                ("Text File", "*.txt"),
                                                                ("All Files", "*.*")))
        else:
            openfilename = directory
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END)
                self.inputeditor.insert(END, open(openfilename).read())
                self.master.title("Book Viewer and Editor - " + splitext(basename(openfilename))[0].title())
            except:
                # print("Cannot Open File!")
                mbox.showerror("Error Opening Selected File" , "Oops!, The file you selected : {} can not be opened!".format(openfilename))
    
    def savefile(self):
        filedata = self.inputeditor.get("1.0" , END)
        savefilename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"),
                                                                  ("Text File", "*.txt")) , title="Save Markdown File")
        if savefilename:
            try:
                f = open(savefilename , "w")
                f.write(filedata)
            except:
                mbox.showerror("Error Saving File" , "Oops!, The File : {} can not be saved!".format(savefilename))


def viewbook(directory=None,master=None):
    if master is None:
        root = Tk()
    else:
        root = Toplevel(master)
    root.geometry("700x600")
    app = BookWindow(root)
    if directory is not None:
        app.openfile(directory=directory)
    app.mainloop()

if __name__ == "__main__":
    viewbook(r"E:\Tin hoc\Lap trinh\Project\Python practices\pygame games\Tkinter\books\license.md")