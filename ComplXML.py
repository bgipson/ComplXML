#!/usr/bin/env python3
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import traceback
#ComplXML - The LC-3 Test XML Maker
#Created by Brandon Gipson
import os
class mainGUI:
    def __init__(self,rootWin):
        self.rootWin = rootWin
        rootWin.title("ComplXML")
        self.testCaseList = []
        self.testCasePointer = None
        self.expanded = False
        self.counter = IntVar()

        
        testNameLabel = Label(rootWin,text = "Enter the name of your Test Case: ")
        self.testNameString = StringVar()
        testNameEntry = Entry(rootWin, textvariable=self.testNameString)
        makeTestCaseButton = Button(rootWin, text = "Create Test Case", command = self.newTestCase)

        #Frame sidebar
        self.sideFrame = Frame(rootWin)
        sideLabel = Label(self.sideFrame, text= "YOUR TEST CASES")
        sideLabel.pack()
        
            
        #Frame for newly created testcases
        self.testFrame = Frame(rootWin, height = 200)
        
        #testFrame Headers
        addressLabel = Label(self.testFrame, text = "Address")
        valLabel = Label(self.testFrame, text = "Value")
        addressLabel.grid(row = 0, column = 1)
        valLabel.grid(row = 0, column = 2)
        
        #Input Buttons
        addInputButton = Button(self.testFrame, width = 15, text = "New Input", command = self.addIn)
        self.inString = StringVar()
        addInputAddress = Entry(self.testFrame, textvariable = self.inString)
        self.inString2 = StringVar()
        addInputVal = Entry(self.testFrame, textvariable = self.inString2)

        addInputButton.grid(row = 1, column = 0)
        addInputAddress.grid(row = 1, column = 1)
        addInputVal.grid(row = 1, column = 2)

        #Output Buttons
        addOutputButton = Button(self.testFrame, width = 15, text = "Expected Outputs", command = self.addOut)
        self.outString = StringVar()
        addOutAddress = Entry(self.testFrame, textvariable = self.outString)
        self.outString2 = StringVar()
        addOutVal = Entry(self.testFrame, textvariable = self.outString2)

        addOutputButton.grid(row = 2, column = 0)
        addOutAddress.grid(row = 2, column = 1)
        addOutVal.grid(row = 2, column = 2)
        
        #Grids important stuff
        testNameLabel.grid(row = 0, column = 0, sticky = W)
        testNameEntry.grid(row = 0, column = 1, sticky = W)
        makeTestCaseButton.grid(row=0, column = 2, columnspan = 2)



        self.curTestString = StringVar()
        curStringLabel = Label(self.testFrame, justify = LEFT, textvariable = self.curTestString)
        curStringLabel.grid(row = 3, column =0)

        menubar = Menu(rootWin)
        rootWin.config(menu=menubar)
        menubar.add_command(label = "Click To Save XML File", command = self.makeXML)
        menubar.add_command(label = "Help and Documentation", command = self.helpWindow)
        menubar.add_command(label = "Run Test Case", command = self.runTest)
        menubar.add_command(label = "Reset", command = self.reset)
    def addIn(self):
        if self.inString.get() == "" or self.inString2.get() == "":
            tkinter.messagebox.showerror(title = "Missing", message = "Please enter an ADDRESS and VALUE")
            return
        address = self.inString.get()
        val = self.inString2.get()
        self.testCasePointer.newIn(address,val)
        self.curTestString.set(self.testCasePointer)
        self.inString.set("")
        self.inString2.set("")

    def addOut(self):
        if self.outString.get() == "" or self.outString2.get() == "":
            tkinter.messagebox.showerror(title = "Missing", message = "Please enter an ADDRESS and VALUE")
            return
        address = self.outString.get()
        val = self.outString2.get()
        self.testCasePointer.newOut(address,val)
        self.curTestString.set(self.testCasePointer)
        self.outString.set("")
        self.outString2.set("")

    def makeXML(self):
        self.file_opt = options = {}
        options['filetypes'] = [("Complx XML Test (.xml)",".xml")]
        if len(self.testCaseList) > 0:
            theFile = tkinter.filedialog.asksaveasfilename(**self.file_opt)
        else:
            tkinter.messagebox.showerror(title="Error", message="Please make at least one test case")
            return
        success = False
        if theFile:
            success = makeXML(theFile,self.testCaseList)

        if success == True:
            tkinter.messagebox.showinfo(title="File Saved!", message="Your XML File has successfully been saved")
        else:
            return

    def helpWindow(self):
        try:
            helpWin = Tk()
            helpWin.title("LC-3 XML Maker HELP")
            helpWin.config(bg = "gray")
            file = open("README.txt")
            text = Text(helpWin, wrap = WORD, height = 40)
            text.insert(END,file.read())
            text.config(state=DISABLED)
            file.close()
            text.pack()
            helpWin.mainloop()
        except:
            helpWin.destroy()
            tkinter.messagebox.showerror(title="Error", message="Couldn't not find README.txt")
        
    def newTestCase(self):
        if self.testNameString.get() == "":
            tkinter.messagebox.showerror(title = "Missing Test Case Title", message = "Please enter a name for your test case!")
            return
        testName = self.testNameString.get()
        newTestCase = testCase(testName)
        self.testCaseList.append(newTestCase)
        self.testCasePointer = newTestCase
        self.curTestString.set(newTestCase)
        button = Radiobutton(self.sideFrame, text=testName, variable = self.counter, command = self.newPointer, value = (len(self.testCaseList) - 1))
        if len(self.testCaseList) > 0 and self.expanded == False:
            self.counter.set(0)
            self.expanded = True
            self.testFrame.grid(row = 1, column = 0)
            self.sideFrame.grid(row=1, column = 1, sticky = E)
        #Sets up radiobuttons
        button.pack()

        self.testNameString.set("")

    def newPointer(self):
        newIndx = self.counter.get()
        self.testCasePointer = self.testCaseList[newIndx]
        print(self.testCasePointer.name)
        self.curTestString.set(self.testCasePointer)

    def runTest(self):
        try:
            self.file_opt = options = {}
            options['filetypes'] = [("Complx XML Test (.xml)",".xml")]
            file = tkinter.filedialog.askopenfilename(**self.file_opt)
            if file:
                pass
            else:
                return
            filePathList = file.split(os.sep)
            actFile = filePathList[-1]
            runFile = actFile[:len(actFile)-3] + "asm"
            del filePathList[-1]
            directory = ""
            for item in filePathList:
                directory += item + os.sep
            out = os.popen("cd {}; lc3test {} {}".format(directory, actFile, runFile)).read()
            resultsWindow = Tk()
            resultsWindow.title("Results")
            scroll = Scrollbar(resultsWindow)
            resultsText = Text(resultsWindow, yscrollcommand = scroll.set)
            resultsText.insert(INSERT, out)
            resultsText.yview(END)
            scroll.config(command = resultsText.yview)
            resultsText.config(state = DISABLED)
            resultsText.pack(side=LEFT)
            scroll.pack(side=RIGHT)
            resultsWindow.mainloop()
        except:
            traceback.print_exc()
            tkinter.messagebox.showinfo(title="Error", message="No XML File chosen")

    def reset(self):
        newWin = Tk()
        newGui = mainGUI(newWin)
        newWin.mainloop()

        

class testInput:
    def __init__(self, rootWin):
        inpLabel = Label(rootWin, text = "Please Enter Input: ")
        self.inpString = StringVar()
        inpEntry = Entry(rootWin, textvariable = self.inpString)

class testOutput:
    def __init__(self, rootWin):
        outLabel = Label(rootWin, text = "Please Enter Output: ")
        self.outString = StringVar()
        outEntry = Entry(rootWin, textvariable = self.inpString)
        
        

class testCase:
    def __init__(self,name):
        self.name = name
        self.arrays = []
        self.inputs = []
        self.outputs = []

    def newArray(self, address, val):
        self.arrays.append((address, val))

    def newIn(self,address,val):
        self.inputs.append((address,val))

    def getName(self):
        return self.name
    
    def newOut(self,address,val):
        self.outputs.append((address,val))

    def __str__(self):
        stri = ("Inputs: ")
        for pair in self.inputs:
            stri = stri + ("{} = {}, ".format(pair[0].upper(),pair[1]))
        stri = stri + "\n"
        stri = stri + ("Outputs: ")
        for pair in self.outputs:
            stri = stri + ("{} = {},".format(pair[0].upper(), pair[1]))
        return stri

def makeXML(filename,testcases):
    file = open(filename,"w")
    file.write("<?xml version=\"1.0\"?>")
    file.write("<test-suite>")
    for test in testcases:
        file.write("<test-case>")
        file.write("<name>{}</name>".format(test.name))
        file.write("<has-max-executions>1</has-max-executions>")
        file.write("<max-executions>1000000</max-executions>")
        file.write("<randomize>1</randomize>")
        if len(test.inputs) > 0:
            file.write("<input>")
            for inp in test.inputs:
                if "," in inp:
                    file.write("<test-array><address>{}</address><value>{}</value></test-array>".format(inp[0],inp[1]))
                else:
                    file.write("<test-value><address>{}</address><value>{}</value></test-value>".format(inp[0],inp[1]))
            file.write("</input>")
        if len(test.outputs) > 0:
            file.write("<output>")
            for inp in test.outputs:
                file.write("<test-value><address>{}</address><value>{}</value></test-value>".format(inp[0],inp[1]))
            file.write("</output>")
        file.write("</test-case>")
    
    
    file.write("</test-suite>")
    file.close
    return True

rootWin = Tk()
gui = mainGUI(rootWin)
rootWin.mainloop()
