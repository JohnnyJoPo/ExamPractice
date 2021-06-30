import os
import sys
import re
import tkinter
import tkinter.ttk
import tkinter.filedialog
import functools
import time
import random
import copy

import msgBank as m

class interface:
    def __init__(self):
        self.window_tk = tkinter.Tk()
        self.window_tk.title("Exam Practice v1.0")
        self.window_tk.geometry("300x130")
        self.window_tk.resizable(width=False, height=False)

        self.manage_btn = tkinter.Button(self.window_tk, width=18, height=2, text="Manage Questions", command=self.openQuestionManager)
        self.options_btn = tkinter.Button(self.window_tk, width=18, height=2, text="Exam Options", command=self.openOptionWindow)
        self.start_btn = tkinter.Button(self.window_tk, width=38, height=2, text="Begin Exam", state="disabled", command=self.startExam)
        self.exit_btn = tkinter.Button(self.window_tk, width=38, height=1, text="Exit", command=self.exitProgram)
        _dummy_lbl = tkinter.Label(self.window_tk)
        self.window_tk.columnconfigure(0, weight=1)
        self.window_tk.columnconfigure(1, weight=1)

        self.manage_btn.grid(row=0, column=0, sticky="ew", padx=(5,2), pady=(5,0))
        self.options_btn.grid(row=0, column=1, sticky="ew", padx=(2,5), pady=(5,0))
        self.start_btn.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        self.exit_btn.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.defaultColor = _dummy_lbl.cget("bg")
        self.questionBank = []
        self.examOptions = []
        for _ in range(0,9):
            self.examOptions.append(tkinter.BooleanVar(value=False))
        tkinter.mainloop()

    def openQuestionManager(self):
        def QM_updateQuestionDisplayList(event=None):
            question = QM_question_input_txt.get("1.0","end-1c")
            selectedIndex = QM_qBank_question_comBx.current()
            if len(QM_questionDisplayList) - 1 == selectedIndex:
                if question.strip() != "":
                    QM_questionDisplayList.insert(selectedIndex, question.strip())
                    self.questionBank.insert(selectedIndex, [question, 1.0, 0, 0, [0], [[0, ""], [1, ""]], [], False])
            else:
                if question.strip() == "":
                    QM_questionDisplayList.pop(selectedIndex)
                    self.questionBank.pop(selectedIndex)
                    QM_points_tkSVar.set("1.0")
                    QM_time_tkSVar.set("0")
                    self.QM_options_quantity_tkIVar.set(2)
                    self.QM_options_type_tkIVar.set(0)
                    self.QM_answers_singleChoice_tkIVar.set(0)
                    QM_error_lbl.config(text="\n")
                    QM_tag_tkSVar.set("")
                    for i in range(0,5):
                        QM_answers_multiChoiceArray[i].set(0)
                        QM_answers_widgetArray[i][2].delete("1.0",tkinter.END)
                else:
                    QM_questionDisplayList[selectedIndex] = question.strip()
                    self.questionBank[selectedIndex][0] = question.strip()

            QM_qBank_question_comBx.config(values=QM_questionDisplayList)
            if question.strip() == "":
                QM_qBank_question_comBx.current(len(QM_questionDisplayList) - 1)       
            else:
                QM_qBank_question_comBx.current(selectedIndex)
            QM_enableChoices()

        def QM_insertData(event=None):
            selectedIndex = QM_qBank_question_comBx.current()
            self.questionBank[selectedIndex][1] = QM_points_tkSVar.get()
            self.questionBank[selectedIndex][2] = QM_time_tkSVar.get()
            self.questionBank[selectedIndex][3] = self.QM_options_type_tkIVar.get()
            self.questionBank[selectedIndex][4].clear()
            for i in range(0,5):
                if (self.QM_answers_singleChoice_tkIVar.get() == i and self.QM_options_type_tkIVar.get() == 0) or (QM_answers_multiChoiceArray[i].get() == True and self.QM_options_type_tkIVar.get() == 1):
                    self.questionBank[selectedIndex][4].append(i)
            self.questionBank[selectedIndex][5].clear()
            for i in range(0,self.QM_options_quantity_tkIVar.get()):
                self.questionBank[selectedIndex][5].append([i, QM_answers_widgetArray[i][2].get("1.0","end-1c").strip()])
            self.questionBank[selectedIndex][6].clear()
            for tag in QM_tags_tagList:
                self.questionBank[selectedIndex][6].append(tag)
            QM_checkValidity(0, None)
            QM_enableExam()

        def QM_checkValidity(mode, checkIndex):
            valid = True
            if mode == 0:
                selectedIndex = QM_qBank_question_comBx.current()
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
                    QM_error_lbl.config(text="\n")
            else:
                self.questionBank[selectedIndex][7] = False
                if mode == 0:
                    QM_error_lbl.config(text="This question is not configured properly and will not appear in the exam.\n" \
                        "Please check that all fields are filled out with proper values.")

        def QM_updateForm(event=None):
            selectedIndex = QM_qBank_question_comBx.current()
            QM_question_input_txt.delete("1.0",tkinter.END)
            if len(QM_questionDisplayList) - 1 > selectedIndex:
                QM_question_input_txt.insert(tkinter.INSERT, self.questionBank[selectedIndex][0])
                QM_points_tkSVar.set(str(self.questionBank[selectedIndex][1]))
                QM_time_tkSVar.set(str(self.questionBank[selectedIndex][2]))
                self.QM_options_quantity_tkIVar.set(len(self.questionBank[selectedIndex][5]))
                self.QM_options_type_tkIVar.set(self.questionBank[selectedIndex][3])
                if self.questionBank[selectedIndex][3] == 0:
                    self.QM_answers_singleChoice_tkIVar.set(self.questionBank[selectedIndex][4][0])
                else:
                    for i in range(0,5):
                        QM_answers_multiChoiceArray[i].set(0)
                        if i in self.questionBank[selectedIndex][4]:
                            QM_answers_multiChoiceArray[i].set(1)
                for i in range(0,5):
                    QM_answers_widgetArray[i][2].delete("1.0",tkinter.END)
                    if i < len(self.questionBank[selectedIndex][5]):
                        QM_answers_widgetArray[i][2].config(state="normal")
                        QM_answers_widgetArray[i][2].insert(tkinter.INSERT, self.questionBank[selectedIndex][5][i][1])
                QM_tag_tkSVar.set("")
                QM_tags_tagList.clear()
                for tag in self.questionBank[selectedIndex][6]:
                    QM_tags_tagList.append(tag)
                if QM_tags_tagList:
                    QM_tags_tagList_comBx.config(values=QM_tags_tagList)
                    QM_tags_tagList_comBx.current(len(QM_tags_tagList)-1)
                else:
                    QM_tags_tagList_comBx.set("")
                    QM_tags_tagList_comBx.config(values=QM_tags_tagList)
                QM_checkValidity(0, None)
            else:
                QM_points_tkSVar.set("1.0")
                QM_time_tkSVar.set("0")
                self.QM_options_quantity_tkIVar.set(2)
                self.QM_options_type_tkIVar.set(0)
                self.QM_answers_singleChoice_tkIVar.set(0)
                QM_error_lbl.config(text="\n")
                QM_tag_tkSVar.set("")
                QM_tags_tagList.clear()
                for i in range(0,5):
                    QM_answers_multiChoiceArray[i].set(0)
                    QM_answers_widgetArray[i][2].delete("1.0",tkinter.END)
            QM_enableChoices()

        def QM_enableExam():
            self.start_btn.config(state="disabled")
            if self.questionBank:
                for check in self.questionBank:
                    if check[7]:
                        self.start_btn.config(state="normal")
                        return

        def QM_enableChoices():
            QM_enableExam()
            selectedIndex = QM_qBank_question_comBx.current()
            if self.questionBank:
                QM_qBank_buttons_clearAll_btn.config(state="normal")
                QM_qBank_buttons_save_btn.config(state="normal")
            else:
                QM_qBank_buttons_clearAll_btn.config(state="disabled")
                QM_qBank_buttons_save_btn.config(state="disabled")  
            if selectedIndex == len(QM_questionDisplayList) - 1:
                QM_qBank_buttons_clear_btn.config(state="disabled")  
                QM_options_points_ent.config(state="disabled")
                QM_options_points_ent.unbind("<KeyRelease>")
                QM_options_time_ent.config(state="disabled")
                QM_options_time_ent.unbind("<KeyRelease>")
                QM_options_typeSingle_rad.config(state="disabled")
                QM_options_typeMulti_rad.config(state="disabled")
                QM_options_quantity_spnBx.config(state="disabled")
                QM_tags_tagList_comBx.set("")
                QM_tags_tagList_comBx.config(values=[], state="disabled")
                QM_tags_addTag_btn.config(state="disabled")
                QM_tags_addTag_ent.config(state="disabled")
                QM_tags_clear_btn.config(state="disabled")
                QM_tags_clearAll_btn.config(state="disabled")
                for i in range(0,5):
                    QM_answers_widgetArray[i][0].config(state="disabled")
                    QM_answers_widgetArray[i][1].config(state="disabled")
                    QM_answers_widgetArray[i][2].delete("1.0",tkinter.END)
                    QM_answers_widgetArray[i][2].config(state="disabled", bg="#dfdfdf")
                    QM_answers_widgetArray[i][2].unbind("<KeyRelease>")
            else:
                QM_qBank_buttons_clear_btn.config(state="normal")
                QM_options_points_ent.config(state="normal")
                QM_options_points_ent.bind("<KeyRelease>", QM_insertData)
                QM_options_time_ent.config(state="normal")
                QM_options_time_ent.bind("<KeyRelease>", QM_insertData)
                QM_options_typeSingle_rad.config(state="normal")
                QM_options_typeMulti_rad.config(state="normal")
                QM_options_quantity_spnBx.config(state="readonly")
                QM_tags_addTag_btn.config(state="normal")
                QM_tags_addTag_ent.config(state="normal")
                if QM_tags_tagList:
                    QM_tags_tagList_comBx.config(values=QM_tags_tagList, state="readonly")
                    QM_tags_tagList_comBx.current(len(QM_tags_tagList)-1)
                    QM_tags_clear_btn.config(state="normal")
                    QM_tags_clearAll_btn.config(state="normal")
                else:
                    QM_tags_tagList_comBx.set("")
                    QM_tags_tagList_comBx.config(values=QM_tags_tagList, state="disabled")
                    QM_tags_clear_btn.config(state="disabled")
                    QM_tags_clearAll_btn.config(state="disabled")
                for i in range(0,5):
                    if self.QM_options_type_tkIVar.get() == 0:
                        QM_answers_widgetArray[i][1].grid_remove()
                        QM_answers_widgetArray[i][0].grid()
                    else:
                        QM_answers_widgetArray[i][0].grid_remove()
                        QM_answers_widgetArray[i][1].grid()
                    if self.QM_options_quantity_tkIVar.get() > i:
                        QM_answers_widgetArray[i][2].config(state="normal", bg="#ffffff")
                        QM_answers_widgetArray[i][2].bind("<KeyRelease>", QM_insertData)
                        if self.QM_options_type_tkIVar.get() == 0:
                            QM_answers_widgetArray[i][0].config(state="normal")
                            QM_answers_widgetArray[i][1].config(state="disabled")
                            QM_answers_widgetArray[i][1].deselect()
                        else:
                            QM_answers_widgetArray[i][0].config(state="disabled")
                            QM_answers_widgetArray[0][0].select()
                            QM_answers_widgetArray[i][1].config(state="normal")
                    else:
                        QM_answers_widgetArray[i][0].config(state="disabled")
                        if self.QM_options_type_tkIVar.get() == 1:
                            QM_answers_widgetArray[0][0].select()
                        QM_answers_widgetArray[i][1].config(state="disabled")
                        QM_answers_widgetArray[i][1].deselect()
                        QM_answers_widgetArray[i][2].config(state="disabled", bg="#dfdfdf")
                        QM_answers_widgetArray[i][2].unbind("<KeyRelease>")
                QM_insertData()

        def QM_clear():
            selectedIndex = QM_qBank_question_comBx.current()
            self.questionBank.pop(selectedIndex)
            QM_questionDisplayList.pop(selectedIndex)
            QM_qBank_question_comBx.config(values=QM_questionDisplayList)
            QM_qBank_question_comBx.current(0)
            QM_updateForm()

        def QM_clearAll():
            if len(QM_questionDisplayList) > 1:
                self.questionBank.clear()
                QM_questionDisplayList.clear()
                QM_questionDisplayList.append("<add new question>")
                QM_qBank_question_comBx.config(values=QM_questionDisplayList)
                QM_qBank_question_comBx.current(0)
                QM_updateForm()

        def QM_addTag():
            if not bool(re.match("^[a-zA-Z0-9_]+$", QM_tag_tkSVar.get().strip())):
                m.display(100, QM_window_tL) # No valid tag entered
                return
            elif QM_tag_tkSVar.get().upper().strip() not in [tag.upper() for tag in QM_tags_tagList]:
                QM_tags_tagList.append(QM_tag_tkSVar.get().strip())
                QM_tag_tkSVar.set("")
                QM_enableChoices()
            else:
                m.display(101, QM_window_tL) # Tag already added
                return
 
        def QM_removeTag():
            selectedIndex = QM_qBank_question_comBx.current()
            selectedTagIndex = QM_tags_tagList_comBx.current()
            if selectedIndex == -1:
                m.display(102, QM_window_tL) # No tag selected for deletion
                return
            QM_tags_tagList.pop(selectedTagIndex)
            QM_tags_tagList_comBx.config(values=QM_tags_tagList)
            QM_enableChoices()

        def QM_removeAllTags():
            QM_tags_tagList.clear()
            QM_enableChoices()

        def QM_load():
            inFilePath = tkinter.filedialog.askopenfilename(\
                parent=QM_window_tL,
                initialdir = os.getcwd(),
                title = "Select file",\
                filetypes = (("text files","*.txt"),("all files","*.*")))
            if inFilePath == "":
                return
            if not m.display(103, QM_window_tL): # Confirm question reset
                return
            self.questionBank.clear()
            QM_questionDisplayList.clear()
            inFile = open(inFilePath, "r")
            count = -1
            warningMsg = False
            for inString in inFile:
                inString = inString.replace("\\n", "\n").rstrip("\n")
                if inString == "":
                    continue
                if inString[:10].upper() == "QUESTION: ":
                    self.questionBank.append([inString[10:], 1.0, 0, 0, [], [], [], False])
                    QM_questionDisplayList.append(inString[10:])
                    count += 1
                elif inString[:7].upper() == "VALUE: ":
                    self.questionBank[count][1] = inString[7:]
                    try:
                        if float(self.questionBank[count][1]):
                            pass
                        self.questionBank[count][1] = float(self.questionBank[count][1])
                    except ValueError:
                        pass
                elif inString[:6].upper() == "TIME: ":
                    self.questionBank[count][2] = inString[6:]
                    try:
                        if int(self.questionBank[count][2]):
                            pass
                        self.questionBank[count][2] = int(self.questionBank[count][2])
                    except ValueError:
                        pass
                elif inString[:14].upper() == "ANSWER-LIMIT: ":
                    if inString[14:].upper() == "MULTI":
                        self.questionBank[count][3] = 1
                    else:
                        self.questionBank[count][3] = 0
                elif inString[:19].upper() == "CORRECT-ANSWER(S): ":
                    self.questionBank[count][4].extend(inString[19:].split(", "))
                    for i in range(0, len(self.questionBank[count][4])):
                        try:
                            if int(self.questionBank[count][4][i]):
                                pass
                            self.questionBank[count][4][i] = int(self.questionBank[count][4][i])
                        except ValueError:
                            continue
                elif inString[:7].upper() == "CHOICE ":
                    for i in range(0,5):
                        checkString = str(i) + ": "
                        if inString[7:10] == checkString:
                            self.questionBank[count][5].append([i, inString[10:]])
                elif inString[:6].upper() == "TAGS: " and inString[6:].upper() != "NONE":
                    self.questionBank[count][6].extend(inString[6:].split(", "))
            for i in range(0, len(self.questionBank)):
                if len(self.questionBank[i][4]) == 0:
                    self.questionBank[i][4].append(0)
                    warningMsg = True
                if len(self.questionBank[i][5]) <= 1:
                    self.questionBank[i][5].clear()
                    self.questionBank[i][5].extend([[0, ""], [1, ""]])
                    warningMsg = True
                filteredQM_tags_tagList = []
                for tag in self.questionBank[i][6]:
                    if bool(re.match("^[a-zA-Z0-9_]+$", tag)):
                        filteredQM_tags_tagList.append(tag)
                    else:
                        warningMsg = True
                self.questionBank[i][6].clear()
                for tag in filteredQM_tags_tagList:
                    self.questionBank[i][6].append(tag)
                QM_checkValidity(1, i)
            inFile.close()
            QM_questionDisplayList.append("<add new question>")
            QM_qBank_question_comBx.config(values=QM_questionDisplayList)
            QM_qBank_question_comBx.current(0)
            QM_updateForm()
            if warningMsg:
                m.display(104, QM_window_tL) # Questions QM_load warning
            else:
                m.display(105, QM_window_tL) # Questions QM_loaded successfully
   
        def QM_save():
            outFilePath = tkinter.filedialog.asksaveasfilename(\
                parent=QM_window_tL,\
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
            m.display(106, QM_window_tL) # Questions QM_saved successfully

        QM_questionDisplayList = ["<add new question>"]
        QM_points_tkSVar = tkinter.StringVar()
        QM_time_tkSVar = tkinter.StringVar()
        QM_tag_tkSVar = tkinter.StringVar(value="")

        QM_window_tL = tkinter.Toplevel()
        QM_window_tL.title("Question Manager")
        QM_window_tL.geometry("500x600")
        QM_window_tL.resizable(width=False, height=False)

        QM_qBank_frm = tkinter.LabelFrame(QM_window_tL, text="Question Bank")
        QM_qBank_question_lbl = tkinter.Label(QM_qBank_frm, text="Selected question:", anchor="w")
        QM_qBank_question_comBx = tkinter.ttk.Combobox(QM_qBank_frm, height=10, state="readonly")
        QM_qBank_question_comBx.bind("<<ComboboxSelected>>", QM_updateForm)
        QM_qBank_buttons_frm = tkinter.Frame(QM_qBank_frm)
        QM_qBank_buttons_clear_btn = tkinter.Button(QM_qBank_buttons_frm, text="Clear Selected Question", command=QM_clear, state="disabled")
        QM_qBank_buttons_clearAll_btn = tkinter.Button(QM_qBank_buttons_frm, text="Clear All Questions", command=QM_clearAll, state="disabled")
        QM_qBank_buttons_load_btn = tkinter.Button(QM_qBank_buttons_frm, text="Load Questions", command=QM_load)
        QM_qBank_buttons_save_btn = tkinter.Button(QM_qBank_buttons_frm, text="Save Questions", command=QM_save, state="disabled")
        QM_qBank_frm.grid(row=0, column=0, sticky="ew", padx=5)
        QM_qBank_question_lbl.grid(row=0, column=0, sticky="w", padx=(5,0), pady=5)
        QM_qBank_question_comBx.grid(row=0, column=1, sticky="ew", padx=(0,5), pady=5)
        QM_qBank_buttons_frm.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0,5))
        QM_qBank_frm.columnconfigure(0, weight=1)
        QM_qBank_frm.columnconfigure(1, weight=100)
        QM_qBank_buttons_clear_btn.grid(row=0, column=0, padx=(0,5), sticky="ew")
        QM_qBank_buttons_clearAll_btn.grid(row=0, column=1, padx=(0,5), sticky="ew")
        QM_qBank_buttons_load_btn.grid(row=0, column=2, padx=(0,5), sticky="ew")
        QM_qBank_buttons_save_btn.grid(row=0, column=3, sticky="ew")
        QM_qBank_buttons_frm.columnconfigure(0, weight=2)
        QM_qBank_buttons_frm.columnconfigure(1, weight=2)
        QM_qBank_buttons_frm.columnconfigure(2, weight=1)
        QM_qBank_buttons_frm.columnconfigure(3, weight=1)

        QM_error_lbl = tkinter.Label(QM_window_tL, text="", fg="red")
        QM_error_lbl.grid(row=1, column=0, sticky="ew", padx=5, pady=(5,0))

        QM_question_frm = tkinter.LabelFrame(QM_window_tL, text="Question")
        QM_question_input_txt = tkinter.Text(QM_question_frm, height=3, wrap="word")
        QM_question_input_yScb = tkinter.Scrollbar(QM_question_frm, orient=tkinter.VERTICAL, command=QM_question_input_txt.yview)
        QM_question_input_txt.config(yscrollcommand=QM_question_input_yScb.set)
        QM_question_input_txt.bind("<KeyRelease>", QM_updateQuestionDisplayList)
        QM_question_frm.grid(row=2, column=0, sticky="ew", padx=5)
        QM_question_input_txt.grid(row=0, column=0, sticky="ew", padx=(5,2), pady=5)
        QM_question_input_yScb.grid(row=0, column=1, padx=(0,5), pady=5)
        QM_question_frm.columnconfigure(0, weight=100)
        QM_question_frm.columnconfigure(1, weight=1)

        self.QM_options_quantity_tkIVar = tkinter.IntVar(value=2)
        self.QM_options_type_tkIVar = tkinter.IntVar(value=0)
        QM_options_frm = tkinter.LabelFrame(QM_window_tL, text="Options")
        QM_options_points_lbl = tkinter.Label(QM_options_frm, text="Question Point Value:", anchor="w")
        QM_options_points_ent = tkinter.Entry(QM_options_frm, width=10, textvariable=QM_points_tkSVar, state="disabled")
        QM_options_time_lbl = tkinter.Label(QM_options_frm, text="Time Limit (in seconds):", anchor="w")
        QM_options_time_ent = tkinter.Entry(QM_options_frm, width=10, textvariable=QM_time_tkSVar, state="disabled")
        QM_options_typeSingle_rad = tkinter.Radiobutton(QM_options_frm, text="Single Answer", variable=self.QM_options_type_tkIVar, value=0, command=QM_enableChoices, state="disabled")
        QM_options_typeMulti_rad = tkinter.Radiobutton(QM_options_frm, text="Multiple Answers", variable=self.QM_options_type_tkIVar, value=1, command=QM_enableChoices, state="disabled")
        QM_options_quantity_lbl = tkinter.Label(QM_options_frm, text="Choices:", anchor="w")
        QM_options_quantity_spnBx = tkinter.ttk.Spinbox(QM_options_frm, width=5, from_=2, to=5, command=QM_enableChoices, textvariable=self.QM_options_quantity_tkIVar, state="disabled")
        QM_options_frm.grid(row=3, column=0, sticky="ew", padx=5)
        QM_options_points_lbl.grid(row=0, column=0, sticky="w", padx=(5,0), pady=(5,0))
        QM_options_points_ent.grid(row=0, column=1, sticky="w", pady=(5,0))
        QM_options_time_lbl.grid(row=1, column=0, sticky="w", padx=(5,0), pady=(0,5))
        QM_options_time_ent.grid(row=1, column=1, sticky="w", pady=(0,5))
        QM_options_typeSingle_rad.grid(row=0, column=2, sticky="w", padx=(10,0), pady=(5,0))
        QM_options_typeMulti_rad.grid(row=1, column=2, sticky="w", padx=(10,0), pady=(0,5))
        QM_options_quantity_lbl.grid(row=0, column=3, sticky="e", pady=(5,0))
        QM_options_quantity_spnBx.grid(row=0, column=4, sticky="ew", padx=(0,5), pady=(5,0))
        QM_options_frm.columnconfigure(0, weight=1)
        QM_options_frm.columnconfigure(1, weight=1)
        QM_options_frm.columnconfigure(2, weight=1)
        QM_options_frm.columnconfigure(3, weight=1)
        QM_options_frm.columnconfigure(4, weight=1)

        self.QM_answers_singleChoice_tkIVar = tkinter.IntVar(value=0)
        QM_answers_multiChoiceArray = []
        QM_answers_widgetArray = [[],[],[],[],[]]
        QM_answers_frm = tkinter.LabelFrame(QM_window_tL, text="Answers", relief="groove", bd=2)
        QM_answers_frm.grid(row=4, column=0, sticky="ew", padx=5)
        QM_answers_frm.columnconfigure(0, weight=1)
        QM_answers_frm.columnconfigure(1, weight=100)

        for i in range(0,5):
            QM_answers_multiChoiceArray.append(tkinter.BooleanVar(value=False))
            QM_answers_widgetArray[i].append(tkinter.Radiobutton(QM_answers_frm, variable=self.QM_answers_singleChoice_tkIVar, value=i, command=QM_insertData, state="disabled"))
            QM_answers_widgetArray[i].append(tkinter.Checkbutton(QM_answers_frm, variable=QM_answers_multiChoiceArray[i], command=QM_insertData, state="disabled"))
            QM_answers_widgetArray[i].append(tkinter.Text(QM_answers_frm, height=2, state="disabled", bg="#dfdfdf", wrap="word"))
            QM_answers_widgetArray[i][0].grid(row=i, column=0, padx=5)
            QM_answers_widgetArray[i][1].grid(row=i, column=0, padx=5)
            QM_answers_widgetArray[i][1].grid_remove()
            QM_answers_widgetArray[i][2].grid(row=i, column=1, sticky="ew", padx=(0,5), pady=(0,5))
            QM_answers_frm.rowconfigure(i, weight=1)

        QM_tags_tagList = []
        QM_tags_frm = tkinter.LabelFrame(QM_window_tL, text="Tags", relief="groove", bd=2)
        QM_tags_newTag_lbl = tkinter.Label(QM_tags_frm, text="Enter new tag:", anchor="w")
        QM_tags_addTag_ent = tkinter.Entry(QM_tags_frm, textvariable=QM_tag_tkSVar, state="disabled")
        QM_tags_addTag_btn = tkinter.Button(QM_tags_frm, text="Add Tag", command=QM_addTag)
        QM_tags_tagList_lbl = tkinter.Label(QM_tags_frm, text="Added tags:", anchor="w")
        QM_tags_tagList_comBx = tkinter.ttk.Combobox(QM_tags_frm, height=4, state="disabled", values=QM_tags_tagList)
        QM_tags_clear_btn = tkinter.Button(QM_tags_frm, text="Clear Selected Tag", command=QM_removeTag, state="disabled")
        QM_tags_clearAll_btn = tkinter.Button(QM_tags_frm, text="Clear All Tags", command=QM_removeAllTags, state="disabled")
        QM_tags_frm.grid(row=5, column=0, padx=5, sticky="ew")
        QM_tags_newTag_lbl.grid(column=0, row=0, sticky="w", padx=(5,0), pady=(5,0))
        QM_tags_addTag_ent.grid(column=1, row=0, sticky="ew", pady=(5,0))
        QM_tags_addTag_btn.grid(column=2, row=0, sticky="ew", padx=5, columnspan=2)
        QM_tags_tagList_lbl.grid(column=0, row=1, sticky="w", padx=(5,0), pady=(0,5))
        QM_tags_tagList_comBx.grid(column=1, row=1, sticky="ew", pady=5)
        QM_tags_clear_btn.grid(column=2, row=1, sticky="ew", padx=5, pady=5)
        QM_tags_clearAll_btn.grid(column=3, row=1, sticky="ew", padx=(0,5), pady=5)
        QM_tags_frm.columnconfigure(0, weight=1)
        QM_tags_frm.columnconfigure(1, weight=1)
        QM_tags_frm.columnconfigure(2, weight=1)
        QM_tags_frm.columnconfigure(3, weight=1)

        for i in range(QM_window_tL.grid_size()[1]):
            QM_window_tL.rowconfigure(i, weight=1)

        for i in range(QM_window_tL.grid_size()[0]):
            QM_window_tL.columnconfigure(i, weight=1)

        if len(self.questionBank) != 0:
            QM_questionDisplayList.clear()
            for inArray in self.questionBank:
                QM_questionDisplayList.append(inArray[0])
            QM_questionDisplayList.append("<add new question>")

        QM_qBank_question_comBx.config(values=QM_questionDisplayList)
        QM_qBank_question_comBx.current(0)
        QM_updateForm()
        QM_window_tL.focus_set()
        QM_window_tL.grab_set()

    def openOptionWindow(self):
        def EO_updateOptions():
            if not self.examOptions[2].get() and not self.examOptions[3].get(): # If both exam and question time limits are disabled
                self.examOptions[4].set(False)
                EO_displayRemainingTime_chk.config(state="disabled")
            else:
                EO_displayRemainingTime_chk.config(state="normal")
            if self.examOptions[2].get(): # If exam time limit is enabled
                EO_examTime_lbl.config(state="normal")
                EO_examTime_spnBx.config(state="readonly")
            else:
                EO_examTime_lbl.config(state="disabled")
                EO_examTime_spnBx.config(state="disabled")

            if self.examOptions[3].get() or self.examOptions[6].get(): # If question time limit or sudden death mode is enabled
                self.examOptions[5].set(False)
                EO_enableBacktracking_chk.config(state="disabled")
            else:
                EO_enableBacktracking_chk.config(state="normal")
            if self.examOptions[6].get(): # If sudden death mode is enabled
                self.examOptions[7].set(False)
                EO_study_chk.config(state="disabled")
            else:
                EO_study_chk.config(state="normal")
            if self.examOptions[7].get(): # If study mode is enabled
                self.examOptions[6].set(False)
                EO_suddenDeath_chk.config(state="disabled")
            else:
                EO_suddenDeath_chk.config(state="normal")

        EO_window_tL = tkinter.Toplevel()
        EO_window_tL.title("Exam Options")
        EO_window_tL.geometry("300x300")
        EO_window_tL.resizable(width=False, height=False)
        EO_window_tL.columnconfigure(0, weight=1)
        EO_window_tL.columnconfigure(1, weight=100)

        self.EO_examTime_tkIVar =       tkinter.IntVar(value="0")
        EO_shuffleQuestions_chk =       tkinter.Checkbutton(EO_window_tL, text="Shuffle Exam Questions", variable=self.examOptions[0], anchor="w")
        EO_shuffleChoices_chk =         tkinter.Checkbutton(EO_window_tL, text="Shuffle Question Choices", variable=self.examOptions[1], anchor="w")
        EO_enableExamTime_chk =         tkinter.Checkbutton(EO_window_tL, text="Enable Exam Time Limit", variable=self.examOptions[2], command=EO_updateOptions, anchor="w")
        EO_examTime_lbl =               tkinter.Label(EO_window_tL, text="Exam Time (in minutes):", state="disabled")
        EO_examTime_spnBx =             tkinter.Spinbox(EO_window_tL, width=5, from_=1, to=180, repeatinterval=4, command=EO_updateOptions, textvariable=self.EO_examTime_tkIVar, state="disabled")
        EO_enableQuestionTime_chk =     tkinter.Checkbutton(EO_window_tL, text="Enable Question Time Limit", variable=self.examOptions[3], command=EO_updateOptions, anchor="w")
        EO_displayRemainingTime_chk =   tkinter.Checkbutton(EO_window_tL, text="Display Remaining Time", variable=self.examOptions[4], command=EO_updateOptions, state="disabled", anchor="w")
        EO_enableBacktracking_chk =     tkinter.Checkbutton(EO_window_tL, text="Enable Previous Question", variable=self.examOptions[5], command=EO_updateOptions, anchor="w")
        EO_suddenDeath_chk =            tkinter.Checkbutton(EO_window_tL, text="Sudden Death Mode", variable=self.examOptions[6], command=EO_updateOptions, anchor="w")
        EO_study_chk =                  tkinter.Checkbutton(EO_window_tL, text="Study Mode", variable=self.examOptions[7], command=EO_updateOptions, anchor="w")
        EO_displayCorrectChoice_chk =   tkinter.Checkbutton(EO_window_tL, text="Show Correct Answers Upon Completion", variable=self.examOptions[8], command=EO_updateOptions, anchor="w")

        EO_shuffleQuestions_chk.grid    (column=0, row=0, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_shuffleChoices_chk.grid      (column=0, row=1, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_enableExamTime_chk.grid      (column=0, row=2, sticky="ew", padx=5, pady=(5,0))
        EO_examTime_lbl.grid            (column=0, row=3, sticky="w", padx=5, pady=(5,0))
        EO_examTime_spnBx.grid          (column=1, row=3, sticky="ew", padx=5, pady=(5,0))
        EO_enableQuestionTime_chk.grid  (column=0, row=4, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_displayRemainingTime_chk.grid(column=0, row=5, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_enableBacktracking_chk.grid  (column=0, row=6, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_suddenDeath_chk.grid         (column=0, row=7, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_study_chk.grid               (column=0, row=8, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        EO_displayCorrectChoice_chk.grid(column=0, row=9, columnspan=2, sticky="ew", padx=5, pady=5)

        EO_window_tL.focus_set()
        EO_window_tL.grab_set()
        EO_updateOptions()

    def startExam(self):
        def EX_exit():
            EX_window_tL.destroy()

        def EX_finishExam(check):
            if check:
                nonlocal EX_exam_currentQuestion
                if not EX_examQuestions[EX_exam_currentQuestion][8]:
                    if not m.display(200, EX_window_tL): # No answer selected; Confirm continuing to next question
                        return
            nonlocal EX_examTags
            nonlocal EX_reviewFlag
            nonlocal EX_endTime
            EX_reviewFlag = True
            for i in range(0,1):
                if self.EX_cycleTask[i] != None:
                    EX_window_tL.after_cancel(self.EX_cycleTask[i])
                    self.EX_cycleTask[i] = None
            EX_exam_frm.grid_remove()
            EX_results_frm.grid()
            examLength = len(EX_examQuestions)
            correctAnswers = 0
            maxPoints = 0.0
            points = 0.0
            score = 0.0
            EX_endTime = int(time.time())
            minutes = int((EX_endTime - EX_startTime) // 60)
            seconds = int((EX_endTime - EX_startTime) % 60)

            for question in EX_examQuestions:
                maxPoints += question[1]
                checkArray = []
                for answer in question[8]:
                    checkArray.append(question[5][answer][0])
                checkArray.sort()
                if question[4] == checkArray:
                    correctAnswers += 1
                    points += question[1]
                    for tag in question[6]:
                        for targetTag in EX_examTags:
                            if tag == targetTag[0]:
                                targetTag[1] += question[1]
                                targetTag[2] += question[1]
                else:
                    partialCredit = 0
                    if question[3]:
                        for answer in checkArray:
                            if answer in question[4]:
                                partialCredit += 1/len(question[4])
                            else:
                                partialCredit -= 1/len(question[4])
                        if partialCredit < 0:
                            partialCredit = 0.0
                        points += partialCredit
                    for tag in question[6]:
                        for targetTag in EX_examTags:
                            if tag == targetTag[0]:
                                targetTag[1] += partialCredit
                                targetTag[2] += question[1]

            score = (points / maxPoints) * 100

            EX_results_correctAnswerRatio_tkSVar.set("Correct answers: " + str(correctAnswers) + " out of " + str(examLength))
            EX_results_pointsRatio_tkSVar.set("Points earned: " + format(float(points), ".2f") + " out of " + format(float(maxPoints), ".2f"))
            EX_results_score_tkSVar.set("Exam score: " + format(float(score), ".2f") + "%")
            EX_results_time_tkSVar.set("Time used: " + str(minutes) + ":" + format(seconds, "02d"))
            EX_results_tags_lbx.delete(0, "end")
            for inArray in EX_examTags:
                outString = inArray[0].ljust(20) + "     " + format(float(inArray[1]), ".2f") + " / " + format(float(inArray[2]), ".2f") + \
                    "     " + format(float((inArray[1]/inArray[2])*100), ".2f") + "%"
                EX_results_tags_lbx.insert("end", outString)
        def EX_examResults():
            EX_exam_frm.grid_remove()
            EX_results_frm.grid()

        def EX_changeQuestion(direction):
            nonlocal EX_exam_currentQuestion
            if direction == 0:
                EX_exam_currentQuestion -= 1
                EX_exam_buttons_next_btn.grid()
                EX_exam_buttons_finish_btn.grid_remove()
                if EX_exam_currentQuestion == 0:
                    EX_exam_buttons_previous_btn.config(state="disabled")
            else:
                if (self.examOptions[5].get() and not self.examOptions[6].get()) or EX_reviewFlag:
                    EX_exam_buttons_previous_btn.config(state="normal")
                elif self.examOptions[6].get():
                    checkArray = []
                    for answer in EX_examQuestions[EX_exam_currentQuestion][8]:
                        checkArray.append(EX_examQuestions[EX_exam_currentQuestion][5][answer][0])
                    checkArray.sort()
                    if EX_examQuestions[EX_exam_currentQuestion][4] != checkArray:
                        EX_finishExam(False)
                else:
                    if not EX_examQuestions[EX_exam_currentQuestion][8] and direction == 1:
                        if not m.display(200, EX_window_tL): # No answer selected; Confirm continuing to next question
                            return
                    elif self.examOptions[3].get() and EX_exam_currentQuestion >= len(EX_examQuestions) - 1:
                        EX_finishExam(False)
                        return
                EX_exam_currentQuestion += 1
            EX_updateDisplay()

        def EX_updateDisplay():
            nonlocal EX_exam_currentQuestion
            nonlocal EX_exam_remainingQuestionTime
            EX_exam_study_tkSVar.set("")
            EX_exam_questionVar_tkSVar.set(EX_examQuestions[EX_exam_currentQuestion][0])
            self.EX_exam_singleAnswer_tkIVar.set(None)
            for i in range(0,5):
                EX_exam_choiceArray[i].set("")
                EX_exam_multiAnswers[i].set(False)
                EX_exam_question_widgetArray[i][0].config(state="disabled")
                EX_exam_question_widgetArray[i][1].config(state="disabled")
                EX_exam_question_widgetArray[i][2].config(state="disabled")
                EX_exam_question_widgetArray[i][2].config(bg=self.defaultColor)
                EX_exam_question_widgetArray[i][0].grid_remove()
                EX_exam_question_widgetArray[i][1].grid_remove()
            count = 0
            for choice in EX_examQuestions[EX_exam_currentQuestion][5]:
                EX_exam_choiceArray[count].set(choice[1])
                if EX_examQuestions[EX_exam_currentQuestion][3] == 0:
                    if not EX_reviewFlag:
                        EX_exam_question_widgetArray[count][0].config(state="normal")
                    else:
                        EX_exam_buttons_check_btn.grid_remove()
                    EX_exam_question_widgetArray[count][0].grid()
                else:
                    if not EX_reviewFlag:
                        EX_exam_question_widgetArray[count][1].config(state="normal")
                    else:
                        EX_exam_buttons_check_btn.grid_remove()
                    EX_exam_question_widgetArray[count][1].grid()
                EX_exam_question_widgetArray[count][2].config(state="normal")
                count += 1
            for answer in EX_examQuestions[EX_exam_currentQuestion][8]:
                if EX_examQuestions[EX_exam_currentQuestion][3] == 0:
                    EX_exam_question_widgetArray[answer][0].select()
                else:
                    EX_exam_question_widgetArray[answer][1].select()
            if EX_exam_currentQuestion >= len(EX_examQuestions) - 1:
                if not EX_reviewFlag:
                    EX_exam_buttons_next_btn.grid_remove()
                    EX_exam_buttons_finish_btn.grid()
                else:
                    EX_exam_buttons_next_btn.config(state="disabled")
            else:
                if not EX_reviewFlag:
                    EX_exam_buttons_next_btn.grid()
                    EX_exam_buttons_finish_btn.grid_remove()
                else:
                    EX_exam_buttons_next_btn.config(state="normal")
            if self.examOptions[3].get() and not EX_reviewFlag:
                if EX_examQuestions[EX_exam_currentQuestion][2] != 0:
                    EX_exam_remainingQuestionTime = EX_examQuestions[EX_exam_currentQuestion][2] + 1
                if self.EX_cycleTask[1] != None:
                    EX_window_tL.after_cancel(self.EX_cycleTask[1])
                    self.EX_cycleTask[1] = None
                if EX_exam_remainingQuestionTime > 0:
                    EX_cycleQuestionCountdown()
                else:
                    EX_exam_remainingQuestionTime_tkSVar.set("Question time remaining: No time limit")
            elif EX_reviewFlag:
                EX_checkAnswer()

        def EX_selectAnswer():
            EX_examQuestions[EX_exam_currentQuestion][8].clear()
            EX_exam_study_tkSVar.set("")
            if EX_examQuestions[EX_exam_currentQuestion][3] == 0:
                EX_examQuestions[EX_exam_currentQuestion][8].append(self.EX_exam_singleAnswer_tkIVar.get())
            else:
                for i in range(0,5):
                    if EX_exam_multiAnswers[i].get():
                        EX_examQuestions[EX_exam_currentQuestion][8].append(i)

        def EX_checkAnswer():
            checkArray = []
            maxPoints = EX_examQuestions[EX_exam_currentQuestion][1]
            points = 0.0
            for answer in EX_examQuestions[EX_exam_currentQuestion][8]:
                checkArray.append(EX_examQuestions[EX_exam_currentQuestion][5][answer][0])
            checkArray.sort()
            if EX_examQuestions[EX_exam_currentQuestion][4] == checkArray:
                   EX_exam_study_tkSVar.set("Correct\n" + str(maxPoints) + " out of " + str(maxPoints) + " points")
                   EX_exam_study_lbl.config(fg="#00af00")
            else:
                if EX_examQuestions[EX_exam_currentQuestion][3]:
                    for answer in checkArray:
                        if answer in EX_examQuestions[EX_exam_currentQuestion][4]:
                            points += 1/len(EX_examQuestions[EX_exam_currentQuestion][4])
                        else:
                            points -= 1/len(EX_examQuestions[EX_exam_currentQuestion][4])
                    if points < 0:
                        points = 0.0
                EX_exam_study_tkSVar.set("Incorrect\n" + str(points) + " out of " + str(maxPoints) + " points")
                EX_exam_study_lbl.config(fg="#ff0000")
            if self.examOptions[8].get():
                targetList = []
                for correctAnswer in EX_examQuestions[EX_exam_currentQuestion][4]:
                    for i in range(0, len(EX_examQuestions[EX_exam_currentQuestion][5])):
                        if correctAnswer == EX_examQuestions[EX_exam_currentQuestion][5][i][0]:
                            targetList.append(i)
                            break
                for location in targetList:
                    EX_exam_question_widgetArray[location][2].config(bg="#00ff00")

        def EX_startExam():
            nonlocal EX_examQuestions
            nonlocal EX_examTags
            nonlocal EX_tagsCheck
            nonlocal EX_reviewFlag
            nonlocal EX_exam_currentQuestion
            nonlocal EX_startTime
            nonlocal EX_exam_remainingExamTime
            EX_reviewFlag = False
            EX_exam_currentQuestion = 0
            EX_exam_buttons_previous_btn.config(state="disabled")
            EX_examQuestions = copy.deepcopy(self.questionBank)
            for question in EX_examQuestions:
                question.append([])
                for tag in question[6]:
                    if tag.lower() not in EX_tagsCheck:
                        EX_examTags.append([tag, 0, 0])
                        EX_tagsCheck.append(tag.lower())
            if self.examOptions[0].get():
                random.shuffle(EX_examQuestions)
            if self.examOptions[1].get():
                for question in EX_examQuestions:
                    random.shuffle(question[5])
            EX_exam_buttons_next_btn.config(state="normal")
            if len(EX_examQuestions) > 1:
                EX_exam_buttons_next_btn.grid()
                EX_exam_buttons_finish_btn.grid_remove()
            else:
                EX_exam_buttons_next_btn.grid_remove()
                EX_exam_buttons_finish_btn.grid()
            EX_startTime = int(time.time())
            if self.examOptions[2].get():
                EX_exam_remainingExamTime = (self.EO_examTime_tkIVar.get() * 60) + 1
                EX_cycleExamCountdown()
            EX_exam_frm.grid()
            EX_results_frm.grid_remove()

            EX_exam_buttons_previous_btn.grid()
            EX_exam_buttons_check_btn.grid()
            EX_exam_buttons_next_btn.grid()
            EX_exam_buttons_finish_btn.grid()
            EX_exam_buttons_finish_btn.grid_remove()
            EX_exam_buttons_results_btn.grid_remove()

            EX_updateDisplay()

        def EX_reviewExam():
            nonlocal EX_exam_currentQuestion
            EX_exam_currentQuestion = 0
            EX_exam_buttons_previous_btn.config(state="disabled")
            if len(EX_examQuestions) > 1:
                EX_exam_buttons_next_btn.grid()
                EX_exam_buttons_finish_btn.grid_remove()
            else:
                EX_exam_buttons_next_btn.grid_remove()
                EX_exam_buttons_finish_btn.grid()
            EX_exam_frm.grid()
            EX_results_frm.grid_remove()

            EX_exam_buttons_previous_btn.grid()
            EX_exam_buttons_results_btn.grid()
            EX_exam_buttons_next_btn.grid()
            EX_exam_buttons_finish_btn.grid_remove()

            EX_updateDisplay()

        def EX_cycleExamCountdown():
            nonlocal EX_exam_remainingExamTime
            EX_exam_remainingExamTime -= 1
            minute = EX_exam_remainingExamTime // 60
            second = EX_exam_remainingExamTime % 60
            if self.examOptions[4].get():
                EX_exam_remainingExamTime_tkSVar.set("Exam time remaining: " + str(minute) + ":" + format(second, "02d"))
            else:
                EX_exam_remainingExamTime_tkSVar.set("Exam time remaining: ?")
            if EX_exam_remainingExamTime > 0:
                self.EX_cycleTask[0] = EX_window_tL.after(1000, EX_cycleExamCountdown)
            else:
                EX_finishExam(False)

        def EX_cycleQuestionCountdown():
            nonlocal EX_exam_currentQuestion
            nonlocal EX_exam_remainingQuestionTime
            EX_exam_remainingQuestionTime -= 1
            minute = EX_exam_remainingQuestionTime // 60
            second = EX_exam_remainingQuestionTime % 60
            if self.examOptions[4].get():
                EX_exam_remainingQuestionTime_tkSVar.set("Question time remaining: " + str(minute) + ":" + format(second, "02d"))
            else:
                EX_exam_remainingQuestionTime_tkSVar.set("Question time remaining: ?")
            if EX_exam_remainingQuestionTime > 0:
                self.EX_cycleTask[1] = EX_window_tL.after(1000, EX_cycleQuestionCountdown)
            else:
                if EX_exam_currentQuestion < len(EX_examQuestions) - 1:
                    EX_changeQuestion(2)
                else:
                    EX_finishExam(False)

        def EX_bindEvent(i, event=None):
            nonlocal EX_examQuestions
            nonlocal EX_exam_question_widgetArray
            if EX_examQuestions[EX_exam_currentQuestion][3] == 0:
                EX_exam_question_widgetArray[i][0].select()
            else:
                EX_exam_question_widgetArray[i][1].toggle()
            EX_selectAnswer()

        EX_examQuestions = []
        EX_examTags = []
        EX_tagsCheck = []
        EX_startTime = 0
        EX_endTime = 0
        self.EX_cycleTask = [None, None]
        EX_reviewFlag = False
        EX_window_tL = tkinter.Toplevel()
        EX_window_tL.title("Exam")
        EX_window_tL.resizable(width=False, height=False)
        EX_window_tL.columnconfigure(0, weight=1)

        EX_exam_currentQuestion = 0
        EX_exam_remainingExamTime = 0
        EX_exam_remainingExamTime_tkSVar = tkinter.StringVar(value="Exam time remaining: No time limit")
        EX_exam_remainingQuestionTime = 0
        EX_exam_remainingQuestionTime_tkSVar = tkinter.StringVar(value="Question time remaining: No time limit")
        EX_exam_questionVar_tkSVar = tkinter.StringVar(value="")
        EX_exam_question_widgetArray = []
        self.EX_exam_singleAnswer_tkIVar = tkinter.IntVar(value=None)
        EX_exam_study_tkSVar = tkinter.StringVar(value="")
        EX_exam_multiAnswers = []
        EX_exam_choiceArray = []

        EX_exam_frm = tkinter.Frame(EX_window_tL)
        EX_exam_frm.columnconfigure(0, weight=1)

        EX_exam_time_frm = tkinter.Frame(EX_exam_frm)
        EX_exam_time_exam_lbl = tkinter.Label(EX_exam_time_frm, textvariable=EX_exam_remainingExamTime_tkSVar, anchor="w")
        EX_exam_time_question_lbl = tkinter.Label(EX_exam_time_frm, textvariable=EX_exam_remainingQuestionTime_tkSVar, anchor="w")
        EX_exam_question_frm = tkinter.Frame(EX_exam_frm)
        EX_exam_question_frm.columnconfigure(0, weight=1)
        EX_exam_question_frm.columnconfigure(1, weight=1000)
        EX_exam_question_lbl = tkinter.Label(EX_exam_question_frm, textvariable=EX_exam_questionVar_tkSVar, anchor="w", justify="left", wraplength=440)

        for i in range(0,5):
            EX_exam_multiAnswers.append(tkinter.BooleanVar(value=False))
            EX_exam_choiceArray.append(tkinter.StringVar(value=""))
            EX_exam_question_widgetArray.append([])
            EX_exam_question_widgetArray[i].append(tkinter.Radiobutton(EX_exam_question_frm, variable=self.EX_exam_singleAnswer_tkIVar, value=i, command=EX_selectAnswer, state="disabled"))
            EX_exam_question_widgetArray[i].append(tkinter.Checkbutton(EX_exam_question_frm, variable=EX_exam_multiAnswers[i], command=EX_selectAnswer, state="disabled"))
            EX_exam_question_widgetArray[i].append(tkinter.Label(EX_exam_question_frm, textvariable=EX_exam_choiceArray[i], state="disabled", anchor="w", justify="left", wraplength=400))
            EX_exam_question_widgetArray[i][0].grid(row=i+1, column=0, sticky="w", padx=5)
            EX_exam_question_widgetArray[i][1].grid(row=i+1, column=0, sticky="w", padx=5)
            EX_exam_question_widgetArray[i][1].grid_remove()
            EX_exam_question_widgetArray[i][2].grid(row=i+1, column=1, sticky="ew", padx=(0,5), pady=(0,5))
            EX_exam_question_widgetArray[i][2].bind("<Button-1>", functools.partial(EX_bindEvent, i))
        EX_exam_study_lbl = tkinter.Label(EX_exam_frm, textvariable=EX_exam_study_tkSVar)
        EX_exam_buttons_frm = tkinter.Frame(EX_exam_frm)
        EX_exam_buttons_frm.columnconfigure(0, weight=1)
        EX_exam_buttons_frm.columnconfigure(1, weight=1)
        EX_exam_buttons_frm.columnconfigure(2, weight=1)
        EX_exam_buttons_previous_btn = tkinter.Button(EX_exam_buttons_frm, width=20, height=2, text="Previous\nQuestion", command=functools.partial(EX_changeQuestion, 0), state="disabled")
        EX_exam_buttons_check_btn = tkinter.Button(EX_exam_buttons_frm, width=20, height=2, text="Check\nAnswer", command=EX_checkAnswer, state="disabled")
        EX_exam_buttons_results_btn = tkinter.Button(EX_exam_buttons_frm, width=20, height=2, text="Exam\nResults", command=EX_examResults)
        EX_exam_buttons_next_btn = tkinter.Button(EX_exam_buttons_frm, width=20, height=2, text="Next\nQuestion", command=functools.partial(EX_changeQuestion, 1))
        EX_exam_buttons_finish_btn = tkinter.Button(EX_exam_buttons_frm, width=20, height=2, text="Finish\nExam", command=functools.partial(EX_finishExam, True))

        EX_results_correctAnswerRatio_tkSVar = tkinter.StringVar(value="")
        EX_results_pointsRatio_tkSVar = tkinter.StringVar(value="")
        EX_results_score_tkSVar = tkinter.StringVar(value="")
        EX_results_time_tkSVar = tkinter.StringVar(value="")

        EX_results_frm = tkinter.Frame(EX_window_tL)
        EX_results_stats_frm = tkinter.Frame(EX_results_frm)
        EX_results_tags_frm = tkinter.Frame(EX_results_frm)
        EX_results_tags_frm.columnconfigure(0, weight=1)
        EX_results_buttons_frm = tkinter.Frame(EX_results_frm)
        EX_results_buttons_frm.columnconfigure(0, weight=1)
        EX_results_buttons_frm.columnconfigure(1, weight=1)
        EX_results_buttons_frm.columnconfigure(2, weight=1)

        EX_results_stats_correctAnswerRatio_lbl = tkinter.Label(EX_results_stats_frm, textvariable=EX_results_correctAnswerRatio_tkSVar, anchor="w")
        EX_results_stats_pointsRatio_lbl = tkinter.Label(EX_results_stats_frm, textvariable=EX_results_pointsRatio_tkSVar, anchor="w")
        EX_results_stats_score_lbl = tkinter.Label(EX_results_stats_frm, textvariable=EX_results_score_tkSVar, anchor="w")
        EX_results_stats_time_lbl = tkinter.Label(EX_results_stats_frm, textvariable=EX_results_time_tkSVar, anchor="w")

        EX_results_tags_lbl = tkinter.Label(EX_results_tags_frm, text="Category Scores by Tag")
        EX_results_tags_lbx = tkinter.Listbox(EX_results_tags_frm, height=5)
        EX_results_tags_yScb = tkinter.Scrollbar(EX_results_tags_frm, orient=tkinter.VERTICAL, command=EX_results_tags_lbx.yview)
        EX_results_tags_lbx.config(yscrollcommand=EX_results_tags_yScb.set)

        EX_results_buttons_restart_btn = tkinter.Button(EX_results_buttons_frm, width=10, height=2, text="Restart\nExam", command=EX_startExam)
        EX_results_buttons_review_btn = tkinter.Button(EX_results_buttons_frm, width=10, height=2, text="Review\nQuestions", command=EX_reviewExam)
        EX_results_buttons_exit_btn = tkinter.Button(EX_results_buttons_frm, width=10, height=2, text="Exit\nExam", command=EX_exit)

        EX_results_frm.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        EX_results_frm.columnconfigure(0, weight=1)
        EX_results_frm.grid_remove()
        EX_results_stats_frm.grid(row=0, column=0)
        EX_results_tags_frm.grid(row=1, column=0, sticky="ew", pady=5)
        EX_results_buttons_frm.grid(row=2, column=0, sticky="ew", pady=5)
        
        EX_results_stats_correctAnswerRatio_lbl.grid(row=0, column=0)
        EX_results_stats_pointsRatio_lbl.grid(row=1, column=0)
        EX_results_stats_score_lbl.grid(row=2, column=0)
        EX_results_stats_time_lbl.grid(row=3, column=0)

        EX_results_tags_lbl.grid(row=0, column=0, sticky="ew")
        EX_results_tags_lbx.grid(row=1, column=0, sticky="ew")
        EX_results_tags_yScb.grid(row=1, column=1, sticky="ns")

        EX_results_buttons_restart_btn.grid(row=0, column=0, sticky="ew")
        EX_results_buttons_review_btn.grid(row=0, column=1, sticky="ew", padx=5)
        EX_results_buttons_exit_btn.grid(row=0, column=2, sticky="ew")

        EX_exam_frm.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        EX_exam_frm.grid_remove()
 
        EX_exam_time_frm.grid(row=0, column=0, sticky="ew")
        EX_exam_time_exam_lbl.grid(row=0, column=0, sticky="ew")
        EX_exam_time_question_lbl.grid(row=1, column=0, sticky="ew")
        EX_exam_question_frm.grid(row=1, column=0, sticky="ew")
        EX_exam_question_lbl.grid(row=0, column=0, columnspan=2, sticky="ew", pady=20)
        EX_exam_study_lbl.grid(row=2, column=0, sticky="ew", pady=(0,5))

        EX_exam_buttons_frm.grid(row=3, column=0, sticky="ew")
        EX_exam_buttons_previous_btn.grid(row=0, column=0, sticky="ew")
        EX_exam_buttons_check_btn.grid(row=0, column=1, sticky="ew", padx=5)
        EX_exam_buttons_results_btn.grid(row=0, column=1, sticky="ew", padx=5)
        EX_exam_buttons_results_btn.grid_remove()
        EX_exam_buttons_next_btn.grid(row=0, column=2, sticky="ew")
        EX_exam_buttons_finish_btn.grid(row=0, column=2, sticky="ew")
        EX_exam_buttons_finish_btn.grid_remove()

        if self.examOptions[7].get():
            EX_exam_buttons_check_btn.config(state="normal")

        EX_startExam()

    def exitProgram(self):
        self.window_tk.destroy()

def start():
    _ = interface()