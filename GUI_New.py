import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Backend_GUI

C_DARK = '#1C2833'
C_GRAY = '#212F3D'
C_LIGHT = '#2c3e50' 
checkSymbol = '✓'
crossSymbol = '✗'

Backend_GUI.ImportJson()
filters = Backend_GUI.filters
_cursor = [None, None]

def selectedFilter():
    return filters[int(_cursor[0])]

class Frames(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Financer")
        self.master.resizable(True, True)
        self.master.tk_setPalette(background=C_GRAY)

        self.master.geometry('1100x700')
        self.xPos = int((self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 8)
        self.yPos = int((self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 10)
        self.master.geometry("+{}+{}".format(self.xPos, self.yPos))

        self.filter_frame = tk.Frame(self.master, name='filter_frame')
        self.filter_frame.pack(side='right', fill='y', pady=25, padx=25)

        self.radio_frame_name = tk.Frame(self.filter_frame, width=25, name='radioframe_n')
        self.radio_frame_name.pack(side='left', fill='y')

        self.name_frame = tk.Frame(self.filter_frame, bd=4, width=150, bg=C_DARK, name='name_frame')
        self.name_frame.pack(side='left', fill='y')

        self.radio_frame_key = tk.Frame(self.filter_frame, width=25, name='radioframe_k')
        self.radio_frame_key.pack(side='left', fill='y')

        self.key_frame = tk.Frame(self.filter_frame, bd=4, width=150, bg=C_DARK, name='key_frame')    
        self.key_frame.pack(side='left', fill='y')

        self.name_label = tk.Label(self.name_frame, text='NAMES', font='Helvetica 16 bold', fg='white', width=15, height=1)
        self.name_label.pack(side='top')

        self.key_label = tk.Label(self.key_frame, text='KEYWORDS', font='Helvetica 16 bold', fg='white', width=15, height=1)
        self.key_label.pack(side='top')

        self.entryFrame_n = tk.Frame(self.name_frame, height=30, name='entry_frame')
        self.entryFrame_n.pack(side='bottom', fill='x')   

        self.entryFrame_k = tk.Frame(self.key_frame, height=30, name='entry_frame')
        self.entryFrame_k.pack(side='bottom', fill='x')  

class Widget:
    def __init__(self):
        self.buildNameMenu()
        entryWidget(app.entryFrame_n)
        entryWidget(app.entryFrame_k)

    def buildNameMenu(self):
        for num in range(len(filters)):
            nameButton(num)
   
    def buildKeyMenu(self):
        for num in range(len(selectedFilter().keywords)):
            keyButton(num)

    def clearFrames(self, *args):
        for frame in args:
            for wdgt in frame.winfo_children():
                if wdgt.winfo_class() == 'Button':
                    wdgt.destroy()
    
    def refreshNames(self):
        self.clearFrames(app.name_frame, app.radio_frame_name)
        self.buildNameMenu()

    def refreshKeys(self):
        self.clearFrames(app.key_frame, app.radio_frame_key)
        self.buildKeyMenu()

    def userPrompt(self):
        root.update()
        if Backend_GUI.Popup(root, pos=_cursor[0]).result():
            filters.pop(_cursor[0]) 
            self.refreshNames()
            self.refreshKeys()

class nameButton(Widget):
    def __init__(self, position, enabled=None):
        self.position = position
        obj = filters[self.position]
        self.name = obj.name
        self.enabled = obj.enabled
        self.selected = False
        if self.enabled:
            self.fogr = 'White'
        else: self.fogr = 'Grey'
        self.customButton()
        nameRadioButton(position=self.position, enabled=self.enabled)

    def __name__(self):
        return 'nameButton'

    def customButton(self):
            button = tk.Button(
                app.name_frame,
                name= f'nameButton{self.position}',
                text=self.name,
                highlightbackground=C_DARK,
                fg=self.fogr,
                highlightthickness=30,
                command= lambda: [f() for f in[ 
                    lambda: button.focus_force(),
                    lambda: self.buttonCommands(),
                    lambda: button.configure(highlightbackground=C_LIGHT),
                    lambda: root.bind('<BackSpace>', lambda event: self.backspaceCommands())
                    ]
                ]
            )
            button.place(
                width=140,
                height=25,
                y=25*self.position+25
            )
    
    def buttonCommands(self):
        _cursor[0] = self.position
        if self.enabled:
            self.refreshKeys()
        else:
            self.clearFrames(app.key_frame, app.radio_frame_key)
        self.resetSelections()

    def backspaceCommands(self):
            # if str(root.focus_get()) == '.':
        self.userPrompt()

    def resetSelections(self):
        for path in app.name_frame.winfo_children():
            path.configure(highlightbackground=C_DARK)

class keyButton(Widget):
    def __init__(self, position:int):
        self.position = position
        self.selected = False
        self.name = selectedFilter().keywords[position]
        self.enabled = selectedFilter().enabledKeyList[position]
        if self.enabled:
            self.fogr = 'White'
        else: self.fogr = 'Grey'
        keyRadioButton(self.position, self.enabled)
        self.customButton()

    def __name__(self):
        return 'keyButton'
        
    def customButton(self):
            button = tk.Button(
                app.key_frame,
                name= f'nameButton{self.position}',
                text=self.name,
                highlightbackground=C_DARK,
                fg=self.fogr,
                highlightthickness=30,
                command= lambda: [f() for f in[ 
                    lambda: button.focus_force(),
                    lambda: self.commands(),
                    lambda: button.configure(highlightbackground=C_LIGHT),
                    lambda: root.bind('<BackSpace>', lambda event: self.backspaceCommands())
                    ]
                ]
            )
            button.place(
                width=140,
                height=25,
                y=25*self.position+25
            )

    def commands(self):
        root.focus_force()
        _cursor[1] = self.position
        self.resetSelections()

    def backspaceCommands(self):
        selectedFilter().popKey(int(_cursor[1]))
        self.refreshKeys()

    def resetSelections(self):
        for path in app.key_frame.winfo_children():
            path.configure(highlightbackground=C_DARK)

class nameRadioButton(nameButton):
    def __init__(self, position, enabled):
        self.position = position
        self.enabled = enabled
        if self.enabled:
            self.custom_radioButton(checkSymbol)
        else: self.custom_radioButton(crossSymbol)

    def custom_radioButton(self, symbol):
        rButton = tk.Button(
            app.radio_frame_name, 
            name=f'check{self.position}',
            text=symbol,
            font = 'Helvetica 16',
            highlightbackground=C_GRAY,
            fg="White",
            highlightthickness=30,
            command= lambda: self.commands()
        )
        rButton.place(
            width=25,
            height=25,
            y=25*self.position+30
        )

    def commands(self):
        filters[self.position].toggleObject()
        self.refreshNames()
        if self.enabled:
            self.clearFrames(app.key_frame, app.radio_frame_key)
        else:
            self.refreshKeys()

class keyRadioButton(keyButton):
    def __init__(self, position, enabled):
        self.position = position
        self.enabled = enabled
        if self.enabled:
            self.custom_radioButton(checkSymbol)
        else: self.custom_radioButton(crossSymbol)

    def custom_radioButton(self, symbol):
        rButton = tk.Button(
            app.radio_frame_key, 
            name=f'check{self.position}',
            text=symbol,
            font = 'Helvetica 16',
            highlightbackground=C_GRAY,
            fg="White",
            highlightthickness=30,
            command= lambda: self.commands()
        )
        rButton.place(
            width=25,
            height=25,
            y=25*self.position+30
        )

    def commands(self):
        selectedFilter().toggleKey(self.position)
        self.refreshKeys()

class entryWidget(Widget):
    def __init__(self, frame):
        self.var = tk.StringVar()
        self._frame = frame
        self.addButton()
        self.myEntry()

    def addButton(self):
        add_button = tk.Button(
            self._frame,
            height=1,
            width=2,
            text='+',
            font='Helvetica 16 bold',
            highlightbackground=C_LIGHT,
            fg="White",
            highlightthickness=30,
            activeforeground='red',
            command= lambda: self.command()
        )
        add_button.place(width=30, height=30, anchor='nw')

    def myEntry(self):
        self._entry = tk.Entry(
            self._frame,
            width=11,
            textvariable=self.var,
            exportselection=0,
            selectborderwidth=2
            )
        self._entry.pack(side='right', anchor='ne')
        self._entry.bind('<Return>', lambda event: self.command())

    def is_Key(self):
        if self._frame == app.entryFrame_n:
            return False
        elif self._frame == app.entryFrame_k:
            return True
        else: raise UnboundLocalError('Unknown entryframe')

    def clearEntry(self):
        self._entry.delete(0,'end')

    def command(self):
        if self.is_Key():
            selectedFilter().appendKey(self.var.get().capitalize())
            self.refreshKeys()
        else:
            Backend_GUI.appendObject(self.var.get().capitalize())
            self.refreshNames()
        self.clearEntry()

if __name__ == "__main__":
    root = tk.Tk()
    app = Frames(root)
    Widget()
    app.mainloop()


def TODO():
    '''
    - Focus mixup fix: when user focuses on the entry the tkinter 'focus_get' isnt being updated.
    - Backend: The changes should be prompted to be saved, and implement a 'save' button to update the changes to the JSON file
    - Integrate the new Filter object in the PDF parser file
    - Make an option for an income filter
    - Append an 'others' filter:
        self.filters.append({'name': 'Other', 'name_key' : [], 'transactions' : [], 'totals' : None})
        self.filters.append({'name': 'Income', 'kind_key' : 'Overschrijving', 'transactions' : [], 'totals' : None})
    '''