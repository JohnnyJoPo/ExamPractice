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

        self.manage_btn = tkinter.Button(self.window_tk, width=18, height=2, text="Manage\nQuestion Bank", command=self.openQuestionManager)
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
                    self.questionBank.insert(selectedIndex, [question, 1.0, 0, 0, [], [], [], False])
            else:
                if question.strip() == "":
                    displayList.pop(selectedIndex)
                    self.questionBank.pop(selectedIndex)
                else:
                    displayList[selectedIndex] = question.strip()
                    self.questionBank[selectedIndex][0] = question.strip()

            questionBank_comBx.config(values=displayList)
            if question.strip() == "":
                questionBank_comBx.current(len(displayList) - 1)
            else:
                questionBank_comBx.current(selectedIndex)

        def insertData(event=None):
            selectedIndex = questionBank_comBx.current()
            self.questionBank[selectedIndex][1] = points_tkSVar.get()
            self.questionBank[selectedIndex][2] = time_tkSVar.get()
            self.questionBank[selectedIndex][3] = self.questionType_tkIVar.get()
            self.questionBank[selectedIndex][4].clear()
            for i in range(0,5):
                if (self.choiceIndex_tkIVar.get() == i and self.questionType_tkIVar.get() == 0) or multiIndexArray[i].get() == True:
                    self.questionBank[selectedIndex][4].append(i)

            self.questionBank[selectedIndex][5].clear()
            self.questionBank[selectedIndex][5].append([choiceArray[0][2].get("1.0","end-1c").strip(), 0])
            self.questionBank[selectedIndex][5].append([choiceArray[1][2].get("1.0","end-1c").strip(), 1])
            if self.choiceAmount_tkIVar.get() > 2:
                self.questionBank[selectedIndex][5].append([choiceArray[2][2].get("1.0","end-1c").strip(), 2])
                if self.choiceAmount_tkIVar.get() > 3:
                    self.questionBank[selectedIndex][5].append([choiceArray[3][2].get("1.0","end-1c").strip(), 3])
                    if self.choiceAmount_tkIVar.get() > 4:
                        self.questionBank[selectedIndex][5].append([choiceArray[4][2].get("1.0","end-1c").strip(), 4])
            self.questionBank[selectedIndex][6].clear()
            for item in tagList:
                self.questionBank[selectedIndex][6].append(item)
            checkValidity()

        def updateForm(event=None):
            selectedIndex = questionBank_comBx.current()
            question_txt.delete("1.0",tkinter.END)
            if len(displayList) - 1 > selectedIndex:
                question_txt.insert(tkinter.INSERT, self.questionBank[selectedIndex][0])

        def checkValidity():
            _ = 0

        def enableChoices():
            for i in range(0,5):
                if self.choiceAmount_tkIVar.get() > i:
                    choiceArray[i][2].config(state="normal", bg="#ffffff")
                    if self.questionType_tkIVar.get() == 0:
                        choiceArray[i][0].config(state="normal")
                        choiceArray[i][1].config(state="disabled")
                        choiceArray[i][1].deselect()
                    else:
                        choiceArray[i][0].config(state="disabled")
                        choiceArray[i][1].config(state="normal")
                else:
                    choiceArray[i][0].config(state="disabled")
                    choiceArray[i][1].config(state="disabled")
                    choiceArray[i][2].config(state="disabled", bg="#dfdfdf")

        def removeChoice():
            _ = 0
        
        def addTag():
            _ = 0

        def clear():
            _ = 0

        def clearAll():
            _ = 0

        def load():
            #_ = 0
            print(self.questionBank)
   
        def save():
            _ = 0

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
        questionBank_comBx = tkinter.ttk.Combobox(questionBank_frm, height=10)
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

        error_lbl = tkinter.Label(window_tL, text="This question is not configured properly and will not appear in the exam.\n" \
            "Please check that all fields are filled out with proper values.", fg="red")
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
        points_ent = tkinter.Entry(options_frm, width=10, textvariable=points_tkSVar)
        time_lbl = tkinter.Label(options_frm, text="Time Limit (in seconds):", anchor="w")
        time_ent = tkinter.Entry(options_frm, width=10, textvariable=time_tkSVar)
        typeSingle_rad = tkinter.Radiobutton(options_frm, text="Single Answer", variable=self.questionType_tkIVar, value=0, command=enableChoices)
        typeMulti_rad = tkinter.Radiobutton(options_frm, text="Multiple Answers", variable=self.questionType_tkIVar, value=1, command=enableChoices)
        choiceAmount_lbl = tkinter.Label(options_frm, text="Choices:", anchor="w")
        choiceAmount_spnBx = tkinter.ttk.Spinbox(options_frm, width=5, from_=2, to=5, command=enableChoices, textvariable=self.choiceAmount_tkIVar, state="readonly")
        points_ent.bind("<KeyRelease>", insertData)
        time_ent.bind("<KeyRelease>", insertData)
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
            choiceArray[i].append(tkinter.Text(answers_frm, height=2))
            choiceArray[i][2].bind("<KeyRelease>", insertData)
            choiceArray[i][0].grid(row=i, column=0, padx=5)
            choiceArray[i][1].grid(row=i, column=1, padx=5)
            choiceArray[i][2].grid(row=i, column=2, sticky="ew", padx=(0,5), pady=(0,5))
            answers_frm.rowconfigure(i, weight=1)

        tags_frm = tkinter.LabelFrame(window_tL, text="Tags", relief="groove", bd=2)
        newTag_lbl = tkinter.Label(tags_frm, text="Enter new tag:", anchor="w")
        addTag_ent = tkinter.Entry(tags_frm, textvariable=tag_tkSVar)
        addTag_btn = tkinter.Button(tags_frm, text="Add Tag", command=addTag)
        tagList_lbl = tkinter.Label(tags_frm, text="Added tags:", anchor="w")
        tagList_comBx = tkinter.ttk.Combobox(tags_frm, height=4)
        clearTag_btn = tkinter.Button(tags_frm, text="Clear Selected Tag", command=clear, state="disabled")
        clearAllTags_btn = tkinter.Button(tags_frm, text="Clear All Tags", command=clearAll, state="disabled")
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
        print(displayList)
        
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