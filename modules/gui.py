import os
import os.path
import sys
import re
import tkinter
import tkinter.ttk
import tkinter.filedialog
import random
import time

import msgBank as m

class interface:
    def __init__(self):
        self.window_tk = tkinter.Tk()
        self.window_tk.title("Exam Practice v1.0")
        self.window_tk.geometry("300x140")
        self.window_tk.resizable(width=False, height=False)

        self.manage_btn = tkinter.Button(self.window_tk, width=18, height=2, text="Manage Questions", command=self.openQuestionManager)
        self.options_btn = tkinter.Button(self.window_tk, width=18, height=2, text="Exam Options", command=self.openOptionWindow)
        self.start_btn = tkinter.Button(self.window_tk, width=38, height=2, text="Begin Exam", state="disabled", command=self.startExam)
        self.exit_btn = tkinter.Button(self.window_tk, width=38, height=1, text="Exit", command=self.exitProgram)

        self.manage_btn.place(x=10, y=10)
        self.options_btn.place(x=150, y=10)
        self.start_btn.place(x=10, y=55)
        self.exit_btn.place(x=10, y=100)

        self.questionBank = []
        tkinter.mainloop()

    def openQuestionManager(self):
        def updateDisplayList(event=None):
            question = question_txt.get("1.0","end-1c")
            selectedIndex = questionBank_comBx.current()
            if len(displayList) - 1 == selectedIndex:
                if question.strip() != "":
                    displayList.insert(selectedIndex, question.strip())
                    self.questionBank.insert(selectedIndex, [question, 1.0, 0, 0, [0], [[0, ""], [1, ""]], [], False])
            else:
                if question.strip() == "":
                    displayList.pop(selectedIndex)
                    self.questionBank.pop(selectedIndex)
                    points_tkSVar.set("1.0")
                    time_tkSVar.set("0")
                    self.choiceAmount_tkIVar.set(2)
                    self.questionType_tkIVar.set(0)
                    self.choiceIndex_tkIVar.set(0)
                    error_lbl.config(text="\n")
                    tag_tkSVar.set("")
                    for i in range(0,5):
                        multiIndexArray[i].set(0)
                        choiceArray[i][2].delete("1.0",tkinter.END)
                else:
                    displayList[selectedIndex] = question.strip()
                    self.questionBank[selectedIndex][0] = question.strip()

            questionBank_comBx.config(values=displayList)
            if question.strip() == "":
                questionBank_comBx.current(len(displayList) - 1)       
            else:
                questionBank_comBx.current(selectedIndex)
            enableChoices()

        def insertData(event=None):
            selectedIndex = questionBank_comBx.current()
            self.questionBank[selectedIndex][1] = points_tkSVar.get()
            self.questionBank[selectedIndex][2] = time_tkSVar.get()
            self.questionBank[selectedIndex][3] = self.questionType_tkIVar.get()
            self.questionBank[selectedIndex][4].clear()
            for i in range(0,5):
                if (self.choiceIndex_tkIVar.get() == i and self.questionType_tkIVar.get() == 0) or (multiIndexArray[i].get() == True and self.questionType_tkIVar.get() == 1):
                    self.questionBank[selectedIndex][4].append(i)
            self.questionBank[selectedIndex][5].clear()
            for i in range(0,self.choiceAmount_tkIVar.get()):
                self.questionBank[selectedIndex][5].append([i, choiceArray[i][2].get("1.0","end-1c").strip()])
            self.questionBank[selectedIndex][6].clear()
            for tag in tagList:
                self.questionBank[selectedIndex][6].append(tag)
            checkValidity(0, None)

        def updateForm(event=None):
            selectedIndex = questionBank_comBx.current()
            question_txt.delete("1.0",tkinter.END)
            if len(displayList) - 1 > selectedIndex:
                question_txt.insert(tkinter.INSERT, self.questionBank[selectedIndex][0])
                points_tkSVar.set(str(self.questionBank[selectedIndex][1]))
                time_tkSVar.set(str(self.questionBank[selectedIndex][2]))
                self.choiceAmount_tkIVar.set(len(self.questionBank[selectedIndex][5]))
                self.questionType_tkIVar.set(self.questionBank[selectedIndex][3])
                if self.questionBank[selectedIndex][3] == 0:
                    self.choiceIndex_tkIVar.set(self.questionBank[selectedIndex][4][0])
                else:
                    for i in range(0,5):
                        multiIndexArray[i].set(0)
                        if i in self.questionBank[selectedIndex][4]:
                            multiIndexArray[i].set(1)
                for i in range(0,5):
                    choiceArray[i][2].delete("1.0",tkinter.END)
                    if i < len(self.questionBank[selectedIndex][5]):
                        choiceArray[i][2].config(state="normal")
                        choiceArray[i][2].insert(tkinter.INSERT, self.questionBank[selectedIndex][5][i][1])
                tag_tkSVar.set("")
                tagList.clear()
                for tag in self.questionBank[selectedIndex][6]:
                    tagList.append(tag)
                if tagList:
                    tagList_comBx.config(values=tagList)
                    tagList_comBx.current(len(tagList)-1)
                else:
                    tagList_comBx.set("")
                    tagList_comBx.config(values=tagList)
                checkValidity(0, None)
            else:
                points_tkSVar.set("1.0")
                time_tkSVar.set("0")
                self.choiceAmount_tkIVar.set(2)
                self.questionType_tkIVar.set(0)
                self.choiceIndex_tkIVar.set(0)
                error_lbl.config(text="\n")
                tag_tkSVar.set("")
                tagList.clear()
                for i in range(0,5):
                    multiIndexArray[i].set(0)
                    choiceArray[i][2].delete("1.0",tkinter.END)
            enableChoices()

        def checkValidity(mode, checkIndex):
            valid = True
            if mode == 0:
                selectedIndex = questionBank_comBx.current()
            else:
                selectedIndex = checkIndex
            try:
                if float(self.questionBank[selectedIndex][1]) < 0:
                    raise ValueError
                else:
                    self.questionBank[selectedIndex][1] = float(self.questionBank[selectedIndex][1])
                if isinstance(self.questionBank[selectedIndex][2], float) or int(self.questionBank[selectedIndex][2]) < 0:
                    raise ValueError
                else:
                    self.questionBank[selectedIndex][2] = int(self.questionBank[selectedIndex][2])
                if not self.questionBank[selectedIndex][4]:
                    raise ValueError
                for inArray in self.questionBank[selectedIndex][5]:
                    if inArray[1].strip() == "":
                        raise ValueError
            except ValueError:
                valid = False
            if valid:
                self.questionBank[selectedIndex][7] = True
                if mode == 0:
                    error_lbl.config(text="\n")
            else:
                self.questionBank[selectedIndex][7] = False
                if mode == 0:
                    error_lbl.config(text="This question is not configured properly and will not appear in the exam.\n" \
                        "Please check that all fields are filled out with proper values.")

        def enableChoices():
            selectedIndex = questionBank_comBx.current()
            if self.questionBank:
                clearAll_btn.config(state="normal")
                save_btn.config(state="normal")
            else:
                clearAll_btn.config(state="disabled")
                save_btn.config(state="disabled")  
            if selectedIndex == len(displayList) - 1:
                clear_btn.config(state="disabled")  
                points_ent.config(state="disabled")
                points_ent.unbind("<KeyRelease>")
                time_ent.config(state="disabled")
                time_ent.unbind("<KeyRelease>")
                typeSingle_rad.config(state="disabled")
                typeMulti_rad.config(state="disabled")
                choiceAmount_spnBx.config(state="disabled")
                tagList_comBx.set("")
                tagList_comBx.config(values=[], state="disabled")
                addTag_btn.config(state="disabled")
                addTag_ent.config(state="disabled")
                clearTag_btn.config(state="disabled")
                clearAllTags_btn.config(state="disabled")
                for i in range(0,5):
                    choiceArray[i][0].config(state="disabled")
                    choiceArray[i][1].config(state="disabled")
                    choiceArray[i][2].delete("1.0",tkinter.END)
                    choiceArray[i][2].config(state="disabled", bg="#dfdfdf")
                    choiceArray[i][2].unbind("<KeyRelease>")
            else:
                clear_btn.config(state="normal")
                points_ent.config(state="normal")
                points_ent.bind("<KeyRelease>", insertData)
                time_ent.config(state="normal")
                time_ent.bind("<KeyRelease>", insertData)
                typeSingle_rad.config(state="normal")
                typeMulti_rad.config(state="normal")
                choiceAmount_spnBx.config(state="readonly")
                addTag_btn.config(state="normal")
                addTag_ent.config(state="normal")
                if tagList:
                    tagList_comBx.config(values=tagList, state="readonly")
                    tagList_comBx.current(len(tagList)-1)
                    clearTag_btn.config(state="normal")
                    clearAllTags_btn.config(state="normal")
                else:
                    tagList_comBx.set("")
                    tagList_comBx.config(values=tagList, state="disabled")
                    clearTag_btn.config(state="disabled")
                    clearAllTags_btn.config(state="disabled")
                for i in range(0,5):
                    if self.choiceAmount_tkIVar.get() > i:
                        choiceArray[i][2].config(state="normal", bg="#ffffff")
                        choiceArray[i][2].bind("<KeyRelease>", insertData)
                        if self.questionType_tkIVar.get() == 0:
                            choiceArray[i][0].config(state="normal")
                            choiceArray[i][1].config(state="disabled")
                            choiceArray[i][1].deselect()
                        else:
                            choiceArray[i][0].config(state="disabled")
                            choiceArray[0][0].select()
                            choiceArray[i][1].config(state="normal")
                    else:
                        choiceArray[i][0].config(state="disabled")
                        if self.questionType_tkIVar.get() == 1:
                            choiceArray[0][0].select()
                        choiceArray[i][1].config(state="disabled")
                        choiceArray[i][1].deselect()
                        choiceArray[i][2].config(state="disabled", bg="#dfdfdf")
                        choiceArray[i][2].unbind("<KeyRelease>")
                insertData()

        def addTag():
            if tag_tkSVar.get().strip() == "":
                # throw empty tag error
                return
            elif tag_tkSVar.get() not in tagList:
                tagList.append(tag_tkSVar.get())
                tag_tkSVar.set("")
                enableChoices()
            else:
                # throw error for tag already being in tagList
                return
 
        def removeTag():
            selectedIndex = questionBank_comBx.current()
            selectedTagIndex = tagList_comBx.current()
            if selectedIndex == -1:
                # throw some error
                return
            tagList.pop(selectedTagIndex)
            tagList_comBx.config(values=tagList)
            enableChoices()

        def removeAllTags():
            tagList.clear()
            enableChoices()

        def clear():
            selectedIndex = questionBank_comBx.current()
            self.questionBank.pop(selectedIndex)
            displayList.pop(selectedIndex)
            questionBank_comBx.config(values=displayList)
            questionBank_comBx.current(0)
            updateForm()

        def clearAll():
            if len(displayList) > 1:
                self.questionBank.clear()
                displayList.clear()
                displayList.append("<add new question>")
                questionBank_comBx.config(values=displayList)
                questionBank_comBx.current(0)
                updateForm()

        def load():
            inFilePath = tkinter.filedialog.askopenfilename(\
                parent=window_tL,
                initialdir = os.getcwd(),
                title = "Select file",\
                filetypes = (("text files","*.txt"),("all files","*.*")))
            if inFilePath == "":
                return
            self.questionBank.clear()
            displayList.clear()
            inFile = open(inFilePath, "r")
            count = -1
            for inString in inFile:
                inString = inString.replace("\\n", "\n").rstrip("\n")
                if inString == "":
                    continue
                if inString[:10] == "QUESTION: ":
                    self.questionBank.append([inString[10:], 1.0, 0, 0, [], [], [], False])
                    displayList.append(inString[10:])
                    count += 1
                elif inString[:7] == "VALUE: ":
                    self.questionBank[count][1] = inString[7:]
                    try:
                        if float(self.questionBank[count][1]):
                            pass
                        self.questionBank[count][1] = float(self.questionBank[count][1])
                    except ValueError:
                        pass
                elif inString[:6] == "TIME: ":
                    self.questionBank[count][2] = inString[6:]
                    try:
                        if int(self.questionBank[count][2]):
                            pass
                        self.questionBank[count][2] = int(self.questionBank[count][2])
                    except ValueError:
                        pass
                elif inString[:14] == "ANSWER-LIMIT: ":
                    if inString[14:] == "MULTI":
                        self.questionBank[count][3] = 1
                    else:
                        self.questionBank[count][3] = 0
                elif inString[:19] == "CORRECT-ANSWER(S): ":
                    self.questionBank[count][4].extend(inString[19:].split(", "))
                    for i in range(0, len(self.questionBank[count][4])):
                        try:
                            if int(self.questionBank[count][4][i]):
                                pass
                            self.questionBank[count][4][i] = int(self.questionBank[count][4][i])
                        except ValueError:
                            continue
                elif inString[:7] == "CHOICE ":
                    for i in range(0,5):
                        checkString = str(i) + ": "
                        if inString[7:10] == checkString:
                            self.questionBank[count][5].append([i, inString[10:]])
                elif inString[:6] == "TAGS: " and inString[6:] != "NONE":
                    self.questionBank[count][6].extend(inString[6:].split(", "))
            for i in range(0, len(self.questionBank)):
                checkValidity(1, i)
            inFile.close()
            displayList.append("<add new question>")
            questionBank_comBx.config(values=displayList)
            questionBank_comBx.current(0)
            updateForm()
   
        def save():
            outFilePath = tkinter.filedialog.asksaveasfilename(\
                parent=window_tL,\
                initialdir = os.getcwd(),\
                title = "Save as",\
                filetypes = (("text files","*.txt"),("all files","*.*")),\
                defaultextension='.txt')
            if outFilePath == "":
                return
            outString = ""
            for question in self.questionBank:
                outString += "\nQUESTION: " + question[0].replace("\n", "\\n") + "\n" \
                    "VALUE: " + str(question[1]) + "\n" \
                    "TIME: " + str(question[2]) + "\n"
                if question[3] == 0:
                    outString += "ANSWER-LIMIT: SINGLE" + "\n"
                else:
                    outString += "ANSWER-LIMIT: MULTI" + "\n"
                outString += "CORRECT-ANSWER(S): "
                for answer in question[4]:
                    outString += str(answer) + ", "
                outString = outString.rstrip(", ")
                outString += "\n"
                for choice in question[5]:
                    outString += "CHOICE " + str(choice[0]) + ": " + choice[1].replace("\n", "\\n") + "\n"
                outString += "TAGS: "
                if question[6]:
                    for tag in question[6]:
                        outString += tag + ", "
                    outString = outString.rstrip(", ")
                else:
                    outString += "NONE"
                outString += "\n"
            outString = outString.strip("\n")
            outFile = open(outFilePath, "w")
            outFile.write(outString)
            outFile.close()
            # questions saved message

        displayList = ["<add new question>"]
        tagList = []
        points_tkSVar = tkinter.StringVar()
        time_tkSVar = tkinter.StringVar()
        self.choiceAmount_tkIVar = tkinter.IntVar(value=2)
        self.questionType_tkIVar = tkinter.IntVar(value=0)
        self.choiceIndex_tkIVar = tkinter.IntVar(value=0)
        tag_tkSVar = tkinter.StringVar(value="")

        window_tL = tkinter.Toplevel()
        window_tL.title("Question Manager")
        window_tL.geometry("500x600")
        window_tL.resizable(width=False, height=False)

        questionBank_frm = tkinter.LabelFrame(window_tL, text="Question Bank")
        questionBank_lbl = tkinter.Label(questionBank_frm, text="Selected question:", anchor="w")
        questionBank_comBx = tkinter.ttk.Combobox(questionBank_frm, height=10, state="readonly")
        questionBankButtons_frm = tkinter.Frame(questionBank_frm)
        clear_btn = tkinter.Button(questionBankButtons_frm, text="Clear Selected Question", command=clear, state="disabled")
        clearAll_btn = tkinter.Button(questionBankButtons_frm, text="Clear All Questions", command=clearAll, state="disabled")
        load_btn = tkinter.Button(questionBankButtons_frm, text="Load Questions", command=load)
        save_btn = tkinter.Button(questionBankButtons_frm, text="Save Questions", command=save, state="disabled")
        questionBank_comBx.bind("<<ComboboxSelected>>", updateForm)
        questionBank_frm.grid(row=0, column=0, sticky="ew", padx=5)
        questionBank_lbl.grid(row=0, column=0, sticky="w", padx=(5,0), pady=5)
        questionBank_comBx.grid(row=0, column=1, sticky="ew", padx=(0,5), pady=5)
        questionBankButtons_frm.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0,5))
        questionBank_frm.columnconfigure(0, weight=1)
        questionBank_frm.columnconfigure(1, weight=100)
        clear_btn.grid(row=0, column=0, padx=(0,5), sticky="ew")
        clearAll_btn.grid(row=0, column=1, padx=(0,5), sticky="ew")
        load_btn.grid(row=0, column=2, padx=(0,5), sticky="ew")
        save_btn.grid(row=0, column=3, sticky="ew")
        questionBankButtons_frm.columnconfigure(0, weight=2)
        questionBankButtons_frm.columnconfigure(1, weight=2)
        questionBankButtons_frm.columnconfigure(2, weight=1)
        questionBankButtons_frm.columnconfigure(3, weight=1)

        error_lbl = tkinter.Label(window_tL, text="", fg="red")
        error_lbl.grid(row=1, column=0, sticky="ew", padx=5, pady=(5,0))

        question_frm = tkinter.LabelFrame(window_tL, text="Question")
        question_txt = tkinter.Text(question_frm, height=3)
        question_yScb = tkinter.Scrollbar(question_frm, orient=tkinter.VERTICAL, command=question_txt.yview)
        question_txt.config(yscrollcommand=question_yScb.set)
        question_txt.bind("<KeyRelease>", updateDisplayList)
        question_frm.grid(row=2, column=0, sticky="ew", padx=5)
        question_txt.grid(row=0, column=0, sticky="ew", padx=(5,2), pady=5)
        question_yScb.grid(row=0, column=1, padx=(0,5), pady=5)
        question_frm.columnconfigure(0, weight=100)
        question_frm.columnconfigure(1, weight=1)


        options_frm = tkinter.LabelFrame(window_tL, text="Options")
        points_lbl = tkinter.Label(options_frm, text="Question Point Value:", anchor="w")
        points_ent = tkinter.Entry(options_frm, width=10, textvariable=points_tkSVar, state="disabled")
        time_lbl = tkinter.Label(options_frm, text="Time Limit (in seconds):", anchor="w")
        time_ent = tkinter.Entry(options_frm, width=10, textvariable=time_tkSVar, state="disabled")
        typeSingle_rad = tkinter.Radiobutton(options_frm, text="Single Answer", variable=self.questionType_tkIVar, value=0, command=enableChoices, state="disabled")
        typeMulti_rad = tkinter.Radiobutton(options_frm, text="Multiple Answers", variable=self.questionType_tkIVar, value=1, command=enableChoices, state="disabled")
        choiceAmount_lbl = tkinter.Label(options_frm, text="Choices:", anchor="w")
        choiceAmount_spnBx = tkinter.ttk.Spinbox(options_frm, width=5, from_=2, to=5, command=enableChoices, textvariable=self.choiceAmount_tkIVar, state="disabled")
        options_frm.grid(row=3, column=0, sticky="ew", padx=5)
        points_lbl.grid(row=0, column=0, sticky="w", padx=(5,0), pady=(5,0))
        points_ent.grid(row=0, column=1, sticky="w", pady=(5,0))
        time_lbl.grid(row=1, column=0, sticky="w", padx=(5,0), pady=(0,5))
        time_ent.grid(row=1, column=1, sticky="w", pady=(0,5))
        typeSingle_rad.grid(row=0, column=2, sticky="w", padx=(10,0), pady=(5,0))
        typeMulti_rad.grid(row=1, column=2, sticky="w", padx=(10,0), pady=(0,5))
        choiceAmount_lbl.grid(row=0, column=3, sticky="e", pady=(5,0))
        choiceAmount_spnBx.grid(row=0, column=4, sticky="ew", padx=(0,5), pady=(5,0))
        options_frm.columnconfigure(0, weight=1)
        options_frm.columnconfigure(1, weight=1)
        options_frm.columnconfigure(2, weight=1)
        options_frm.columnconfigure(3, weight=1)
        options_frm.columnconfigure(4, weight=1)

        multiIndexArray = []
        choiceArray = [[],[],[],[],[]]

        answers_frm = tkinter.LabelFrame(window_tL, text="Answers", relief="groove", bd=2)
        answers_frm.grid(row=4, column=0, sticky="ew", padx=5)
        answers_frm.columnconfigure(0, weight=1)
        answers_frm.columnconfigure(1, weight=1)
        answers_frm.columnconfigure(2, weight=100)

        for i in range(0,5):
            multiIndexArray.append(tkinter.BooleanVar(value=False))
            choiceArray[i].append(tkinter.Radiobutton(answers_frm, variable=self.choiceIndex_tkIVar, value=i, command=insertData, state="disabled"))
            choiceArray[i].append(tkinter.Checkbutton(answers_frm, variable=multiIndexArray[i], command=insertData, state="disabled"))
            choiceArray[i].append(tkinter.Text(answers_frm, height=2, state="disabled", bg="#dfdfdf"))
            choiceArray[i][0].grid(row=i, column=0, padx=5)
            choiceArray[i][1].grid(row=i, column=1, padx=5)
            choiceArray[i][2].grid(row=i, column=2, sticky="ew", padx=(0,5), pady=(0,5))
            answers_frm.rowconfigure(i, weight=1)

        tags_frm = tkinter.LabelFrame(window_tL, text="Tags", relief="groove", bd=2)
        newTag_lbl = tkinter.Label(tags_frm, text="Enter new tag:", anchor="w")
        addTag_ent = tkinter.Entry(tags_frm, textvariable=tag_tkSVar, state="disabled")
        addTag_btn = tkinter.Button(tags_frm, text="Add Tag", command=addTag)
        tagList_lbl = tkinter.Label(tags_frm, text="Added tags:", anchor="w")
        tagList_comBx = tkinter.ttk.Combobox(tags_frm, height=4, state="disabled")
        clearTag_btn = tkinter.Button(tags_frm, text="Clear Selected Tag", command=removeTag, state="disabled")
        clearAllTags_btn = tkinter.Button(tags_frm, text="Clear All Tags", command=removeAllTags, state="disabled")
        tags_frm.grid(row=5, column=0, padx=5, sticky="ew")
        newTag_lbl.grid(column=0, row=0, sticky="w", padx=(5,0), pady=(5,0))
        addTag_ent.grid(column=1, row=0, sticky="ew", pady=(5,0))
        addTag_btn.grid(column=2, row=0, sticky="ew", padx=5, columnspan=2)
        tagList_lbl.grid(column=0, row=1, sticky="w", padx=(5,0), pady=(0,5))
        tagList_comBx.grid(column=1, row=1, sticky="ew", pady=5)
        clearTag_btn.grid(column=2, row=1, sticky="ew", padx=5, pady=5)
        clearAllTags_btn.grid(column=3, row=1, sticky="ew", padx=(0,5), pady=5)
        tags_frm.columnconfigure(0, weight=1)
        tags_frm.columnconfigure(1, weight=1)
        tags_frm.columnconfigure(2, weight=1)
        tags_frm.columnconfigure(3, weight=1)

        for i in range(window_tL.grid_size()[1]):
            window_tL.rowconfigure(i, weight=1)

        for i in range(window_tL.grid_size()[0]):
            window_tL.columnconfigure(i, weight=1)

        if len(self.questionBank) != 0:
            displayList.clear()
            for inArray in self.questionBank:
                displayList.append(inArray[0])
            displayList.append("<add new question>")

        print(self.questionBank)
        
        questionBank_comBx.config(values=displayList)
        questionBank_comBx.current(0)
        tagList_comBx.config(values=tagList)
        updateForm()
        window_tL.focus_set()
        window_tL.grab_set()

    def openOptionWindow(self):
        _ = 0

    def startExam(self):
        _ = 0

    def exitProgram(self):
        self.window_tk.destroy()

def start():
    _ = interface()