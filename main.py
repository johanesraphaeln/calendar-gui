import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
from time import strftime

todos = {}

def detailTodo(cb=None):
    win = tk.Toplevel()
    win.wm_title("Detail todo")
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)['text']
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value=selectedTodo['judul'])
    tk.Label(win, text='Tanggal:').grid(row=0, column=0, sticky='N')
    tk.Label(win, text='{} | {}'.format(tanggal, selectedTodo['judul'])).grid(row=0, column=1, sticky='E')
    tk.Label(win, text='Judul:').grid(row=1, column=0, sticky='N')
    tk.Entry(win, state='disabled', textvariable=judul).grid(row=1, column=1, sticky='E')
    tk.Label(win, text='Keterangan:').grid(row=2, column=0, sticky='N')
    keterangan = ScrolledText(win, width= 12, height= 5)
    keterangan.grid(row=2, column=1, sticky='E')
    keterangan.insert(tk.INSERT, selectedTodo['keterangan'])
    keterangan.configure(state='disabled')

def LoadTodos():
    global todos
    f = open('mytodo.dat', 'r')
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()

def SaveTodos():
    f = open('mytodo.dat', 'w')
    f.write(str(todos))
    f.close()

def delTodo():
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus()
    todos[tanggal].pop(treev.item(selectedItem)['text'])
    ListTodo()
def ListTodo(cb=None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("", "end", text=i, values=(todos[tanggal][i]['waktu'], todos[tanggal][i]['judul']))

def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        'waktu':'{}:{}'.format(jam.get(), menit.get()),
        'judul': judul.get(),
        'keterangan': keterangan.get('1.0', tk.END)
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()
def AddForm():
    win = tk.Toplevel()
    win.wm_title("+")
    jam = tk.IntVar(value= 10)
    menit = tk.IntVar(value= 30)
    judul = tk.StringVar(value="")
    tk.Label(win, text= 'Waktu:').grid(row= 0, column= 0)
    tk.Spinbox(win, from_= 0, to= 23,  textvariable= jam, width= 3).grid(row= 0, column= 1)
    tk.Spinbox(win, from_= 0, to= 59,  textvariable= menit, width= 3).grid(row= 0, column= 2)
    tk.Label(win, text='Judul:').grid(row=1, column=0)
    tk.Entry(win, textvariable= judul).grid(row=1, column= 1, columnspan= 2)
    tk.Label(win, text='Keterangan:').grid(row=2, column= 0)
    keterangan = ScrolledText(win, width= 12, height= 5)
    keterangan.grid(row=2, column=1, columnspan= 2, rowspan= 4)
    tanggal = str(cal.selection_get()) 
    tk.Button(win, text='Tambah', command= lambda: addTodo(win, tanggal, jam, menit, judul, keterangan), background ='green', foreground='white', font='Arial 8 bold').grid(row=6, column=1)

def title():
    waktu = strftime('%H:%M')
    tanggal = str(cal.selection_get())
    root.title((tanggal + " | " + waktu + " | Kalender").center(175))
    root.after(1000,title)

root = tk.Tk()
s = ttk.Style()
s.configure('Treeview', rowheight= 15)
root.title('Calendarku')

cal = Calendar(root, font='Consolas 15 bold', selectmode= 'day', locale='id_ID', cursor= 'hand2')
cal.grid(row= 0, column= 0, sticky= 'N', rowspan= 7)
cal['background'] = 'black'
cal['showweeknumbers'] = False
cal['weekendbackground'] = 'white'
cal['weekendforeground'] = 'black'
cal['othermonthbackground'] = 'gray'
cal['othermonthwebackground'] = 'gray'
cal['othermonthforeground'] = 'white'
cal['othermonthweforeground'] = 'white'
cal.bind("<<CalendarSelected>>", ListTodo)
tanggal = str(cal.selection_get())
treev = ttk.Treeview(root)
treev.grid(row= 0, column= 1, sticky= 'WNE', rowspan= 4, columnspan= 2)
scrollBar = tk.Scrollbar(root, orient= 'vertical', command= treev.yview)
scrollBar.grid(row= 0, column= 3, sticky= 'ENS', rowspan= 4)
treev.configure(yscrollcommand= scrollBar.set)
treev.bind("<Double-1>", detailTodo)
treev['columns'] = ("1", "2")
treev['show'] = 'headings'
treev.column('1', width= 100)
treev.heading('1', text= 'JAM')
treev.heading('2', text='JUDUL')


btnAdd = tk.Button(root, text='Tambah', font='Consolas 10 bold', width= 20, command= AddForm, background='orange', foreground='black')
btnAdd.grid(row= 4, column= 1, sticky= 'N')

btnDel = tk.Button(root, text= 'Hapus', font='Consolas 10 bold', width= 20, command= delTodo, background='red', foreground='black')
btnDel.grid(row= 4, column = 2, sticky= 'N')

btnLoad = tk.Button(root, text='Muat', font='Consolas 10 bold', width=20, command= LoadTodos, background='yellow', foreground='black')
btnLoad.grid(row=6, column =1 , sticky='S')

btnSave = tk.Button(root, text='Simpan', font='Consolas 10 bold', width= 20, command = SaveTodos, background='green', foreground='black')
btnSave.grid(row=6, column=2, sticky='S')
title()
root.mainloop()