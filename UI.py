import tkinter as tk
from tkinter.filedialog import *
from RSA_CBC import CBC

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master=None)
        self.grid()
        self.createWidgets()
        self.rsa_cbc = CBC()

    def createWidgets(self):
        self.Label = Label(self, text='')
        self.Label.grid(row=0, column=0)

        self.FileLabel = tk.Label(self, text='文件:', width=10)
        self.Filev = StringVar()
        self.FileEntry = Entry(self, textvariable=self.Filev, width=60)
        self.FileButton = Button(self, text='....', command=self.funcOpen1)
        self.FileLabel.grid(row=1, column=0, sticky=tk.E)
        self.FileEntry.grid(row=1, column=1, columnspan=5)
        self.FileButton.grid(row=1, column=6)

        self.PubLabel = Label(self, text='公钥:', width=10)
        self.Pubv = StringVar()
        self.PubEntry = Entry(self, textvariable=self.Pubv, width=60)
        self.PubButton = Button(self, text='....', command=self.funcOpen2)
        self.PubLabel.grid(row=2, column=0, sticky=tk.E)
        self.PubEntry.grid(row=2, column=1, columnspan=5)
        self.PubButton.grid(row=2, column=6)

        self.PrivateLabel = Label(self, text='私钥:', width=10)
        self.Privatev = StringVar()
        self.PrivateEntry = Entry(self, textvariable=self.Privatev, width=60)
        self.PrivateButton = Button(self, text='....', command=self.funcOpen3)
        self.PrivateLabel.grid(row=3, column=0, sticky=tk.E)
        self.PrivateEntry.grid(row=3, column=1, columnspan=5)
        self.PrivateButton.grid(row=3, column=6)

        v = StringVar()
        self.Label = Label(self, text='', textvariable=v)
        self.Label.grid(row=4, column=0)
        self.gen_keysButton = Button(self, text='生成密钥', command=self.gen_keys)
        self.gen_keysButton.grid(row=6, column=2)
        self.encrypt_Button = Button(self, text='加密', command=self.encrypt)
        self.encrypt_Button.grid(row=6, column=3)
        self.decrypt_Button = Button(self, text='解密', command=self.decrpyt)
        self.decrypt_Button.grid(row=6, column=4)

    def funcOpen1(self):
        fname = askopenfilename()
        self.Filev.set(fname)

    def funcOpen2(self):
        fname = askopenfilename()
        self.Pubv.set(fname)

    def funcOpen3(self):
        fname = askopenfilename()
        self.Privatev.set(fname)

    def gen_keys(self):
        file = asksaveasfilename()
        self.rsa_cbc.gen_keys(file)
        self.Pubv.set(file + '.pub')
        self.Privatev.set(file + '.key')

    def encrypt(self):
        Pfile = self.Filev.get()
        keysFile = self.Pubv.get()
        Cfile = asksaveasfilename()
        self.rsa_cbc.encrypt(Pfile, Cfile, keysFile)

    def decrpyt(self):
        Cfile = self.Filev.get()
        Pfile = asksaveasfilename()
        keysFile = self.Privatev.get()
        self.rsa_cbc.decrypt(Pfile, Cfile, keysFile)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('RSA')
    center_window(root, 300, 240)
    root.maxsize(555, 200)
    root.minsize(555, 200)
    app = Application(master=root)
    app.mainloop()
