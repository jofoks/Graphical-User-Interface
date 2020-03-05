import json
import tkinter as tk

jsonDir = "GUI_ING/filters.json"
filters = []

def appendObject(name):
    if name not in [x.name.capitalize() for x in filters]:
        filters.append(
            Fltr(
            position=len(filters)+1,
            name = name
        ) )
        filters[-1]._update()
    else: print( ValueError('Keyword already exists'))

class Popup(tk.Toplevel):
    def __init__(self, parent, pos):
        parent.update()
        tk.Toplevel.__init__(self, parent)
        self.inp = tk.BooleanVar()
        self.transient(parent)
        self.title('Caution')
        self.parent = parent
        self.buttonbox()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_width()/2,
                                  parent.winfo_height()/2))
        self.geometry('200x75')

    def buttonbox(self):
        l = tk.Label(self, text="Delete this filter?", font='Helvetica 14 bold')
        l.pack(side='top', pady=5)
        self.a = tk.Button(self,
                    name='yes',
                    text="Yes",
                    fg='white',
                    highlightthickness=30,
                    highlightbackground='#1C2833',
                    command=self.yes,
                    default='active')
        self.a.place(width=92, height=30, x=5, y=40)
        self.b = tk.Button(self,
                    name='cancel',
                    text="Cancel",
                    fg='white',
                    highlightthickness=30,
                    highlightbackground='#1C2833',
                    command=self.cancel)
        self.b.place(width=92, height=30, x=105, y=40)
        self.bind('<Return>',lambda event: self.onReturn())
        self.bind("<Escape>", lambda event: self.cancel())
        self.bind('<Left>', lambda event: self.onArrow(self.a))
        self.bind('<Right>', lambda event: self.onArrow(self.b))

    def onArrow(self, _button):
        self.a.configure(highlightbackground='#1C2833')
        self.b.configure(highlightbackground='#1C2833')
        _button.focus_force()
        _button.configure(highlightbackground='#2c3e50')

    def onReturn(self):
        if str(self.focus_get()) == '.!popup.yes':
            self.inp.set(True)
        else: self.inp.set(False)

    def yes(self):
        self.inp.set(True)

    def cancel(self):
        self.inp.set(False)

    def result(self):
        self.wait_variable(self.inp)
        self.parent.focus_set()
        self.destroy()
        return self.inp.get()

class Fltr(object):
    def __init__(self, position, name, keywords_tup=[], enabled=True):
        self.name = name
        self.keywords_tup = keywords_tup
        self.enabled = enabled
        self.position = position
        self._update()

    def _update(self):
        self.keywords = [value[0] for value in self.keywords_tup]
        self.enabledKeyList = [value[1] for value in self.keywords_tup]
    
    def __repr__(self):
        print(f'\nFltr: {self.name} --> #{self.position}\nKeywords (tuple): {self.keywords_tup}\n')

    def appendKey(self, newName):
        if newName not in [x.capitalize() for x in self.keywords]:
            self.keywords_tup.append([newName, True])
            self._update()
        else: print( ValueError('Keyword already exists'))

    def popKey(self, pos):
        del self.keywords_tup[pos]
        self._update()
    
    def toggleObject(self):
        self.enabled = not self.enabled

    def toggleKey(self, pos):
        self.enabledKeyList[pos] = not self.enabledKeyList[pos]
        return self.enabledKeyList[pos]
    
    def is_key_enabled(self, key):
        keyPosition = self.keywords.index(key)
        return self.enabledKeyList[keyPosition]

class ImportJson:
    def __init__(self):
        self.parseContence(filters)

    def openFile(self):
        with open(jsonDir) as jsonFile:
            data = json.load(jsonFile)
            contence = [None] * len(data)
            for num, item in enumerate(data):
                contence[num] = item
        return contence

    def parseContence(self, lst):
        for num, item in enumerate(self.openFile()):
            lst.append(
                Fltr(
                    position = num,
                    name = item['name'],
                    keywords_tup = item['keywords'],
                    enabled = item['enable']
                )
            )

def main():
    pass

if __name__ == "__main__":
    main()

class ExportJson:
    '''
    # Get all the information and append create a new JSON, append idles to a new list in a filter
    def getDict(self):
        pass
        # Get the titles
        # def getKeywords(self, title):
        #     print()
        #     pass
        #     # Get the keywords of that title
        
        # def getIdleKeys(self, title):
        #     print()
        #     pass

    def saveToJSON(self, dict, idleKeys):
        # Write JSON file with the added idleKeys list
        pass
    '''
