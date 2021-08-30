from tkinter import *
from tkinter import messagebox,font,ttk
from os.path import abspath,dirname
from CodeModule import En_de
from PIL import Image, ImageTk
import webbrowser as wb

USERSPATH = (abspath(dirname(__file__)) + "\\users\\")[0].upper() + (abspath(dirname(__file__)) + "\\users\\")[1:]

class CheckboxTreeview(ttk.Treeview):
    """
        Treeview widget with checkboxes left of each item.
        The checkboxes are done via the image attribute of the item, so to keep
        the checkbox, you cannot add an image to the item.
    """

    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        # checkboxes are implemented with pictures
        a = Image.open(USERSPATH+'checked.png')
        wi,he = a.size;rat = 1
        # a.resize((wi//rat,he//rat))
        self.im_checked = ImageTk.PhotoImage(a,size=(wi//rat,he//rat))
        b = Image.open(USERSPATH+'unchecked.png')
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
        """ check the boxes of item's descendants """
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


def closing():
    confirm = messagebox.askyesnocancel("Quit","Are you really want to quit?")
    if confirm:
        exit()

def initialize(screen,title,sx,sy,close=False,rat=2):
    screen.title(title)
    screen.geometry(f"{sx}x{sy}+{int(mainscreen.winfo_screenwidth()/rat - sx/2)}+{int(mainscreen.winfo_screenheight()/rat - sy/2)}")
    screen.resizable(False,False)

    if close:
        screen.protocol("WM_DELETE_WINDOW",closing)
    else:
        screen.protocol("WM_DELETE_WINDOW",lambda:[mainscreen.deiconify(),screen.destroy()])

def save(u,t):
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

def packToTree(t,wr,bo,pu,b,w,p):
    if b and w and p:
        t.insert("",END,values=(str(b),str(w),str(p)))
        wr.delete(0,END)
        bo.delete(0,END)
        pu.delete(0,END)
    else:
        messagebox.showwarning("NoneError","Not enough data to add. Please try again")

def deletesome(t):
    x = []
    for i in t.get_children():
        if "checked" in t.item(i)["tags"] and i not in x:
            x.append(i)

    if len(x) > 0:
        for r in x:
            t.delete(r)
    else:
        messagebox.showwarning("NoneSelected","No selected item(s), try again")

def searchOnline(treeViewObject: ttk.Treeview):
    listSelection = []
    for i in treeViewObject.get_children():
        if "checked" in treeViewObject.item(i)["tags"] and i not in listSelection:
            listSelection.append(i)

    if len(listSelection) > 1:
        messagebox.showwarning("TooManyArguments","Too many books selected, please try again")
    elif len(listSelection) == 0:
        messagebox.showwarning("NoneSelected","No selected item(s), please try again")
    else:
        bookName = treeViewObject.item(listSelection[0])["values"][0]
        wb.get().open("https://www.google.com/search?tbm=bks&q=" + bookName)

def editBook():
    messagebox.showerror("NotImplementedError","Sorry, this function haven't been implemented yet.") 
    raise NotImplementedError
seeBookContent = editBook

def adminScreen(user):
    app = Toplevel(mainscreen)
    initialize(app,"Book Viewer: " + str(user),1000,600,True)
    ico = PhotoImage(file=USERSPATH+'book.png')
    app.tk.call('wm', 'iconphoto', app._w, ico)
    menu = Menu(app)
    app.config(menu=menu)

    fileMenu = Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)

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
    pe.bind("<Return>",lambda event=None: packToTree(mbt,be,we,pe,bn.get(),wt.get(),pl.get()))

    ttk.Button(elblf,text="Add item",command=lambda: packToTree(mbt,be,we,pe,bn.get(),wt.get(),pl.get())).grid(row=3,column=0,pady=(0,10))
    ttk.Button(elblf,text="Remove Selected Item(s)",command=lambda:[deletesome(mbt)]).grid(row=3,column=1,pady=(0,10))

    mlblf = LabelFrame(app,relief="groove",text="More Book Details")
    mlblf.pack(anchor="w",padx=20,fill="x")

    online_search = ttk.Button(mlblf,text="Search this book online (Google)",command=lambda: searchOnline(mbt))
    online_search.grid(padx=(10,0),pady=(10,0))
    bookContentViewButton = ttk.Button(mlblf,text="View Selected Book's Content",command=lambda: editBook())
    bookContentViewButton.grid(padx=(10,0))
    bookContentEditButton = ttk.Button(mlblf,text="Edit Selected Book's Content",command=lambda: seeBookContent())
    bookContentEditButton.grid(pady=(0,10),padx=(10,0))

    with open(USERSPATH+user+".txt") as fileLoader:
        files = [a.rstrip("\n") for a in fileLoader.readlines()]
    del files[0]
    
    for i in range(0,len(files),3):
        mbt.insert("",END,value=(files[i],files[i+1],files[i+2]))

    fileMenu.add_command(label="Save",command=lambda:[save(user,mbt)])
    fileMenu.add_command(label="Exit",command=closing)

    sb = Scrollbar(trvf,orient="vertical",command=mbt.yview)
    sb.pack(side =RIGHT, fill =BOTH)
    mbt.configure(yscrollcommand = sb.set)
    mbt.pack(padx=(25,10),pady=20)

    app.rowconfigure(0,weight=1)
    app.columnconfigure(0, weight=1)

def checkloginstate(s,ue,pe,u,p):
    try:
        open(USERSPATH+(u)+".txt")
    except:
        messagebox.showwarning("Wrong Username","Wrong username, please try again")
        Label(s,text="Wrong Username",fg="red").grid(row=8)
        ue.delete(0,END)
        pe.delete(0,END)
    else:
        with open(USERSPATH+(u)+".txt") as checker:
            checking = [a.rstrip("\n") for a in checker.readlines()]
        if checking[0] == En_de(p):
            s.destroy()
            adminScreen(u)
        else:
            messagebox.showwarning("Wrong Password","Wrong Password, please try again")
            Label(s,text="Wrong Password",fg="red").grid(row=8)
            ue.delete(0,END)
            pe.delete(0,END)

def login():
    mainscreen.withdraw()
    logscreen = Toplevel(mainscreen)
    initialize(logscreen,"Login",450,300)

    loginusername = StringVar()
    loginpassword = StringVar()
    Label(logscreen,text="").grid(row=0)
    Label(logscreen,text="").grid(row=1)
    Label(logscreen,text="").grid(row=2,column=0)
    Label(logscreen,text="").grid(row=3,column=0)

    Label(logscreen,text="Username: ").grid(row=4,column=0)
    uent = ttk.Entry(logscreen,textvariable=loginusername)
    uent.grid(row=4,column=1)

    Label(logscreen,text="Password: ").grid(row=5,column=0)
    pent = ttk.Entry(logscreen,textvariable=loginpassword,show="*")
    pent.grid(row=5,column=1)
    pent.bind("<Return>",lambda event=None:[checkloginstate(logscreen,uent,pent,loginusername.get(),loginpassword.get())])

    Label(logscreen).grid(row=6)

    ttk.Button(logscreen,text="Login",command=lambda:[checkloginstate(logscreen,uent,pent,loginusername.get(),loginpassword.get())]).grid(row=7)

    lf = Frame(logscreen,bg="gray",width=450,height=75)
    lf.place(x=0,y=0)
    lf.pack_propagate(False) 
    lfont = font.Font(family="Times New Roman",size=20)
    Label(lf,text="Login",bg="gray",fg="white",font=lfont).place(x=190,y=15)

def registeruser(s,u,p):
    try:
        open(USERSPATH+u+".txt")
    except:
        with open(USERSPATH+u+".txt","w") as re:
            re.write(En_de(p) + "\n")
        messagebox.showinfo("Registration","Successfully registered user " + u)
        mainscreen.deiconify()
        s.destroy()
    else:
        Label(s,text="User Already",fg="red").grid(row=8)
        Label(s,text="Registered",fg="red").grid(row=9)

def register():
    mainscreen.withdraw()
    rescreen = Toplevel(mainscreen)
    initialize(rescreen,"Register",450,300)

    reusername = StringVar()
    repassword = StringVar()
    Label(rescreen,text="").grid(row=0)
    Label(rescreen,text="").grid(row=1)
    Label(rescreen,text="").grid(row=2,column=0)
    Label(rescreen,text="").grid(row=3,column=0)

    Label(rescreen,text="Username: ").grid(row=4,column=0)
    Entry(rescreen,textvariable=reusername).grid(row=4,column=1)

    Label(rescreen,text="Password: ").grid(row=5,column=0)
    Entry(rescreen,textvariable=repassword).grid(row=5,column=1)

    Label(rescreen).grid(row=6)

    Button(rescreen,text="Register",width=10,command=lambda:[
        registeruser(rescreen,reusername.get(),repassword.get())
    ]).grid(row=7)

    lf = Frame(rescreen,bg="gray",width=450,height=75)
    lf.place(x=0,y=0)
    lf.pack_propagate(False) 
    lfont = font.Font(family="Times New Roman",size=20)
    Label(lf,text="Register",bg="gray",fg="white",font=lfont).place(x=180,y=15)

def main():
    global mainscreen
    mainscreen = Tk()
    mainscreen.title("Application v1.0")
    mainscreen.geometry("450x350")
    
    mainscreen.geometry("450x350+{}+{}".format(int(mainscreen.winfo_screenwidth()/2 - 450/2), int(mainscreen.winfo_screenheight()/2 - 350/2)))
    mainscreen.resizable(False,False)

    af = Frame(mainscreen,bg="gray",width=450,height=75)
    af.pack()
    af.pack_propagate(False) 
    afont = font.Font(family="Times New Roman",size=20)
    Label(af,text="Application v1.0",bg="gray",fg="white",font=afont).pack(side="top",pady=20)
    
    Button(mainscreen,text="Login",width=50,height=5,command=login).pack(pady=20)
    Button(mainscreen,text="Register",width=50,height=5,command=register).pack(pady=20)

    mainscreen.protocol("WM_DELETE_WINDOW",closing)
    mainscreen.mainloop()

if __name__ == "__main__":
    main()