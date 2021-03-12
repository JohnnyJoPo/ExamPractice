import tkinter.messagebox

def display(messageID, parentContainer):
    winType = 0
    title = ""
    message = ""

    # WinTypes
    # 0 Info box
    # 1 Warning
    # 2 Error
    # 3 Ok/Cancel Request (returns boolean)

    # Question manager messages
    if 100 <= messageID <= 199:
        if messageID == 100:
            winType = 2
            title = "Error"
            message = "Please enter a valid tag name. Tag names may only contain alphanumeric characters and underscores."

        elif messageID == 101:
            winType = 2
            title = "Error"
            message = "This tag has already been added to this question. Tag names are not case-sensitive."

        elif messageID == 102:
            winType = 2
            title = "Error"
            message = "Please select a tag to delete from the drop down menu."

        elif messageID == 103:
            winType = 3
            title = "Confirm Deletion"
            message = "All currently configured questions will be cleared. Continue?"

        elif messageID == 104:
            winType = 1
            title = "Warning"
            message = "The input data may be faulty. Please check that all information is correct."

        elif messageID == 105:
            winType = 0
            title = "Load Complete"
            message = "Question configuration loaded successfully."

        elif messageID == 106:
            winType = 0
            title = "Save Complete"
            message = "Question configuration saved successfully."

    if winType == 3:
        return returnFeedback(winType, title, message, parentContainer)
    else:
        returnFeedback(winType, title, message, parentContainer)

## Takes input message and displays it via messagebox
def returnFeedback(winType, title, message, parentContainer):
    if winType == 0:
        tkinter.messagebox.showinfo(title, message, parent=parentContainer)
    elif winType == 1:
        tkinter.messagebox.showwarning(title, message, parent=parentContainer)
    elif winType == 2:
        tkinter.messagebox.showerror(title, message, parent=parentContainer)
    elif winType == 3:
        return tkinter.messagebox.askokcancel(title, message, parent=parentContainer)