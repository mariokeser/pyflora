import tkinter as tk

app = tk.Tk()

frames = []
widgets = []

def createwidgets():
    global widgetNames
    global frameNames

    frame = tk.Frame(app, borderwidth=2, relief="groove")
    frames.append(frame)

    frame.pack(side="top", fill="x")

    for i in range(3):
        widget = tk.Entry(frame)
        widgets.append(widget)

        widget.pack(side="left")

createWidgetButton = tk.Button(app, text="createWidgets", command=createwidgets)
createWidgetButton.pack(side="bottom", fill="x")

app.mainloop()