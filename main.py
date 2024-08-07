import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from PIL import ImageTk, Image
import requests
from io import BytesIO



tilstand = {}

def oppdater_bilde(img_url):
    response = requests.get(img_url)
    img_data = response.content
    tilstand['img'] = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    tilstand['poster']['image'] = tilstand['img'] 

def sok_film(_ = None):
    onsket_film = tilstand['spørring'].get()
    url = ('http://www.omdbapi.com/?t=%s&apikey=251351e8' 
        % onsket_film.replace(' ', '+'))
    film_respons = requests.get(url).json()
    if film_respons['Response'] == 'True':
        tilstand['tittel'].set(film_respons['Title'])
        tilstand['regi'].set(film_respons['Director'])
        tilstand['ar'].set(film_respons['Year'])
        tilstand['plot'].set(film_respons['Plot'])
        oppdater_bilde(film_respons['Poster'])
    else:
        mb.showinfo('Ingen film funnet', 'Vi kunne dessverre ikke finne filmen med navnet "%s"' % onsket_film)

def sett_opp_og_start_gui():
    hoved_vindu = tk.Tk()
    hoved_vindu.title('Filmsøk')
    #hoved_vindu.geometry('500x700')
    hoved_vindu.minsize(500, 700)
    hoved_vindu.eval('tk::PlaceWindow . top') 
    
    hoved_ramme = ttk.Frame(hoved_vindu, padding='0.5i')
    hoved_ramme.pack(fill=tk.BOTH, expand=True)
    
    # Her skal GUI-koden
    spørre_ramme = ttk.Frame(hoved_ramme, relief=tk.GROOVE, padding='0.2i')
    spørre_ramme.pack(fill=tk.BOTH)

    resultat_ramme = ttk.Frame(hoved_ramme, relief=tk.SUNKEN,padding='0.2i')
    resultat_ramme.pack(fill=tk.BOTH, expand=True, pady=20 )

    ttk.Label(spørre_ramme, text='Skriv navnet på filmen du ønsker å søke opp(Engelsk tittel helst): ', font=('Helvetica','12','bold')).grid(row=0, column=0,columnspan=2)
    ttk.Label(spørre_ramme, text='Film: ').grid(row=1, column=0, sticky=tk.W )

    textbox_var = tk.StringVar()
    tilstand['spørring'] = textbox_var
    textbox = ttk.Entry(spørre_ramme, textvariable=textbox_var)
    textbox.grid(row=1, column=0, padx=20)
    ttk.Button(spørre_ramme, text='Send', command=sok_film).grid(row=1, column=2)
    textbox.bind('<Return>', sok_film)

    # Nederste frame

    
    ttk.Label(resultat_ramme, text='Tittel: '   ).grid(row=0, column=0, sticky=tk.NW )

    ttk.Label(resultat_ramme, text='År: '       ).grid(row=1, column=0, sticky=tk.NW )

    ttk.Label(resultat_ramme, text='Regissør: ' ).grid(row=2, column=0, sticky=tk.NW )

    ttk.Label(resultat_ramme, text='Plot: '     ).grid(row=3, column=0,sticky=tk.NW )

    ttk.Label(resultat_ramme, text='Poster: '   ).grid(row=4, column=0,sticky=tk.NW )

    #innehold til label
    
    tilstand['tittel'] = tk.StringVar(hoved_vindu, '')
    tilstand['ar'] = tk.StringVar(hoved_vindu, '')
    tilstand['regi'] = tk.StringVar(hoved_vindu, '')
    tilstand['plot'] = tk.StringVar(hoved_vindu, '')

    ttk.Label(resultat_ramme, textvariable=tilstand['tittel']   ).grid(row=0, column=1,padx=2, pady=2)

    ttk.Label(resultat_ramme, textvariable=tilstand['ar']       ).grid(row=1, column=1,sticky=tk.W)

    ttk.Label(resultat_ramme, textvariable=tilstand['regi']     ).grid(row=2, column=1,sticky=tk.W)

    ttk.Label(resultat_ramme, textvariable=tilstand['plot'],wraplength='400').grid(row=3, column=1,sticky=tk.W)


    tilstand['poster'] = ttk.Label(resultat_ramme)
    tilstand['poster'].grid(row=4, column=1)

    hoved_vindu.mainloop()


if __name__ == "__main__":
    sett_opp_og_start_gui()