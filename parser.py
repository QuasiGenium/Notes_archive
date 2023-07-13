from PyPDF2 import PdfReader
import datetime

months = {'янв.': 1, 'февр.': 2, 'мар.': 3, 'апр.': 4,
          'мая': 5, 'июн.': 6, 'июл.': 7, 'авг.': 8,
          'сент.': 9, 'окт.': 10, 'нояб.': 11, 'дек.': 12}


def from_PDF_to_text() -> list:
    book = list()
    for i in range(1, 5):
        reader = PdfReader(f"ARCHIVE/{i}.pdf")
        pages = reader.pages
        text = '\n'.join([pages[i].extract_text() for i in range(len(pages))])
        text = '\n'.join(text.split('\n')[2:])
        print(text)
        date = text.split(':')[0].strip() + ':' + text.split(':')[1].strip()[:2]
        date = date.replace('\n', ' ').split()

        if len(date) == 5:
            date = datetime.datetime(int(date[2]), months[date[1]], int(date[0]),
                                     int(date[-1].split(':')[0]), int(date[-1].split(':')[1]))
        else:
            date = datetime.datetime(2023, months[date[1][:-1]], int(date[0]),
                                     int(date[-1].split(':')[0]), int(date[-1].split(':')[1]))
        text = '\n'.join(text.split('\n')[1:])
        try:
            if text[2] == ':' or text[1] == ':':
                text = '\n'.join(text.split('\n')[1:])
        except Exception as e:
            pass
        book.append([i, date, text])
    return book


if __name__ == '__main__':
    for i in from_PDF_to_text():
        print(i)
        pass

