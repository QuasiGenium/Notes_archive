from data import db_session
from parser import from_PDF_to_text
from data.notes import Note


def main():
    db_session.global_init("db/notes.db")
    book = from_PDF_to_text()
    db_sess = db_session.create_session()
    for i in book:
        n = Note()
        n.id = i[0]
        n.date = i[1]
        n.created_date = i[1]
        n.text = i[2]
        if '#' in i[2]:
            j = i[2].split()[::-1]
            j2 = []
            for k in j:
                if k[0] == '#':
                    j2.append(k)
            n.tags = ' '.join(j2)
        db_sess.add(n)
    db_sess.commit()


if __name__ == '__main__':
    main()