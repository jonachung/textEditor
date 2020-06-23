from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class TextEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("1200x700+200+150")
        self.filename = None
        self.title = StringVar()

        #Create title bar (title of file)
        self.titlebar = Label(self.root, textvariable=self.title, font=("ariel",15,"bold"),bd=2,relief=GROOVE)
        self.titlebar.pack(side=TOP,fill=BOTH)
        self.settitle()

        #Creating Menu Bar
        self.menubar = Menu(self.root, font=("ariel",15,"bold"), activebackground="skyblue")
        self.root.config(menu=self.menubar)

        #file menu
        self.filemenu = Menu(self.menubar, font=("ariel", 15, "bold"),activebackground="skyblue",tearoff=0)

        # New file command
        self.filemenu.add_command(label="New",accelerator="Ctrl+N", command=self.newfile)
        # Open file command
        self.filemenu.add_command(label="Open",accelerator="Ctrl+O", command=self.openfile)
        #Save File command
        self.filemenu.add_command(label="Save",accelerator="Ctrl+S", command=self.savefile)
        # Save As File command
        self.filemenu.add_command(label="Save As",accelerator="Ctrl+A", command=self.saveasfile)
        self.filemenu.add_separator()
        # Exit window command
        self.filemenu.add_command(label="Exit",accelerator="Ctrl+E", command=self.exit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.menubar,font=("ariel",15,"bold"),activebackground="skyblue",tearoff=0)
        # Adding Cut text Command
        self.editmenu.add_command(label="Cut",accelerator="Ctrl+X",command=self.cut)
        # Adding Copy text Command
        self.editmenu.add_command(label="Copy",accelerator="Ctrl+C",command=self.copy)
        # Adding Paste text command
        self.editmenu.add_command(label="Paste",accelerator="Ctrl+V",command=self.paste)
        self.editmenu.add_separator()
        # Adding Undo text Command
        self.editmenu.add_command(label="Undo",accelerator="Ctrl+U",command=self.undo)

        # Cascading editmenu to menubar
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        # Creating Help Menu
        self.helpmenu = Menu(self.menubar,font=("ariel",15,"bold"),activebackground="skyblue",tearoff=0)
        # Adding About Command
        self.helpmenu.add_command(label="About",command=self.infoabout)
        # Cascading helpmenu to menubar
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        # Creating Scrollbar
        scrol_y = Scrollbar(self.root,orient=VERTICAL)

        # Creating Text Area
        self.txtarea = Text(self.root,yscrollcommand=scrol_y.set,font=("ariel",15,"bold"),state="normal",relief=GROOVE)
        # Packing scrollbar to root window
        scrol_y.pack(side=RIGHT,fill=Y)
        # Adding Scrollbar to text area
        scrol_y.config(command=self.txtarea.yview)
        # Packing Text Area to root window
        self.txtarea.pack(fill=BOTH,expand=1)
        # Calling shortcuts funtion
        self.shortcuts()

    # Defining settitle function
    def settitle(self):
        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")

    # Defining New file Function
    def newfile(self,*args):
        self.txtarea.delete("1.0",END)
        self.filename = None
        self.settitle()

    # Defining Open File Funtion
    def openfile(self,*args):
        try:
            self.filename = filedialog.askopenfilename(title = "Select file",filetypes = (("All Files","*.*"),("Text Files","*.txt")))
            if self.filename:
                infile = open(self.filename,"r")
                self.txtarea.delete("1.0",END) # clear text
                for line in infile:
                    self.txtarea.insert(END,line)
                infile.close()
                self.settitle()
        except Exception as e:
            messagebox.showerror("Exception",e)

    # Defining Save File Funtion
    def savefile(self,*args):
        try:
            if self.filename:
                data = self.txtarea.get("1.0",END)
                outfile = open(self.filename,"w")
                outfile.write(data)
                outfile.close()
                self.settitle()
            else:
                self.saveasfile()
        except Exception as e:
            messagebox.showerror("Exception",e)

    # Defining Save As File Funtion
    def saveasfile(self,*args):
        try:
            untitledfile = filedialog.asksaveasfilename(title = "Save file As",defaultextension=".txt",initialfile = "Untitled.txt",filetypes = (("All Files","*.*"),("Text Files","*.txt")))
            data = self.txtarea.get("1.0",END)
            outfile = open(untitledfile,"w")
            outfile.write(data)
            outfile.close()
            self.filename = untitledfile
            self.settitle()
        except Exception as e:
            messagebox.showerror("Exception",e)

    # Defining Exit Funtion
    def exit(self,*args):
        op = messagebox.askyesno("WARNING","Your Unsaved Data May be Lost!!")
        if op>0:
            self.root.destroy()
        else:
            return

    # Defining Cut Funtion
    def cut(self,*args):
        self.txtarea.event_generate("<<Cut>>")

    # Defining Copy Funtion
    def copy(self,*args):
            self.txtarea.event_generate("<<Copy>>")

    # Defining Paste Funtion
    def paste(self,*args):
        self.txtarea.event_generate("<<Paste>>")

    # Defining Undo Funtion
    def undo(self,*args):
        try:
            if self.filename:
                self.txtarea.delete("1.0",END)
                infile = open(self.filename,"r")
                for line in infile:
                    self.txtarea.insert(END,line)
                infile.close()
                self.settitle()
            else:
                self.txtarea.delete("1.0",END)
                self.filename = None
                self.settitle()
        except Exception as e:
            messagebox.showerror("Exception",e)

    # Defining About Funtion
    def infoabout(self):
        messagebox.showinfo("About Text Editor","A Simple Text Editor\nCreated using Python.\n\nMade by Jonathan Hung")
    
    # Defining shortcuts Funtion
    def shortcuts(self):
        self.txtarea.bind("<Control-n>",self.newfile)
        self.txtarea.bind("<Control-o>",self.openfile)
        self.txtarea.bind("<Control-s>",self.savefile)
        self.txtarea.bind("<Control-a>",self.saveasfile)
        self.txtarea.bind("<Control-e>",self.exit)
        self.txtarea.bind("<Control-x>",self.cut)
        self.txtarea.bind("<Control-c>",self.copy)
        self.txtarea.bind("<Control-v>",self.paste)
        self.txtarea.bind("<Control-u>",self.undo)


# Creating TK Container
root = Tk()
TextEditor(root)
root.mainloop()
