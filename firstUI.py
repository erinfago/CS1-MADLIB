#################################
# firstUI.py
# Creates lablib game w/ Tkinter
#################################


# import modules
import tkinter as tk
import ttk
from tkinter.messagebox import askokcancel
import tkinter.filedialog as tkdl


class mainScreen(tk.Frame):
    # create the constructor
    def __init__(self, parent = None):
        # create a frame that is used for the main screen

        tk.Frame.__init__(self, parent)
        
        # initialize the game by creating global variables & calling functions 
        self.grid()
        self.config(bg = "#ffffff")
        self.countDict = {}
        self.parent = parent
        self.parent.title("Fun with Mad Libs!")
        self.wordlist = []
        self.cleanwordlist = []
        self.centerWindow()
        self.mainButtons()    
        

    # centers the window on the screen
    def centerWindow(self):
        
        w= 750
        h = 592
        # get the screen dim
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        #adjust the position according to the dim
        self.parent.geometry('%dx%d+%d+%d' % (w,h,x,y))

    
    # creates labels and buttons on the frame
    def mainButtons(self):
        #create the themes
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.configure(bg = 'white')
        
        #make a label
        label1 = tk.Label(self, text="Select a Mad Lib!",font = "Impact 16 bold")
        label1.config(bg = "cyan")
        label1.grid(row = 0, sticky = tk.W) 

        # list of possible files (with MadLibs inside) for the user to choose
        madLibs = ['ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6']

        #create the buttons to select madlibs
        i = 0
        while i < len(madLibs):
            but = ttk.Button(self, text = madLibs[i], command =lambda i=i:  self.selectML(madLibs[i][2]))
            
            but.config(width = 30)
            but.grid(row = 1 + i,column = 0)
            i += 1
            
        # create a close button to end game
        closeButton = ttk.Button(self, text="Quit Game", command = self.quit)
        closeButton.grid(row = 0, column = 7,padx = 5, pady = 5, sticky = tk.SE)
        
        # create a continue button: 
        # when user enters words- entries are sent to inputs to be integrated 
        continueButton = ttk.Button(self, text="Continue", command = lambda: self.inputs())
        continueButton.grid(row = 0, column = 8, sticky = tk.SW, padx = 5, pady = 5)


        
        ###############################
        
    # create conditions for which madlib can be selected
        # then send information to getType method
    def selectML(self, txt):

        if txt == "1":
            self.infileName = "ML1.txt"
            self.getType()
        elif txt == "2":
            self.infileName = "ML2.txt"
            self.getType()
        elif txt =="3":
            self.infileName = "ML3.txt"
            self.getType()
        elif txt == "4":
            self.infileName = "ML4.txt"
            self.getType()
        elif txt == "5":
            self.infileName = "ML5.txt"
            self.getType()
        elif txt == "6":
            self.infileName = "ML6.txt"
            self.getType()
    
    # go in to the file the user selected and make a dictionary
        # keys   = a key word 
        # values = the # of occurances in file 
    def getType(self):
               
        # list of keywords
        listterms = ["ADJ","VERB", "NOUN", "PLACE", "NUM", "PLURALNOUN", "VERBING", "VERBED", "BODYPART", "ADVERB", "PLURALGROUPNAME", "COLOR", "ANIMAL", "NAME", "NUMBER", "COLOR", "SHAPE", "BODPART"]

        # open file to read
        self.infile = open(self.infileName, "r")
        
        # create two empty lists to break the file down into words 
        linelist = []

        keylist = []
        
        # read the file and get it into a useful form
        for line in self.infile:
            linelist.append(line.strip('\n'))
        for sents in linelist:
            self.wordlist.append(sents.split())
        for item in self.wordlist:
            for obj in item:
                # clean up the words
                new = obj.replace("?","")
                new = new.replace("!","")
                new = new.replace(".","")
                new = new.replace(",","")
                new = new.replace("'","")
                new = new.replace(";","")
                new = new.replace("\"","") 
                new = new.replace("-", "")
                new = new.replace("-", "")
                new = new.replace(".\"", "")
                new = new.replace("\'", "")
                new = new.replace("\n", "")
                if new.upper() == new:
                    self.cleanwordlist.append(new)

        # thing is a word string in the list of lists... ran out of var names
        for thing in self.cleanwordlist:
            if thing in self.countDict.keys():
                self.countDict[thing] += 1
            else:
                if thing in listterms:
                    self.countDict[thing] = 1
        self.inputs()
        return True
        # this now works for all files. make sure ALL KEYWORDS are in listterms
        # exactly as they appear or else this will not work
        

    # makes entry boxes appear when mad lib is selected from buttons
    def inputs(self):
        
        # acc created to format entry box's row on grid
        acc = 1
        self.entrylist = []
        # value number of times for each key:
        # a entry box with the title of the key should be printed
        for j in range(len(self.countDict)):
            num = self.countDict[list(self.countDict.keys())[j]]
            for i in range(num):
                # labels
                L1 = tk.Label(self, text=list(self.countDict.keys())[j])
                L1.config(bg = 'cyan')
                L1.grid(row = acc, column = 2, padx = 2, pady = 2)
                # entries
                self.E1 = tk.Entry(self)
                self.E1.grid(row = acc, column = 3, padx = 2, pady = 2)
                
                acc +=1
                self.entrylist.append((list(self.countDict.keys())[j],self.E1))

        # once inputted, user presses continue button
        # elist = tuple of label and entry obj that is updated w/ user input
        continueButton = ttk.Button(self, text="Continue", command = lambda: self.combine(self.entrylist)) # this calls combine with par. (label, entry obj)
        continueButton.grid(row = 0, column = 8, sticky = tk.SW, padx = 5, pady = 5)


    # combines user input and file
    # replaces the key words in the file with the corresponding user input
    def combine(self,elist):  # elist = (label, entry obj)
        

        # go through the file contents list created earlier
        for n in range(len(self.wordlist)):
            for j in range(len(self.wordlist[n])):
                for i in range(len(elist)):
                    
                    # if word = keyword, replace with respective entry
                    if elist[i][0] == self.wordlist[n][j] or elist[i][0] == self.wordlist[n][j][0:-1]:

                        self.wordlist[n][j]= elist[i][1].get()
                        elist.pop(i)
                        # break the inner most for loop
                        break
        
        # instead of having a list here we convert it to a string
        self.fnlStr = ""
        for item in self.wordlist:
            for i in range(0, len(item)+2, 8):
                item.insert(i, "\n")
        for line in self.wordlist:
            for word in line:
                self.fnlStr += word + " "

        self.printOut()
        #completed story (the string) is sent back to tkinter to a new window 
        
        ##############################
    def printOut(self):

        newWin = tk.Toplevel(self)
        newWin.title("Completed Mad Lib")
        w= 750
        h = 550
        # get the screen dim
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        #adjust the position according to the dim
        newWin.geometry('%dx%d+%d+%d' % (w,h,x,y))
        
        canvas = tk.Canvas(newWin)
        canvas.config(bg = "white")
        cid = canvas.create_text(225, 170, anchor = tk.W, font = "Prussia")
        canvas.itemconfig(cid, text = self.fnlStr)
        canvas.insert(cid, 12, "")
        
        canvas.pack(fill = tk.BOTH, expand = 1)
        
        



# main function calls/ drives the rest of the function
def main():
  
    root = tk.Tk()
    root.config(bg = "white")
    app = mainScreen(root)
    root.mainloop()  
    

# calling the main function
if __name__ == '__main__':
    main()
