from tkinter import *
from tkinter import messagebox,font,ttk
from os.path import abspath,dirname
from CodeModule import En_de 
import userScreen

USERSPATH = (abspath(dirname(__file__)) + "\\users\\")[0].upper() + (abspath(dirname(__file__)) + "\\users\\")[1:]
BOOKFILESPATH = abspath(dirname(__file__)) + "\\books\\"

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
            ad.adminScreen(u)
        else:
            messagebox.showwarning("Wrong Password","Wrong Password, please try again")
            Label(s,text="Wrong Password",fg="red").grid(row=8)
            ue.delete(0,END)
            pe.delete(0,END)

def login():
    mainscreen.withdraw()
    logscreen = Toplevel(mainscreen)
    ad.initialize(logscreen,"Login",450,300)

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
    
    photo = PhotoImage(file = userScreen.RESOURCESPATH + "back.png")
    photo = photo.subsample(18)
    picLabel = Label(lf,image=photo,bg="gray",fg="white")
    picLabel.place(x=0,y=0)

    picLabel.bind("<Button-1>",lambda event:[mainscreen.deiconify(),logscreen.destroy()])
    picLabel.bind("<Enter>",lambda event: picLabel.config(cursor="hand2"))
    mainloop()

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
    ad.initialize(rescreen,"Register",450,300)

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

    photo = PhotoImage(file = userScreen.RESOURCESPATH + "back.png")
    photo = photo.subsample(18)
    picLabel = Label(lf,image=photo,bg="gray",fg="white")
    picLabel.place(x=0,y=0)

    picLabel.bind("<Button-1>",lambda event:[mainscreen.deiconify(),rescreen.destroy()])
    picLabel.bind("<Enter>",lambda event: picLabel.config(cursor="hand2"))
    mainloop()

def main():
    global mainscreen,ad
    mainscreen = Tk()
    ad = userScreen.Screen(mainscreen=mainscreen)
    mainscreen.title("Application v1.0")
    mainscreen.geometry("450x350")
    
    mainscreen.geometry("450x350+{}+{}".format(int(mainscreen.winfo_screenwidth()/2 - 450/2), int(mainscreen.winfo_screenheight()/2 - 350/2)))
    mainscreen.resizable(False,False)

    af = Frame(mainscreen,bg="gray",width=450,height=75)
    af.pack()
    af.pack_propagate(False) 
    afont = font.Font(family="Times New Roman",size=20)
    Label(af,text="Book Viewer v1.1",bg="gray",fg="white",font=afont).pack(side="top",pady=20)
    
    Button(mainscreen,text="Login",width=50,height=5,command=login).pack(pady=20)
    Button(mainscreen,text="Register",width=50,height=5,command=register).pack(pady=20)

    mainscreen.protocol("WM_DELETE_WINDOW",ad.closing)
    mainloop()

if __name__ == "__main__":
    main()