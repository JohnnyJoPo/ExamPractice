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
                    self.questionBank.insert(selectedIndex, [question, 1.0, 0, 0, 0, [], []])
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

        def updateForm(event=None):
            selectedIndex = questionBank_comBx.current()
            question_txt.delete("1.0",tkinter.END)
            if len(displayList) - 1 > selectedIndex:
                question_txt.insert(tkinter.INSERT, self.questionBank[selectedIndex][0])

        def enableChoices():
            _ = 0
            
        def removeChoice():
            _ = 0
        
        def clear():
            _ = 0

        def clearAll():
            _ = 0

        def load():
            _ = 0
   
        def save():
            _ = 0

        displayList = ["<add new question>"]
        points_tkSVar = tkinter.StringVar()
        time_tkSVar = tkinter.StringVar()
        self.choiceAmount_tkIVar = tkinter.IntVar(value=2)
        self.questionType_tkIVar = tkinter.IntVar(value=0)
        self.choiceIndex_tkIVar = tkinter.IntVar(value=0)
        multiIndex1_tkBVar = tkinter.BooleanVar(value=False)
        multiIndex2_tkBVar = tkinter.BooleanVar(value=False)
        multiIndex3_tkBVar = tkinter.BooleanVar(value=False)
        multiIndex4_tkBVar = tkinter.BooleanVar(value=False)
        multiIndex5_tkBVar = tkinter.BooleanVar(value=False)

        window_tL = tkinter.Toplevel()
        window_tL.title("Question Manager")
        window_tL.geometry("500x500")
        window_tL.resizable(width=False, height=False)
        menu_frm = tkinter.Frame(window_tL)
        questionBank_lbl = tkinter.Label(menu_frm, text="Selected question:", anchor="w")
        questionBank_comBx = tkinter.ttk.Combobox(menu_frm, width=60, height=10)
        header_frm = tkinter.Frame(window_tL)
        clear_btn = tkinter.Button(header_frm, width=20, text="Clear Selected Question", command=clear, state="disabled")
        clearAll_btn = tkinter.Button(header_frm, width=16, text="Clear All Questions", command=clearAll, state="disabled")
        load_btn = tkinter.Button(header_frm, width=13, text="Load Questions", command=load)
        save_btn = tkinter.Button(header_frm, width=13, text="Save Questions", command=save, state="disabled")
        question_frm = tkinter.LabelFrame(window_tL, text="Question")
        question_txt = tkinter.Text(question_frm, width=57, height=3)
        question_yScb = tkinter.Scrollbar(question_frm, orient=tkinter.VERTICAL, command=question_txt.yview)
        question_txt.config(yscrollcommand=question_yScb.set)
        options_frm = tkinter.LabelFrame(window_tL, text="Options")
        topOptions_frm = tkinter.Frame(options_frm)
        points_lbl = tkinter.Label(topOptions_frm, text="Point Value:", anchor="w")
        points_ent = tkinter.Entry(topOptions_frm, width=8, textvariable=points_tkSVar)
        typeSingle_rad = tkinter.Radiobutton(topOptions_frm, text="Single Answer", variable=self.questionType_tkIVar, value=0)
        choiceAmount_lbl = tkinter.Label(topOptions_frm, text="Choices:", anchor="w")
        choiceAmount_spnBx = tkinter.ttk.Spinbox(topOptions_frm, from_=2, to=5, command=enableChoices, textvariable=self.choiceAmount_tkIVar, state="readonly", width=4)
        bottomOptions_frm = tkinter.Frame(options_frm)
        time_lbl = tkinter.Label(bottomOptions_frm, text="Time Limit (in seconds):", anchor="w")
        time_ent = tkinter.Entry(bottomOptions_frm, width=8, textvariable=time_tkSVar)
        typeMulti_rad = tkinter.Radiobutton(bottomOptions_frm, text="Multiple Answers", variable=self.questionType_tkIVar, value=1)
        answers_frm = tkinter.LabelFrame(window_tL, text="Answers", relief="groove", bd=2)
        choice1_frm = tkinter.Frame(answers_frm)
        choice1_rad = tkinter.Radiobutton(choice1_frm, variable=self.choiceIndex_tkIVar, value=0)
        choice1_chk = tkinter.Checkbutton(choice1_frm, variable=multiIndex1_tkBVar, state="disabled")
        choice1_txt = tkinter.Text(choice1_frm, width=52, height=2)
        choice2_frm = tkinter.Frame(answers_frm)
        choice2_rad = tkinter.Radiobutton(choice2_frm, variable=self.choiceIndex_tkIVar, value=1)
        choice2_chk = tkinter.Checkbutton(choice2_frm, variable=multiIndex2_tkBVar, state="disabled")
        choice2_txt = tkinter.Text(choice2_frm, width=52, height=2)
        choice3_frm = tkinter.Frame(answers_frm)
        choice3_rad = tkinter.Radiobutton(choice3_frm, variable=self.choiceIndex_tkIVar, value=2, state="disabled")
        choice3_chk = tkinter.Checkbutton(choice3_frm, variable=multiIndex3_tkBVar, state="disabled")
        choice3_txt = tkinter.Text(choice3_frm, width=52, height=2, state="disabled", bg="#dfdfdf")
        choice4_frm = tkinter.Frame(answers_frm)
        choice4_rad = tkinter.Radiobutton(choice4_frm, variable=self.choiceIndex_tkIVar, value=3, state="disabled")
        choice4_chk = tkinter.Checkbutton(choice4_frm, variable=multiIndex4_tkBVar, state="disabled")
        choice4_txt = tkinter.Text(choice4_frm, width=52, height=2, state="disabled", bg="#dfdfdf")
        choice5_frm = tkinter.Frame(answers_frm)
        choice5_rad = tkinter.Radiobutton(choice5_frm, variable=self.choiceIndex_tkIVar, value=4, state="disabled")
        choice5_chk = tkinter.Checkbutton(choice5_frm, variable=multiIndex5_tkBVar, state="disabled")
        choice5_txt = tkinter.Text(choice5_frm, width=52, height=2, state="disabled", bg="#dfdfdf")

        question_txt.bind("<KeyRelease>", updateDisplayList)
        questionBank_comBx.bind("<<ComboboxSelected>>", updateForm)

        menu_frm.place(x=5, y=5)
        questionBank_lbl.pack(side="left")
        questionBank_comBx.pack(fill="x", expand="true", padx=(4,0))
        header_frm.place(x=5, y=30)
        clear_btn.pack(side="left")
        clearAll_btn.pack(side="left", padx=(5,0))
        load_btn.pack(side="left", padx=(5,0))
        save_btn.pack(side="left", padx=(5,0))
        question_frm.place(x=5, y=65)
        question_yScb.pack(side="right", fill="y", padx=(5,0), pady=5)
        question_txt.pack(fill="x", expand="true", padx=(5,0), pady=5)
        options_frm.place(x=5, y=155)
        topOptions_frm.pack(side="top", anchor="w", padx=5, pady=(5,0))
        points_lbl.pack(side="left")
        points_ent.pack(side="left", padx=(0,93))
        typeSingle_rad.pack(side="left", padx=(0,60))
        choiceAmount_lbl.pack(side="left")
        choiceAmount_spnBx.pack(side="left", padx=(0,5))
        bottomOptions_frm.pack(side="top", anchor="w", padx=5, pady=(0,5))
        time_lbl.pack(side="left")
        time_ent.pack(side="left", padx=(0,30))
        typeMulti_rad.pack(side="left")
        answers_frm.place(x=5, y=245)
        choice1_frm.pack(fill="x", pady=5)
        choice1_rad.pack(side="left", padx=(5,0))
        choice1_chk.pack(side="left")
        choice1_txt.pack(fill="x", padx=(0,5), expand="true")
        choice2_frm.pack(fill="x", pady=5)
        choice2_rad.pack(side="left", padx=(5,0))
        choice2_chk.pack(side="left")
        choice2_txt.pack(fill="x", padx=(0,5), expand="true")
        choice3_frm.pack(fill="x", pady=5)
        choice3_rad.pack(side="left", padx=(5,0))
        choice3_chk.pack(side="left")
        choice3_txt.pack(fill="x", padx=(0,5), expand="true")
        choice4_frm.pack(fill="x", pady=5)
        choice4_rad.pack(side="left", padx=(5,0))
        choice4_chk.pack(side="left")
        choice4_txt.pack(fill="x", padx=(0,5), expand="true")
        choice5_frm.pack(fill="x", pady=5)
        choice5_rad.pack(side="left", padx=(5,0))
        choice5_chk.pack(side="left")
        choice5_txt.pack(fill="x", padx=(0,5), expand="true")

        if len(self.questionBank) != 0:
            displayList.clear()
            for inArray in self.questionBank:
                displayList.append(inArray[0])
            displayList.append("<add new question>")

        print(self.questionBank)
        print(displayList)
        
        questionBank_comBx.config(values=displayList)
        questionBank_comBx.current(0)
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