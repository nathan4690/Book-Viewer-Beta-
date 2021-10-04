from tkinter import *
from tkinter import messagebox,ttk
from PIL import Image, ImageTk
import webbrowser as wb
from os.path import abspath,dirname,exists,splitext,basename
import bookEditor

USERSPATH = (abspath(dirname(__file__)) + "\\users\\")[0].upper() + (abspath(dirname(__file__)) + "\\users\\")[1:]
BOOKFILESPATH = abspath(dirname(__file__)) + "\\books\\"
RESOURCESPATH = abspath(dirname(__file__)) + "\\resources\\"

class SelectionRequiredInvalid(Exception):
    pass

class CheckboxTreeview(ttk.Treeview):
    """
        Treeview widget with checkboxes left of each item.
        The checkboxes are done via the image attribute of the item, so to keep
        the checkbox, you cannot add an image to the item.
    """

    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        # checkboxes are implemented with pictures
        a = Image.open(RESOURCESPATH+'checked.png')
        wi,he = a.size;rat = 1
        # a.resize((wi//rat,he//rat))
        self.im_checked = ImageTk.PhotoImage(a,size=(wi//rat,he//rat))
        b = Image.open(RESOURCESPATH+'unchecked.png')
        # b.resize((wi//rat,he//rat))
        self.im_unchecked = ImageTk.PhotoImage(b,size=(wi//rat,he//rat))
        self.tag_configure("unchecked", image=self.im_unchecked)
        self.tag_configure("checked", image=self.im_checked)
        # check / uncheck boxes on click
        self.bind("<Button-1>", self.box_click, True)

    def insert(self, parent, index, iid=None, **kw):
        """ same method as for standard treeview but add the tag 'unchecked'
            automatically if no tag among ('checked', 'unchecked', 'tristate')
            is given """
        if not "tags" in kw:
            kw["tags"] = ("unchecked",)
        elif not ("unchecked" in kw["tags"] or "checked" in kw["tags"]
                  or "tristate" in kw["tags"]):
            kw["tags"] = ("unchecked",)
        ttk.Treeview.insert(self, parent, index, iid, **kw)

    def check_descendant(self, item):
        """ check the boxes of item's 
         """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("checked",))
            self.check_descendant(iid)

    def check_ancestor(self, item):
        """ check the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("checked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["checked" in self.item(c, "tags") for c in children]
            self.check_ancestor(parent)

    def uncheck_descendant(self, item):
        """ uncheck the boxes of item's descendant """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("unchecked",))
            self.uncheck_descendant(iid)

    def uncheck_ancestor(self, item):
        """ uncheck the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("unchecked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["unchecked" in self.item(c, "tags") for c in children]
            self.uncheck_ancestor(parent)

    def box_click(self, event):
        """ check or uncheck box when clicked """
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.identify_row(y)
            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)

class Screen:
    def __init__(self,mainscreen:Tk) -> None:
        self.mainscreen = mainscreen
    
    def closing(self):
        confirm = messagebox.askyesnocancel("Quit","Are you really want to quit?")
        if confirm:
            exit()

    def initialize(self,screen:Toplevel,title,sx,sy,close=False,showScreen=True,rat=2):
        screen.title(title)
        screen.geometry(f"{sx}x{sy}+{int(self.mainscreen.winfo_screenwidth()/rat - sx/2)}+{int(self.mainscreen.winfo_screenheight()/rat - sy/2)}")
        screen.resizable(False,False)

        if close:
            screen.protocol("WM_DELETE_WINDOW",self.closing)
        else:
            screen.protocol("WM_DELETE_WINDOW",lambda:[self.mainscreen.deiconify() if showScreen else print("",end=""),screen.destroy()])

    def save(self,u,t:ttk.Treeview):
        tc = []
        for child in t.get_children():
            for i in range(3):
                tc.append(t.item(child)["values"][i])

        with open(USERSPATH+u+".txt") as f:
            dat = [a.rstrip("\n") for a in f.readlines()]

        with open(USERSPATH+u+".txt","w") as f:
            f.write(dat[0]+"\n")
            for i in range(0,len(tc),3):
                f.write(tc[i] + "\n")
                f.write(tc[i+1] + "\n")
                f.write(tc[i+2] + "\n")

    def packToTree(self,t:ttk.Treeview,wr,bo,pu,b,w,p):
        if b and w and p:
            t.insert("",END,values=(str(b),str(w),str(p)))
            wr.delete(0,END)
            bo.delete(0,END)
            pu.delete(0,END)
        else:
            messagebox.showwarning("NoneError","Not enough data to add. Please try again")

    def getChecked(self,treeViewObject: ttk.Treeview,getString=False,NoOfObjectRequired = None):
        x = []
        for i in treeViewObject.get_children():
            if "checked" in treeViewObject.item(i)["tags"] and i not in x:
                x.append(i)

        if len(x) == NoOfObjectRequired or NoOfObjectRequired is None:
            if getString:
                xReturnerToGetString = []
                for i in x:
                    xReturnerToGetString.append(treeViewObject.item(i)["values"][0])
                return xReturnerToGetString
            return x
        else:
            messagebox.showerror("SelectionRequiredInvalid","Invalid number of selections, try again")
            raise SelectionRequiredInvalid(f"""Invalid number of selection: {len(x)}, """ +
            f"""while the expected number of selection is {NoOfObjectRequired}""")

    def deletesome(self,t: ttk.Treeview):
        x = []
        x += self.getChecked(t)
        if len(x) == 0:
            messagebox.showwarning("NoneSelected","No selected item(s), try again")
            return None

        for i in x:
            t.delete(i)

    def searchOnline(self,treeViewObject: ttk.Treeview):
        listSelection = self.getChecked(treeViewObject,True,NoOfObjectRequired=1)

        wb.get().open("https://www.google.com/search?tbm=bks&q=" + listSelection[0])

    def editBook(self,directory:str):
        directory = directory[0].upper() + directory[1:]
        if exists(directory):
            bookEditor.viewbook(directory,self.mainscreen)
        else:
            a = messagebox.askyesno("Create book",f"No book named {splitext(basename(directory))[0].title()} found. Create one?")
            if a:
                maker = open(directory,"w")
                maker.close()
                bookEditor.viewbook(directory=directory,master=self.mainscreen)

    def aboutScreen(self):
        about_width = 400
        about_height = 300
        about_window = Toplevel(self.mainscreen)
        self.initialize(about_window,"About",500,300,showScreen=False)

        Label(about_window,text="Book viewer Beta",font=("Arial",20,"bold")).pack()
        Label(about_window,text="Version 1.1 (dev)",font=("Arial",20,"bold")).pack()
        Label(about_window,text="This book viewer is created with ♡ by nathan4690" \
        ,font=("Arial",14),wraplength=about_width).pack(anchor=CENTER)
        Label(about_window,text="""You are free to get or modify (fork) this or older versions, """+
        """but please give credit to creator. """+
        """For more information, take a look at the license""" \
        ,wraplength=about_width,font=("Arial",14)).pack(anchor=CENTER)
        Label(about_window,text="View license on:",font=("Arial",12,"bold"),padx=500-about_width//2).pack(anchor=W)
        gith = Label(about_window,text="Github",font=("Arial",12,"underline"),fg="blue",padx=500-about_width//2)
        gith.pack(anchor=W)
        gith.bind("<Button-1>",lambda event: wb.open("https://github.com/nathan4690/Book-Viewer-Beta-/blob/main/LICENSE"))
        gith.bind("<Enter>",lambda event: gith.config(fg="red",cursor="hand2"))
        gith.bind("<Leave>",lambda event: gith.config(fg="blue"))
        ls = Label(about_window,text="Local Storage",font=("Arial",12,"underline"),fg="blue",padx=500-about_width//2)
        ls.pack(anchor=W)
        ls.bind("<Button-1>",lambda event: bookEditor.viewbook(BOOKFILESPATH + "license.md",about_window))
        ls.bind("<Enter>",lambda event: ls.config(fg="red",cursor="hand2"))
        ls.bind("<Leave>",lambda event: ls.config(fg="blue"))

    def raiseNotImplemented(self):
        raise NotImplementedError

    def adminScreen(self,user):
        app = Toplevel(self.mainscreen)
        self.initialize(app,"Book Viewer: " + str(user),1000,625,True)
        ico = PhotoImage(file=RESOURCESPATH+'book.png')
        app.tk.call('wm', 'iconphoto', app._w, ico)
        menu = Menu(app,tearoff=0)
        app.config(menu=menu)

        fileMenu = Menu(menu,tearoff=0)
        optionsMenu = Menu(menu,tearoff=0)
        menu.add_cascade(label="File", menu=fileMenu)
        menu.add_cascade(label="Options",menu=optionsMenu)

        trvlblf = LabelFrame(app,relief="groove",text="Your Books")
        trvf = Frame(trvlblf)
        trvlblf.pack()
        trvf.pack()

        mbt = CheckboxTreeview(trvf,columns=("#1","#2","#3"),selectmode="browse")
        widthSize = 285
        mbt.column("#0",minwidth=45,width=30)
        mbt.column("#1",minwidth=190,width=widthSize)
        mbt.column("#2",minwidth=190,width=widthSize)
        mbt.column("#3",minwidth=190,width=widthSize)
        # mbt.column("#3",minwidth=200,width=widthSize)
        mbt.heading('#0', text='', anchor='center')
        mbt.heading("#1",text="Book name")
        mbt.heading("#2",text="Writer")
        mbt.heading("#3",text="Publisher")

        bn = StringVar()
        wt = StringVar()
        pl = StringVar()

        elblf = LabelFrame(app,relief="groove",text="Edit Data")
        elblf.pack(anchor="w",padx=20,fill="x")

        ew = 75
        ttk.Label(elblf,text="Book Name").grid(row=0,column=0,pady=(10,0))
        be = ttk.Entry(elblf,width=ew,textvariable=bn)
        be.grid(row=0,column=1,pady=(10,0))
        ttk.Label(elblf,text="Writer").grid(row=1,column=0)
        we = ttk.Entry(elblf,width=ew,textvariable=wt)
        we.grid(row=1,column=1)
        ttk.Label(elblf,text="Publisher").grid(row=2,column=0,pady=(0,10))
        pe = ttk.Entry(elblf,width=ew,textvariable=pl)
        pe.grid(row=2,column=1,pady=(0,10))
        pe.bind("<Return>",lambda event=None: self.packToTree(mbt,be,we,pe,bn.get(),wt.get(),pl.get()))

        ttk.Button(elblf,text="Add item", \
        command=lambda: self.packToTree(mbt,be,we,pe,bn.get(),wt.get(),pl.get())).grid(row=3,column=0,pady=(0,10))
        ttk.Button(elblf,text="Remove Selected Item(s)",command=lambda:[self.deletesome(mbt)]).grid(row=3,column=1,pady=(0,10))

        mlblf = LabelFrame(app,relief="groove",text="More Book Details")
        mlblf.pack(anchor="w",padx=20,fill="both")
        
        self.searchImage = PhotoImage(file=RESOURCESPATH+"search.png")
        self.searchImage = self.searchImage.subsample(10)
        online_search = ttk.Button(mlblf,text="Search this book online (Google)", \
        compound="top",image=self.searchImage,command=lambda: self.searchOnline(mbt))
        online_search.grid(padx=(10,0),pady=(10,10))
        self.viewImage = PhotoImage(file=RESOURCESPATH+"View-edit.png")
        self.viewImage = self.viewImage.subsample(5)
        bookContentEditButton = ttk.Button(mlblf,text="View/edit Selected Book's Content",compound=TOP,image=self.viewImage, \
        command=lambda: self.editBook(BOOKFILESPATH + self.getChecked(mbt,True,NoOfObjectRequired=1)[0] + ".md"))
        bookContentEditButton.grid(pady=(10,10),padx=(10,0),row=0,column=1) 

        with open(USERSPATH+user+".txt") as fileLoader:
            files = [a.rstrip("\n") for a in fileLoader.readlines()]
        del files[0]
        
        for i in range(0,len(files),3):
            mbt.insert("",END,value=(files[i],files[i+1],files[i+2]))

        fileMenu.add_command(label="Save",command=lambda:[self.save(user,mbt)])
        fileMenu.add_separator()
        fileMenu.add_command(label="Log Out",command=lambda:[self.mainscreen.deiconify(),app.destroy()])
        fileMenu.add_command(label="Exit",command=self.closing)
        optionsMenu.add_command(label="About",command=self.aboutScreen)
        optionsMenu.add_command(label="Feedback",command=lambda:wb.get().open("mailto:pythonloginregister@gmail.com"))

        sb = Scrollbar(trvf,orient="vertical",command=mbt.yview)
        sb.pack(side =RIGHT, fill =BOTH)
        mbt.configure(yscrollcommand = sb.set)
        mbt.pack(padx=(25,10),pady=20)

        app.rowconfigure(0,weight=1)
        app.columnconfigure(0, weight=1)
        # self.aboutScreen()

if __name__ == "__main__":
    r = Tk()
    r.withdraw()
    a = Screen(r)
    a.adminScreen("nathan4690")

    r.mainloop()