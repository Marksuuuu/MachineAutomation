
import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)



        self.GLabel_61=tk.Label(root)
        self.GLabel_61["bg"] = "#999999"
        self.ft = tkFont.Font(family='Times',size=24)
        self.GLabel_61["font"] = self.ft
        self.GLabel_61["fg"] = "#333333"
        self.GLabel_61["justify"] = "center"
        self.GLabel_61["text"] = "label"
        self.GLabel_61["relief"] = "sunken"
        self.GLabel_61.place(x=0,y=0,width=601,height=208)

        self.GLineEdit_172=tk.Entry(root)
        self.GLineEdit_172["bg"] = "#999999"
        self.GLineEdit_172["borderwidth"] = "1px"
        self.GLineEdit_172["disabledforeground"] = "#000000"
        self.ft = tkFont.Font(family='Times',size=28)
        self.GLineEdit_172["font"] = self.ft
        self.GLineEdit_172["fg"] = "#333333"
        self.GLineEdit_172["justify"] = "center"
        self.GLineEdit_172["text"] = "Entry"
        self.GLineEdit_172.place(x=80,y=320,width=439,height=147)

        self.GLabel_60=tk.Label(root)
        self.GLabel_60["bg"] = "#1f93ff"
        self.ft = tkFont.Font(family='Times',size=13)
        self.GLabel_60["font"] = self.ft
        self.GLabel_60["fg"] = "#333333"
        self.GLabel_60["justify"] = "center"
        self.GLabel_60["text"] = "label"
        self.GLabel_60.place(x=220,y=220,width=161,height=78)


        def countdown(count):
            # change text in label        
            self.GLabel_60['text'] = count

            if count > 0:
                # call countdown again after 1000ms (1s)
                root.after(1000, 10, count-1)

        self.root = tk.Tk()

        self.label = tk.Label(self)
        self.label.place(x=35, y=15)

        # call countdown first time    
        # root.after(0, countdown, 5)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
