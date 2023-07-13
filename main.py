from data import db_session
from data.notes import Note
from tkinter import *
import os

choose = ()

db_session.global_init("db/notes.db")
db_ses = db_session.create_session()

const = len(db_ses.query(Note).all())

db_ses.commit()


def get_list_of_notes(n=None, f='', s=0, oa=0):
    db_session.global_init("db/notes.db")
    db_sess = db_session.create_session()
    notes = {i.id: {'text': i.text if i.text else '', 'tags': i.tags if i.tags else '', 'date': i.date,
                    'ad_tags': i.ad_tags if i.ad_tags else '', 'created_date': i.created_date}
             for i in db_sess.query(Note).all()}
    a = '\n'
    if f == '':
        db_sess.commit()
        if s:
            return [f"{i} - {notes[i]['text'].split(a)[0]}" for i in notes.keys()][::-1]
        return [f"{i} - {notes[i]['text'].split(a)[0]}" for i in notes.keys()]
    else:
        ts = f.split()
        result = {}
        prams = {0: lambda x, y: y in x['tags'].lower() or y in x["ad_tags"].lower(),
                 1: lambda x, y: y in x['tags'].lower(),
                 2: lambda x, y: y in x['text'].lower(),
                 3: lambda x, y: y in x['tags'].lower() or y in x["ad_tags"].lower() or y in x['text'].lower()}
        for i in range(1, const + 1):
            flag = True if not oa else False
            for j in ts:
                if not prams[n](notes[i], j) and oa == 0:
                    flag = False
                    break
                elif prams[n](notes[i], j) and oa == 1:
                    flag = True
                    break
            if flag:
                result[i] = notes[i]
        if s:
            return [f"{i} - {notes[i]['text'].split(a)[0]}" for i in result.keys()][::-1]
        return [f"{i} - {notes[i]['text'].split(a)[0]}" for i in result.keys()]


def get_item_from_db(n):
    db_session.global_init("db/notes.db")
    db_sess = db_session.create_session()
    note = db_sess.query(Note).filter(Note.id == int(n)).first()
    return {note.id: {'text': note.text if note.text else '', 'tags': note.tags if note.tags else '', 'date': note.date,
                      'ad_tags': note.ad_tags if note.ad_tags else '', 'created_date': note.created_date}}


def view_one_note(a):
    oot = Tk()
    m = a[list(a.keys())[0]]

    oot.geometry('400x400+600+150')
    oot.title(f'Заметка номер {list(a.keys())[0]}')
    oot.resizable(width=False, height=False)

    count = Label(oot, text=m['date'].strftime("%A %d-%B-%Y %H:%M"))
    count.place(relx=0.05, rely=0.03)

    v = Scrollbar(oot, orient='vertical')
    v.pack(side=RIGHT, fill='y')

    text = Text(oot, width=44, height=20, yscrollcommand=v.set)
    text.place(relx=0.05, rely=0.1)
    text.insert(END, m['text'] + '\n\n' + m['ad_tags'])
    v.config(command=text.yview)

    fun = lambda *n: change_ad_tags(list(a.keys())[0])

    btn = Button(oot, text='Изменить доп. теги', width=45, height=1, command=fun)
    btn.place(relx=0.1, rely=0.92)

    oot.mainloop()


def change_ad_tags(n):
    db_session.global_init("db/notes.db")
    db_sess = db_session.create_session()
    note = db_sess.query(Note).filter(Note.id == int(n)).first()

    def save(*x):
        a = text.get("1.0", END)
        a = a.replace('\n', ' ')
        note.ad_tags = a
        db_sess.commit()
        ot.destroy()

    ot = Tk()
    ot.geometry('400x100+650+200')
    ot.title(f'Редактор доп. тегов заметки №{n}')
    ot.resizable(width=False, height=False)

    text = Text(ot, width=44, height=4)
    if note.ad_tags == None:
        text.insert(END, '')
    else:
        text.insert(END, note.ad_tags)
    text.place(relx=0.05, rely=0)

    save = Button(ot, text='Сохранить', width=10, height=1, command=save)
    save.place(relx=0.75, rely=0.73)

    cancel = Button(ot, text='Отмена', width=10, height=1, command=lambda: ot.destroy())
    cancel.place(relx=0.05, rely=0.73)

    ot.mainloop()


def main():
    def btn_def():
        if choose:
            os.startfile(fr'ARCHIVE\{_listbox.get(choose).split()[0]}.pdf')

    def list_def(*n):
        global choose
        if choose != _listbox.curselection():
            choose = _listbox.curselection()
        else:
            a = get_item_from_db(_listbox.get(choose).split()[0])
            view_one_note(a)

    def filter_btn(*n):
        m = string.get().lower()
        for i in range(_listbox.size()):
            _listbox.delete(0)
        g = get_list_of_notes(var.get(), m, sort_var.get(), or_var.get())
        for i in g:
            _listbox.insert(_listbox.size(), i)
        sv.set(f'Колиство элементов в списке - {len(g)}')

    view_notes = get_list_of_notes()
    root = Tk()
    root.geometry('500x600+600+150')
    root.title('Архив заметок')
    root.resizable(width=False, height=False)

    frame = Frame(root)
    frame.place(relwidth=1, relheight=1)

    sv = StringVar()
    sv.set('Колиство элементов в списке - 522')
    count = Label(frame, textvariable=sv)
    count.place(relx=0.3, rely=0.83)

    string = Entry(frame, bg='white', width=34)
    string.pack(anchor=NW, padx=100, pady=78)

    fbtn = Button(frame, text='Фильтровать', width=11, height=1, command=filter_btn)
    fbtn.place(relx=0.624, rely=0.125)

    _listbox = Listbox(listvariable=Variable(value=view_notes), height=30, width=50)
    _listbox.pack(anchor=NW, padx=100, pady=100)
    _listbox.bind("<<ListboxSelect>>", list_def)

    btn = Button(frame, text='Открыть исходный файл', width=18, height=1, command=btn_def)
    btn.pack(fill=X, pady=20, side=BOTTOM)

    var = IntVar()
    var.set(0)
    _1 = Radiobutton(frame, text="по всем\nтегам", variable=var, value=0)
    _2 = Radiobutton(frame, text="по основным\nтегам", variable=var, value=1)
    _3 = Radiobutton(frame, text="по тексту", variable=var, value=2)
    _4 = Radiobutton(frame, text="по всему", variable=var, value=3)
    _1.place(relx=0.8, rely=0.125)
    _2.place(relx=0.8, rely=0.19)
    _3.place(relx=0.8, rely=0.26)
    _4.place(relx=0.8, rely=0.29)

    dec = Label(frame, text='----------------')
    dec.place(relx=0.8, rely=0.323)

    sort_var = IntVar()
    sort_var.set(0)
    up = Radiobutton(frame, text="по возр.", variable=sort_var, value=0)
    down = Radiobutton(frame, text="по убыв.", variable=sort_var, value=1)
    up.place(relx=0.8, rely=0.35)
    down.place(relx=0.8, rely=0.384)

    inf = Label(frame, text='В заметке\nдолжны\nвстречаться:')
    inf.place(relx=0.04, rely=0.047+0.08)

    or_var = IntVar()
    or_var.set(0)
    _and = Radiobutton(frame, text="все кодовые\nслова", variable=or_var, value=0)
    _or = Radiobutton(frame, text="хотя бы одно\nкодовое\nслово", variable=or_var, value=1)
    _and.place(relx=0.001, rely=0.125+0.08)
    _or.place(relx=0.001, rely=0.19+0.08)

    root.mainloop()


if __name__ == '__main__':
    main()
