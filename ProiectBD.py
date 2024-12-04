import tkinter
import pypyodbc as odbc
from tkinter import messagebox

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-R77CARD\SQLEXPRESS'
DATABASE_NAME = 'Analize_Lab'

connection_string = f"""
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
Trust_Connection=yes;
"""

def login():
    username = "admin"
    password = "123"
    if username_entry.get() == username and password_entry.get() == password:
        conn = odbc.connect(connection_string)
        print(conn)
        open_admin_window(conn)
    else:
        messagebox.showerror("Eroare", "Nume de utilizator sau parolă incorectă.")
        # Nu mai deschide automat fereastra pacientului



def open_admin_window(conn):
    admin_window = tkinter.Toplevel()
    admin_window.title("Panou de Administrare")
    admin_window.geometry("800x600")  # Dimensiunea ferestrei
    admin_window.configure(bg="#333333")

    # Mesaj de salut
    welcome_label = tkinter.Label(admin_window, text="BUNĂ ZIUA!", bg="#333333", fg="#FFFFFF", font=("Arial", 24))
    welcome_label.pack(pady=20)

    # Buton pentru inserare
    insert_button = tkinter.Button(admin_window, text="Inserare", command=lambda: open_insert_window(conn), bg="#F1CB7E", fg="#000000")
    insert_button.pack(pady=10)

    # Buton pentru update
    update_button = tkinter.Button(admin_window, text="Update", command=lambda: open_update_window(conn), bg="#F1CB7E", fg="#000000")
    update_button.pack(pady=10)

    # Buton pentru delete
    delete_button = tkinter.Button(admin_window, text="Delete", command=lambda: open_delete_window(conn), bg="#F1CB7E", fg="#000000")
    delete_button.pack(pady=10)

    # Buton pentru selectare
    select_button = tkinter.Button(admin_window, text="Selectare", command=lambda: open_select_window(conn), bg="#F1CB7E", fg="#000000")
    select_button.pack(pady=10)

def open_insert_window(conn):
    insert_window = tkinter.Toplevel()
    insert_window.title("Adaugă Pacient și Personal")
    insert_window.geometry("800x400")
    insert_window.configure(bg="#333333")

    left_frame = tkinter.Frame(insert_window, bg="#333333")
    left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    right_frame = tkinter.Frame(insert_window, bg="#333333")
    right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

    pacient_labels = ["Nume", "Prenume", "Data Nașterii", "CNP", "Gen", "Contact"]
    pacient_entries = {}
    for label in pacient_labels:
        lbl = tkinter.Label(left_frame, text=label, bg="#333333", fg="#FFFFFF")
        lbl.pack(pady=5)
        entry = tkinter.Entry(left_frame)
        entry.pack(pady=5)
        pacient_entries[label] = entry

    add_patient_button = tkinter.Button(left_frame, text="Adaugă Pacient", command=lambda: add_pacient(conn, pacient_entries), bg="#F1CB7E", fg="#000000")
    add_patient_button.pack(pady=20)

    # Dicționar pentru departamente și ID-uri
    departamente = {"Curatenie": 1, "Medical": 2, "Laborator": 6}

    personal_labels = ["Nume", "Prenume", "Funcție", "Contact"]
    personal_entries = {}
    for label in personal_labels:
        lbl = tkinter.Label(right_frame, text=label, bg="#333333", fg="#FFFFFF")
        lbl.pack(pady=5)
        entry = tkinter.Entry(right_frame)
        entry.pack(pady=5)
        personal_entries[label] = entry

    # Dropdown pentru selectarea departamentului
    departament_var = tkinter.StringVar(right_frame)
    departament_dropdown = tkinter.OptionMenu(right_frame, departament_var, *departamente.keys())
    departament_dropdown.pack(pady=5)

    # Câmp ascuns pentru DepartamentID
    departament_id_entry = tkinter.Entry(right_frame)
    personal_entries["DepartamentID"] = departament_id_entry

    # Actualizează DepartamentID când un departament este selectat
    def update_departament_id(*args):
        departament_id = departamente.get(departament_var.get(), "")
        departament_id_entry.delete(0, tkinter.END)
        departament_id_entry.insert(0, departament_id)

    departament_var.trace("w", update_departament_id)

    add_personal_button = tkinter.Button(right_frame, text="Adaugă Personal", command=lambda: add_personal(conn, personal_entries), bg="#F1CB7E", fg="#000000")
    add_personal_button.pack(pady=20)


def add_pacient(conn, entries):
    try:
        cursor = conn.cursor()
        # Construiește și execută interogarea SQL pentru a adăuga un nou pacient
        query = """INSERT INTO Pacient (Nume, Prenume, DataNasterii, CNP, Gen, Contact) VALUES (?, ?, ?, ?, ?, ?)"""
        data = (entries["Nume"].get(), entries["Prenume"].get(), entries["Data Nașterii"].get(), entries["CNP"].get(), entries["Gen"].get(), entries["Contact"].get())
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Succes", "Pacient adăugat cu succes în baza de date.")
    except Exception as e:
        # Afișează un mesaj de eroare dacă ceva nu merge bine
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def add_personal(conn, entries):
    try:
        cursor = conn.cursor()
        # Construiește și execută interogarea SQL pentru a adăuga un nou membru al personalului
        query = """INSERT INTO Personal (Nume, Prenume, Functie, Contact, DepartamentID) VALUES (?, ?, ?, ?, ?)"""
        data = (entries["Nume"].get(), entries["Prenume"].get(), entries["Funcție"].get(), entries["Contact"].get(), entries["DepartamentID"].get())
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Succes", "Personal adăugat cu succes în baza de date.")
    except Exception as e:
        # Afișează un mesaj de eroare dacă ceva nu merge bine
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()



def open_delete_window(conn):
    delete_window = tkinter.Toplevel()
    delete_window.title("Șterge Pacient")
    delete_window.geometry("400x300")  # Mărit pentru a include spațiul pentru afișarea programărilor
    delete_window.configure(bg="#333333")

    # Câmp de intrare pentru CNP
    cnp_label = tkinter.Label(delete_window, text="Introduceți CNP-ul pacientului:", bg="#333333", fg="#FFFFFF")
    cnp_label.pack(pady=10)
    cnp_entry = tkinter.Entry(delete_window)
    cnp_entry.pack(pady=10)

   # Buton pentru ștergerea pacientului
    delete_button = tkinter.Button(delete_window, text="Șterge Pacient", command=lambda: delete_pacient(conn, cnp_entry.get()), bg="#F1CB7E", fg="#000000")
    delete_button.pack(pady=10)

    # Zonă de text pentru afișarea programărilor
    appointments_text = tkinter.Text(delete_window, height=5, width=50, state=tkinter.DISABLED)
    appointments_text.pack(pady=10)

    # Buton pentru afișarea programărilor pacientului
    show_appointments_button = tkinter.Button(delete_window, text="Afișează Programările", command=lambda: show_appointments(conn, cnp_entry.get(), appointments_text), bg="#F1CB7E", fg="#000000")
    show_appointments_button.pack(pady=10)
    
# Câmpuri de intrare pentru data și ora
    data_label = tkinter.Label(delete_window, text="Introduceți data (YYYY-MM-DD):", bg="#333333", fg="#FFFFFF")
    data_label.pack(pady=10)
    data_entry = tkinter.Entry(delete_window)
    data_entry.pack(pady=10)

    ora_label = tkinter.Label(delete_window, text="Introduceți ora (HH:MM):", bg="#333333", fg="#FFFFFF")
    ora_label.pack(pady=10)
    ora_entry = tkinter.Entry(delete_window)
    ora_entry.pack(pady=10)

    # Buton pentru ștergerea programării
    delete_appointment_button = tkinter.Button(delete_window, text="Șterge Programare", command=lambda: delete_appointment(conn, cnp_entry.get(), data_entry.get(), ora_entry.get()), bg="#F1CB7E", fg="#000000")
    delete_appointment_button.pack(pady=20)

 

def show_appointments(conn, cnp, appointments_text):
    try:
        cursor = conn.cursor()
        #Afișează Programările
        query = """SELECT Programari.Data, Programari.Ora, Programari.Status 
                   FROM Programari
                   JOIN BuletinAnalize ON Programari.BuletinID = BuletinAnalize.BuletinID
                   JOIN Pacient ON BuletinAnalize.PacientID = Pacient.PacientID
                   WHERE Pacient.CNP = ?"""
        cursor.execute(query, (cnp,))
        rows = cursor.fetchall()

        appointments_text.config(state=tkinter.NORMAL)
        appointments_text.delete("1.0", tkinter.END)

        if rows:
            for row in rows:
                appointments_text.insert(tkinter.END, f"Data: {row[0]}, Ora: {row[1]}, Status: {row[2]}\n")
        else:
            appointments_text.insert(tkinter.END, "Nu există programări pentru CNP-ul specificat.\n")

        appointments_text.config(state=tkinter.DISABLED)

    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def delete_appointment(conn, cnp, data, ora):
    try:
        cursor = conn.cursor()
        query = """DELETE FROM Programari 
                   WHERE BuletinID IN (SELECT BuletinID FROM BuletinAnalize WHERE PacientID IN (SELECT PacientID FROM Pacient WHERE CNP = ?))
                   AND Data = ? AND Ora = ?"""
        cursor.execute(query, (cnp, data, ora))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Succes", "Programare ștearsă cu succes.")
        else:
            messagebox.showinfo("Informație", "Nicio programare găsită pentru datele specificate.")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def delete_pacient(conn, cnp):
    try:
        cursor = conn.cursor()
        query = """DELETE FROM Pacient WHERE CNP = ?"""
        cursor.execute(query, (cnp,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Succes", "Pacient șters cu succes.")
        else:
            messagebox.showinfo("Informație", "Niciun pacient găsit cu CNP-ul specificat.")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def open_update_window(conn):
    update_window = tkinter.Toplevel()
    update_window.title("Actualizează Informațiile Personalului și Analizelor")
    update_window.geometry("800x350")
    update_window.configure(bg="#333333")

    left_frame = tkinter.Frame(update_window, bg="#333333")
    left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    right_frame = tkinter.Frame(update_window, bg="#333333")
    right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

    # Câmpuri de intrare pentru actualizarea informațiilor personalului
    update_labels = ["Nume", "Prenume", "Funcție", "Contact"]
    update_entries = {}
    for label in update_labels:
        lbl = tkinter.Label(left_frame, text=label, bg="#333333", fg="#FFFFFF")
        lbl.pack(pady=5)
        entry = tkinter.Entry(left_frame)
        entry.pack(pady=5)
        update_entries[label] = entry

    # Dicționar pentru departamente și ID-uri
    departamente = {"Curatenie": 1, "Medical": 2, "Laborator": 6}

    # Dropdown pentru selectarea departamentului
    departament_var = tkinter.StringVar(left_frame)
    departament_dropdown = tkinter.OptionMenu(left_frame, departament_var, *departamente.keys())
    departament_dropdown.pack(pady=5)

    # Câmp ascuns pentru DepartamentID
    departament_id_entry = tkinter.Entry(update_window)
    update_entries["DepartamentID"] = departament_id_entry

    # Actualizează DepartamentID când un departament este selectat
    def update_departament_id(*args):
        departament_id = departamente.get(departament_var.get(), "")
        departament_id_entry.delete(0, tkinter.END)
        departament_id_entry.insert(0, departament_id)

    departament_var.trace("w", update_departament_id)

    # Buton pentru actualizarea personalului
    update_button = tkinter.Button(left_frame, text="Actualizează Personal", 
                                   command=lambda: update_personal(conn, update_entries), 
                                   bg="#F1CB7E", fg="#000000")
    update_button.pack(pady=20)

    # Formular pentru actualizarea prețului analizelor
    analiza_label = tkinter.Label(right_frame, text="Numele Analizei:", bg="#333333", fg="#FFFFFF")
    analiza_label.pack(pady=5)
    analiza_entry = tkinter.Entry(right_frame)
    analiza_entry.pack(pady=5)

    pret_label = tkinter.Label(right_frame, text="Pret Nou:", bg="#333333", fg="#FFFFFF")
    pret_label.pack(pady=5)
    pret_entry = tkinter.Entry(right_frame)
    pret_entry.pack(pady=5)

    update_pret_button = tkinter.Button(right_frame, text="Actualizează Preț Analiză", 
                                       command=lambda: update_pret_analiza(conn, analiza_entry.get(), pret_entry.get()), 
                                       bg="#F1CB7E", fg="#000000")
    update_pret_button.pack(pady=20)

def update_personal(conn, entries):
    try:
        cursor = conn.cursor()
        # Construiește și execută interogarea SQL pentru a actualiza personalul
        query = """UPDATE Personal SET Functie = ?, Contact = ?, DepartamentID = ? 
                   WHERE Nume = ? AND Prenume = ?"""
        data = (entries["Funcție"].get(), entries["Contact"].get(), entries["DepartamentID"].get(), entries["Nume"].get(), entries["Prenume"].get())
        cursor.execute(query, data)
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Succes", "Informațiile personalului au fost actualizate.")
        else:
            messagebox.showinfo("Informație", "Niciun personal găsit cu numele specificat.")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()



def update_pret_analiza(conn, nume_analiza, pret_nou):
    try:
        cursor = conn.cursor()
        query = "UPDATE Analize SET Pret = ? WHERE Nume = ?"
        cursor.execute(query, (pret_nou, nume_analiza))
        conn.commit()
        messagebox.showinfo("Succes", "Prețul analizei a fost actualizat.")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def open_select_window(conn):
    select_window = tkinter.Toplevel()
    select_window.title("Selectare Informații")
    select_window.geometry("600x400")
    select_window.configure(bg="#333333")

    # Frame pentru butoane
    buttons_frame = tkinter.Frame(select_window, bg="#333333")
    buttons_frame.pack(side=tkinter.LEFT, fill=tkinter.Y)

    # Frame pentru afișarea rezultatelor
    result_frame = tkinter.Frame(select_window, bg="#333333")
    result_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

    # Câmp de text pentru afișarea rezultatelor
    result_text = tkinter.Text(result_frame, height=15, width=100, state=tkinter.DISABLED)
    result_text.pack(pady=10)

    # Buton pentru prima interogare
    query1_button = tkinter.Button(select_window, text="Pacienti si Rezultatul Analizelor", command=lambda: execute_query1(conn, result_text), bg="#F1CB7E", fg="#000000")
    query1_button.pack(pady=10)

    # Buton pentru a doua interogare
    query2_button = tkinter.Button(select_window, text="Programari si Personal", command=lambda: execute_query2(conn, result_text), bg="#F1CB7E", fg="#000000")
    query2_button.pack(pady=10)

    # Dropdown pentru selectarea analizei
    analiza_var = tkinter.StringVar(select_window)
    analiza_dropdown = tkinter.OptionMenu(select_window, analiza_var, "Selectați Analiza")
    analiza_dropdown.pack(pady=5)

    # Populăm dropdown-ul cu analizele
    populate_analiza_dropdown(conn, analiza_var, analiza_dropdown)

    # Buton pentru executarea interogării
    query3_button = tkinter.Button(select_window, text="Afișează Pacienți in functie de analiza", command=lambda: execute_query3(conn, analiza_var.get(), result_text), bg="#F1CB7E", fg="#000000")
    query3_button.pack(pady=10)

     # Buton pentru executarea interogării 4
    query4_button = tkinter.Button(select_window, text="Afișează Programările Efectuate", command=lambda: execute_query4(conn, result_text), bg="#F1CB7E", fg="#000000")
    query4_button.pack(pady=10)

    # Buton pentru executarea interogării 5
    query5_button = tkinter.Button(select_window, text="Afișează Programările Neefectuate", command=lambda: execute_query5(conn, result_text), bg="#F1CB7E", fg="#000000")
    query5_button.pack(pady=10)

    # Adăugarea casetelor de text pentru introducerea datelor
    data_inceput_label = tkinter.Label(select_window, text="Data început (YYYY-MM-DD):", bg="#333333", fg="#FFFFFF")
    data_inceput_label.pack(pady=5)
    data_inceput_entry = tkinter.Entry(select_window)
    data_inceput_entry.pack(pady=5)

    data_sfarsit_label = tkinter.Label(select_window, text="Data sfârșit (YYYY-MM-DD):", bg="#333333", fg="#FFFFFF")
    data_sfarsit_label.pack(pady=5)
    data_sfarsit_entry = tkinter.Entry(select_window)
    data_sfarsit_entry.pack(pady=5)

    # Buton pentru afișarea programărilor între cele două date
    query_date_button = tkinter.Button(select_window, text="Afișează Programările între Date", command=lambda: execute_query_date(conn, data_inceput_entry.get(), data_sfarsit_entry.get(), result_text), bg="#F1CB7E", fg="#000000")
    query_date_button.pack(pady=10)

    # Adăugarea casetelor de text pentru introducerea datelor
    data_inceput_label = tkinter.Label(select_window, text="Data început (YYYY-MM-DD):", bg="#333333", fg="#FFFFFF")
    data_inceput_label.pack(pady=5)
    data_inceput_entry = tkinter.Entry(select_window)
    data_inceput_entry.pack(pady=5)

    data_sfarsit_label = tkinter.Label(select_window, text="Data sfârșit (YYYY-MM-DD):", bg="#333333", fg="#FFFFFF")
    data_sfarsit_label.pack(pady=5)
    data_sfarsit_entry = tkinter.Entry(select_window)
    data_sfarsit_entry.pack(pady=5)

    # Buton pentru afișarea analizelor cel mai frecvente analize efectuate
    query_analize_button = tkinter.Button(select_window, text="Afișează Analizele Frecvente", command=lambda: execute_query_analize(conn, data_inceput_entry.get(), data_sfarsit_entry.get(), result_text), bg="#F1CB7E", fg="#000000")
    query_analize_button.pack(pady=10)

    # Buton pentru afișarea analizelor cu cele mai multe rezultate anormale
    query_analize_anormale_button = tkinter.Button(buttons_frame, text="Afișează Analizele Anormale", command=lambda: execute_query_analize_anormale(conn, result_text), bg="#F1CB7E", fg="#000000")
    query_analize_anormale_button.pack(pady=10)

    # Buton pentru afișarea departamentului cu cel mai mare număr de personal
    query_departament_max_button = tkinter.Button(buttons_frame, text="Afișează Departamentele cu numarul de personal", command=lambda: execute_query_departament_max(conn, result_text), bg="#F1CB7E", fg="#000000")
    query_departament_max_button.pack(pady=10)

    most_expensive_analysis_button = tkinter.Button(buttons_frame, text="Afișează Cea Mai Scumpă Analiză și Pacienții", command=lambda: execute_query_most_expensive_analysis(conn, result_text), bg="#F1CB7E", fg="#000000")
    most_expensive_analysis_button.pack(pady=10)

    # Adăugarea unei etichete și a unui câmp de text pentru luna în frame-ul cu butoane
    month_label = tkinter.Label(buttons_frame, text="Introduceți Luna (1-12):", bg="#333333", fg="#FFFFFF")
    month_label.pack(pady=5)
    month_entry = tkinter.Entry(buttons_frame)
    month_entry.pack(pady=5)

    query_button = tkinter.Button(buttons_frame, text="Afișează Media Analizelor pe Luna Selectată", 
                              command=lambda: execute_query_avg_analysis_per_month(conn, result_text, month_entry.get()), 
                              bg="#F1CB7E", fg="#000000")
    query_button.pack(pady=10)



def execute_query_avg_analysis_per_month(conn, result_text, month):
    try:
        cursor = conn.cursor()
        query = """
        SELECT AVG(NumarAnalize) AS MediaAnalizelor, Luna
        FROM (
            SELECT COUNT(ba.BuletinID) AS NumarAnalize, MONTH(ba.Data) AS Luna
            FROM BuletinAnalize ba
            GROUP BY ba.PacientID, MONTH(ba.Data)
        ) AS AnalizePeLuna
        WHERE Luna = ?
        GROUP BY Luna;
        """
        cursor.execute(query, (month,))
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Luna: {row[1]}, Media Analizelor: {row[0]:.2f}\n")

        result_text.config(state=tkinter.DISABLED)
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def execute_query1(conn, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL care unește tabelele Pacient și BuletinAnalize
        query = """SELECT p.Nume, p.Prenume, ba.Rezultat
                   FROM Pacient p
                   JOIN BuletinAnalize ba ON p.PacientID = ba.PacientID;"""
        cursor.execute(query)
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Nume: {row[0]}, Prenume: {row[1]}, Rezultat Analiză: {row[2]}\n")

        result_text.config(state=tkinter.DISABLED)
        cursor.close()
    except Exception as e:
        messagebox.showerror("Eroare", str(e))



def execute_query2(conn, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL care unește tabelele necesare pentru a obține informații despre programări și personal
        query = """SELECT p.Nume, p.Prenume, pr.Data, pr.Ora, per.Nume, per.Prenume
                   FROM Programari pr
                   JOIN BuletinAnalize ba ON pr.BuletinID = ba.BuletinID
                   JOIN Pacient p ON ba.PacientID = p.PacientID
                   JOIN Personal per ON pr.PersonalID = per.PersonalID;"""
        cursor.execute(query)
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Pacient: {row[0]} {row[1]}, Data: {row[2]}, Ora: {row[3]}, Personal: {row[4]} {row[5]}\n")

        result_text.config(state=tkinter.DISABLED)
        cursor.close()
    except Exception as e:
        messagebox.showerror("Eroare", str(e))


def execute_query3(conn, analiza_selectata, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL pentru a găsi pacienții care au efectuat analiza selectată
        query = """SELECT p.Nume, p.Prenume
                   FROM Pacient p
                   JOIN BuletinAnalize ba1 ON p.PacientID = ba1.PacientID
                   JOIN BA ON ba1.BuletinID = BA.BuletinID
                   JOIN Analize a ON BA.AnalizeID = a.AnalizeID
                   WHERE a.Nume = ?"""
        cursor.execute(query, (analiza_selectata,))
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Nume: {row[0]}, Prenume: {row[1]}\n")

        result_text.config(state=tkinter.DISABLED)
        cursor.close()
    except Exception as e:
        messagebox.showerror("Eroare", str(e))


def execute_query4(conn, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL care unește tabelele necesare pentru a obține programările "Efectuate" și personalul care le-a efectuat
        query = """SELECT pr.Data, pr.Ora, per.Nume, per.Prenume
                   FROM Programari pr
                   JOIN Personal per ON pr.PersonalID = per.PersonalID
                   JOIN BuletinAnalize ba ON pr.BuletinID = ba.BuletinID
                   WHERE pr.Status = 'Efectuata';"""
        cursor.execute(query)
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Data: {row[0]}, Ora: {row[1]}, Personal: {row[2]} {row[3]}\n")

        result_text.config(state=tkinter.DISABLED)
        cursor.close()
    except Exception as e:
        messagebox.showerror("Eroare", str(e))

def execute_query5(conn, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL care unește tabelele necesare pentru a obține programările "Neefectuate" și personalul care le-a efectuat
        query = """SELECT pr.Data, pr.Ora, per.Nume, per.Prenume
                   FROM Programari pr
                   JOIN Personal per ON pr.PersonalID = per.PersonalID
                   JOIN BuletinAnalize ba ON pr.BuletinID = ba.BuletinID
                   WHERE pr.Status = 'Neefectuata';"""
        cursor.execute(query)
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Data: {row[0]}, Ora: {row[1]}, Personal: {row[2]} {row[3]}\n")

        result_text.config(state=tkinter.DISABLED)
        cursor.close()
    except Exception as e:
        messagebox.showerror("Eroare", str(e))


def execute_query_date(conn, data_inceput, data_sfarsit, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL pentru a găsi analizele efectuate între cele două date specificate
        query = """SELECT p.Nume, p.Prenume, a.Nume AS NumeAnaliza, ba1.Data, ba1.Rezultat
                   FROM Pacient p
                   JOIN BuletinAnalize ba1 ON p.PacientID = ba1.PacientID
                   JOIN BA ON ba1.BuletinID = BA.BuletinID
                   JOIN Analize a ON BA.AnalizeID = a.AnalizeID
                   WHERE ba1.Data BETWEEN ? AND ?"""
        cursor.execute(query, (data_inceput, data_sfarsit))
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Nume Pacient: {row[0]} {row[1]}, Analiza: {row[2]}, Data: {row[3]}, Rezultat: {row[4]}\n")

        result_text.config(state=tkinter.DISABLED)
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def execute_query_analize(conn, data_inceput, data_sfarsit, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL pentru a determina analizele cel mai frecvent efectuate
        query = """SELECT a.Nume, COUNT(*) AS NumarDeOri
                   FROM Analize a
                   JOIN BA ON a.AnalizeID = BA.AnalizeID
                   JOIN BuletinAnalize ba1 ON BA.BuletinID = ba1.BuletinID
                   WHERE ba1.Data BETWEEN ? AND ?
                   GROUP BY a.Nume
                   ORDER BY COUNT(*) DESC"""
        cursor.execute(query, (data_inceput, data_sfarsit))
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Analiza: {row[0]}, Număr de ori efectuată: {row[1]}\n")

        result_text.config(state=tkinter.DISABLED)
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close() 


def execute_query_analize_anormale(conn, result_text):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.Nume, COUNT(*) AS NumarRezultateAnormale
            FROM Analize a
            JOIN BA ON a.AnalizeID = BA.AnalizeID
            JOIN BuletinAnalize ba1 ON BA.BuletinID = ba1.BuletinID
            WHERE ba1.BuletinID IN (
                SELECT BuletinID 
                FROM BuletinAnalize
                WHERE Rezultat = 'Anormal'
            )
            GROUP BY a.Nume
            ORDER BY COUNT(*) DESC;
        """)
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Analiza: {row[0]}, Număr Rezultate Anormale: {row[1]}\n")

        result_text.config(state=tkinter.DISABLED)
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def execute_query_departament_max(conn, result_text):
    try:
        cursor = conn.cursor()
        # Interogarea SQL complexă pentru a găsi departamentele cu un număr mare de angajați
        query = """
        SELECT d.Nume, COUNT(*) AS NumarAngajati
        FROM Departament d
        JOIN Personal p ON d.DepartamentID = p.DepartamentID
        WHERE d.DepartamentID IN (
            SELECT p.DepartamentID
            FROM Personal p
            JOIN Programari pr ON p.PersonalID = pr.PersonalID
            GROUP BY p.DepartamentID
            HAVING COUNT(pr.ProgramareID) >= 2
        )
        GROUP BY d.Nume
        ORDER BY COUNT(*) DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        for row in rows:
            result_text.insert(tkinter.END, f"Departament: {row[0]}, Număr de Personal: {row[1]}\n")

        result_text.config(state=tkinter.DISABLED)
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def execute_query_most_expensive_analysis(conn, result_text):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Nume, p.Prenume, a.Nume AS Analiza, a.Pret
            FROM Pacient p
            JOIN BuletinAnalize ba1 ON p.PacientID = ba1.PacientID
            JOIN BA ON ba1.BuletinID = BA.BuletinID
            JOIN Analize a ON BA.AnalizeID = a.AnalizeID
            WHERE a.Pret = (SELECT MAX(Pret) FROM Analize);
        """)
        rows = cursor.fetchall()
        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)
        for row in rows:
            result_text.insert(tkinter.END, f"Pacient: {row[0]} {row[1]}, Analiza: {row[2]}, Preț: {row[3]}\n")
        result_text.config(state=tkinter.DISABLED)
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()


def populate_analiza_dropdown(conn, analiza_var, analiza_dropdown):
    try:
        cursor = conn.cursor()
        query = "SELECT Nume FROM Analize"
        cursor.execute(query)
        analize = cursor.fetchall()

        analiza_dropdown['menu'].delete(0, 'end')
        for analiza in analize:
            analiza_dropdown['menu'].add_command(label=analiza[0], command=lambda value=analiza[0]: analiza_var.set(value))

        if not analize:
            analiza_var.set("Nicio analiză disponibilă")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
    finally:
        cursor.close()

def open_pacient_window(conn):
    pacient_window = tkinter.Toplevel()
    pacient_window.title("Gestionare Pacienți")
    pacient_window.geometry("800x600")  # Dimensiunea ferestrei
    pacient_window.configure(bg="#333333")

    # Câmp de intrare pentru CNP
    cnp_label = tkinter.Label(pacient_window, text="Introduceți CNP-ul:", bg="#333333", fg="#FFFFFF")
    cnp_label.pack(pady=10)
    cnp_entry = tkinter.Entry(pacient_window)
    cnp_entry.pack(pady=10)

    # Buton pentru a căuta analizele pacientului
    search_button = tkinter.Button(pacient_window, text="Caută Analize", command=lambda: search_analize(conn, cnp_entry.get(), result_text), bg="#F1CB7E", fg="#000000")
    search_button.pack(pady=10)

    # Text pentru afișarea rezultatelor
    result_text = tkinter.Text(pacient_window, height=15, width=70, state=tkinter.DISABLED)
    result_text.pack(pady=10)

def search_analize(conn, cnp, result_text):
    try:
        cursor = conn.cursor()
        query = """SELECT p.Nume, p.Prenume, an.Nume, ba1.Rezultat, ba1.Data
                   FROM Pacient p
                   JOIN BuletinAnalize ba1 ON p.PacientID = ba1.PacientID
                   JOIN BA ON ba1.BuletinID = BA.BuletinID
                   JOIN Analize an ON BA.AnalizeID = an.AnalizeID
                   WHERE p.CNP = ?
                   ORDER BY p.Nume, p.Prenume, ba1.Data DESC"""
        cursor.execute(query, (cnp,))

        rows = cursor.fetchall()

        result_text.config(state=tkinter.NORMAL)
        result_text.delete("1.0", tkinter.END)

        if rows:
            # Afiseaza numele pacientului o singura data
            result_text.insert(tkinter.END, f"Pacient: {rows[0][0]} {rows[0][1]}\n")
            for row in rows:
                result_text.insert(tkinter.END, f"   Analiza: {row[2]}, Rezultat: {row[3]}, Data: {row[4]}\n")
        else:
            result_text.insert(tkinter.END, "Nu s-au găsit rezultate pentru CNP-ul dat.\n")

        result_text.config(state=tkinter.DISABLED)
        cursor.close()

    except Exception as e:
        messagebox.showerror("Eroare", str(e))


window = tkinter.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.title("Formular Logare")
window.geometry(f"{screen_width}x{screen_height}")
window.configure(bg='#333333')

frame = tkinter.Frame(bg='#333333')
frame.pack()

login_label = tkinter.Label(frame, text="Login", bg='#333333', fg="#FFFFFF", font=("Arial", 30))
login_label.grid(row=0, column=0, columnspan=2, pady=40)

username_label = tkinter.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_label.grid(row=1, column=0)
username_entry = tkinter.Entry(frame, font=("Arial", 16))
username_entry.grid(row=1, column=1)

password_label = tkinter.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_label.grid(row=2, column=0)
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
password_entry.grid(row=2, column=1)

login_button = tkinter.Button(frame, text="Login", bg="#F1CB7E", fg="#000000", command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

pacient_button = tkinter.Button(frame, text="Interfață Pacient", bg="#F1CB7E", fg="#000000", command=lambda: open_pacient_window(odbc.connect(connection_string)))
pacient_button.grid(row=4, column=0, columnspan=2, pady=10)

window.mainloop()