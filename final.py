from tkinter import *
from tkinter import ttk
import sqlite3
import re
from tkinter import messagebox
import tkinter.font as font
import os

main = Tk()
main.geometry("1080x720")
main.resizable(0,0)


dbase = sqlite3.connect('theater_data.db')
cursor = dbase.cursor()

dbase.execute("PRAGMA foreign_keys = ON;");

cursor.execute("""CREATE TABLE IF NOT EXISTS cinema_list(
    cinema_number integer PRIMARY KEY,
    cinema_name VARCHAR(25),
    cinema_seats integer
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS movie_list(
    movie_number integer PRIMARY KEY,
    movie_title VARCHAR(50),
    movie_synopsis VARCHAR(255),
    movie_maturity VARCHAR(10),
    movie_language VARCHAR(15)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS sched_list(
    sched_number integer PRIMARY KEY,
    movie_number integer,
    cinema_number integer,
    screen_time TIME,
    screen_date DATE,
    FOREIGN KEY (movie_number)
        REFERENCES movie_list(movie_number)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    FOREIGN KEY (cinema_number)
        REFERENCES cinema_list(cinema_number)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS booking_list(
    booking_number integer PRIMARY KEY,
    movie_number integer,
    cinema_number integer,
    numberOf_tickets integer,
    FOREIGN KEY (movie_number)
        REFERENCES movie_list(movie_number)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    FOREIGN KEY (movie_number)
            REFERENCES movie_list(movie_number)
                ON UPDATE CASCADE
                ON DELETE CASCADE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS genre_list(
    genre_name VARCHAR(20) PRIMARY KEY,
    genre_desc VARCHAR(50)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS movie_genre(
    genmovie_key integer PRIMARY KEY,
    movie_number integer,
    genre_name VARCHAR(20),
    FOREIGN KEY (movie_number)
        REFERENCES movie_list(movie_number)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    FOREIGN KEY (genre_name)
        REFERENCES genre_list(genre_name)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_list(
    user_number integer PRIMARY KEY,
    user_name VARCHAR(20),
    password VARCHAR(20)
    )""")

def update_list():
    global cinemaList
    cursor.execute("SELECT * FROM cinema_list")
    cinemaList = cursor.fetchall()
    global movieList
    cursor.execute("SELECT * FROM movie_list")
    movieList = cursor.fetchall()
    global genreList
    cursor.execute("SELECT * FROM genre_list")
    genreList = cursor.fetchall()
    global mgenList
    cursor.execute("SELECT * FROM movie_genre")
    mgenList = cursor.fetchall()
    global bookList
    cursor.execute("SELECT * FROM booking_list")
    bookList = cursor.fetchall()
    global schedList
    cursor.execute("SELECT * FROM sched_list")
    schedList = cursor.fetchall()
    global userList
    cursor.execute("SELECT * FROM user_list")
    userList = cursor.fetchall()

#Log In GUI
main.withdraw()
userWindow = Toplevel()
userWindow.resizable(0,0)

def check_user():
    if userName.get()=="" or password.get()=="":
        messagebox.showinfo("Theater Management System","Fill in all fields.",parent=userWindow)
        return 
    for user in userList:
        if userName.get()==user[1] and password.get()==user[2]:
            messagebox.showinfo("Theater Management System","Log-in sucessful.",parent=userWindow)
            userWindow.destroy()
            main.deiconify()
            return
    messagebox.showinfo("Theater Management System","User not found.",parent=userWindow)    

Label(userWindow,text="Username\t:",anchor=W).grid(row=0,column=0,padx=(10,0),pady=(10,0))
userName = Entry(userWindow,width=40)
userName.grid(row=0,column=1,padx=(0,10),pady=(10,0))
Label(userWindow,text="Password\t:",anchor=W).grid(row=1,column=0,padx=(10,0),pady=(10,0))
password = Entry(userWindow,width=40)
password.grid(row=1,column=1,padx=(0,10),pady=(10,0))
holder=Frame(userWindow)
holder.grid(row=2,column=0,columnspan=2)
logIn = Button(holder,text="Log In",width=20,height=2,command=check_user)
logIn.pack(pady=5)

def diverge(command,strain):
    update_list()
    mycanvas.yview_moveto(0)
    if command == 0:
        global thisEntry
        thisEntry = StringVar()
        myEntry = Entry(searchFrame, textvariable=thisEntry, width = 120)
        myEntry.grid(row=0, column=1,ipady=3)
        #Traces the changes made in the search bar
        thisEntry.trace('w',show_cinema)
        show_cinema()
    elif command == 1:
        global thoseEntry
        thoseEntry = StringVar()
        global strainer
        strainer = strain
        itEntry = Entry(searchFrame, textvariable=thoseEntry, width = 120)
        itEntry.grid(row=0, column=1,ipady=3)
        #Traces the changes made in the search bar
        thoseEntry.trace('w',show_showing)
        show_showing()
    else:
        global thatEntry
        thatEntry = StringVar()    
        theirEntry = Entry(searchFrame, textvariable=thatEntry, width = 120)
        theirEntry.grid(row=0, column=1,ipady=3)
        #Traces the changes made in the search bar
        thatEntry.trace('w',show_movies)
        show_movies()
        
def delete_cinema(cinema):
    reponse = messagebox.askyesno("Theater Management System","Delete this cinema?")
    if reponse == 0:
        return
    cursor.execute("DELETE from cinema_list WHERE cinema_number=?",(cinema[0],))
    dbase.commit()
    show_cinema()

def cinema_window(comm,cinema):
    #Function for adding or updating the info of a course
    def command():
        #Checks if an existing record already exist
        if comm == "add":
            for thiscinema in cinemaList:
                if thiscinema[1] == cname.get('1.0',"end-1c"):
                    messagebox.showinfo("Theater Management System","Record already exists.",parent=cWindow)
                    return
        if cseats.get('1.0',"end-1c").isdigit()==False:
            messagebox.showinfo("Theater Management System","Must input an integer in seats.",parent=cWindow)
            return 
        #Guarantees that the input fields are not empty
        if cname.get("1.0",END)=="\n" or cseats.get("1.0",END)=="\n":
            messagebox.showinfo("Theater Management System","Fill in all the fields.",parent=cWindow)
        else:
            if comm == "edit":
                cursor.execute("UPDATE cinema_list SET cinema_seats=? WHERE cinema_number=?",
                               (int(cseats.get('1.0',"end-1c")),cinema[0]))
            else:
                cursor.execute("INSERT INTO cinema_list(cinema_name,cinema_seats)VALUES(?,?)",
                                   (cname.get('1.0',"end-1c"),int(cseats.get('1.0',"end-1c"))))
            dbase.commit()
            cWindow.destroy()
            show_cinema()
        
    cWindow = Toplevel()
    cWindow.geometry("500x155")
    cWindow.resizable(0,0)
    #cWindow.geometry("+{}+{}".format(positionRight-250, positionDown-85))
    
    this = LabelFrame(cWindow,text="Add Cinema Details" if comm=="add" else "Edit Cinema Details",font='Helvitica 12 bold')
    this.pack(padx=5,pady=5,fill='both',expand='yes')

    Label(this,text="Cinema Name\t:").grid(row=0,column=0,padx=5,pady=(10,5))
    Label(this,text="Cinema # of Seats\t:").grid(row=1,column=0,padx=5,pady=5)
    cname = Text(this, width=44,height=1)
    cname.grid(row=0,column=1,padx=5,pady=(10,5))
    cseats = Text(this, width=44, height=1)
    cseats.grid(row=1,column=1,padx=5,pady=5)

    if comm == "edit":
        cname.insert(END,cinema[1])
        cname.config(state=DISABLED)
        cseats.insert(END,cinema[2])
        
    buttonFrame = Frame(this)
    buttonFrame.grid(row=2,column=0,columnspan=2)
    commandButton = Button(buttonFrame,text="ADD CINEMA" if comm=="add" else "EDIT CINEMA",height=2,width=30,command=command)
    commandButton.pack(side=LEFT,padx=5,pady=5)
    cancelButton = Button(buttonFrame,text="CANCEL",height=2,width=30)
    cancelButton.pack(side=RIGHT,padx=5,pady=5)

def show_cinema(*args):
    update_list()
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thisEntry.get()
        
    this.config(text="LIST OF CINEMAS")
    addButton.config(text="Add Cinema", command=lambda:cinema_window("add",[]))
    
    row,column=0,0
    #Loops through the list of courses
    for cinema in cinemaList:
        #Only displays course with names containing the search string
        if searchword.lower() in cinema[1].lower():
            if column==2:
                row += 1
                column = 0
            currFrame=Frame(listFrame, highlightbackground="black", highlightthickness=1,height=135, width=505)
            currFrame.grid(row=row,column=column,padx=(15,0),pady=(15,0))
            currFrame.grid_propagate(0)
            Label(currFrame,text=cinema[1],font='Helvitica 30 bold').grid(row=0,column=0,columnspan=3,pady=(15,0),sticky=W+E)
            viewButton = Button(currFrame,text="View Showing Movies",width=21,height=2, command=lambda x=cinema[0]:diverge(1,x))
            viewButton.grid(row=1,column=0,padx=(7,0),pady=(15,0))
            editButton = Button(currFrame,text="Edit Cinema",width=21,height=2,command=lambda x=cinema:cinema_window("edit",x))
            editButton.grid(row=1,column=1,padx=(7,0),pady=(15,0))
            deleteButton = Button(currFrame,text="Delete Cinema",width=21,height=2,command=lambda x=cinema:delete_cinema(x))
            deleteButton.grid(row=1,column=2,padx=(7,0),pady=(15,0))
            column += 1
    fixFrame = Frame(listFrame, height=2000, width=470)
    fixFrame.grid(row=row+1,column=0,columnspan=3)
    fixFrame.grid_propagate(0)

def command_genre(com,thisgenre):
    genWindow = Toplevel()
    genWindow.geometry("300x180")
    genWindow.resizable(0,0)

    def commGenre():
        if com == "add":
            cursor.execute("INSERT INTO genre_list(genre_name,genre_desc)VALUES(?,?)",
                           (genTitle.get(),genDesc.get("1.0",END)))
        else:
            cursor.execute("UPDATE genre_list SET genre_desc=? WHERE genre_name=?",
                           (genDesc.get("1.0",END),thisgenre[0]))
        dbase.commit()
        update_list()
        genWindow.destroy()
        #show_genre()
        
    commFrame = LabelFrame(genWindow,text="Genre Details",font='Helvitica 12 bold')
    commFrame.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(commFrame,text="Genre Name\t:",anchor=W).grid(row=0,column=0,padx=5,pady=5)
    genTitle = Entry(commFrame,width=26)
    genTitle.grid(row=0,column=1,padx=5,pady=5)
    Label(commFrame,text="Description\t:",anchor=W).grid(row=1,column=0,padx=5,pady=5)
    genDesc = Text(commFrame,width=19,height=3)
    genDesc.grid(row=1,column=1,padx=5,pady=5)
    botFrame = Frame(commFrame)
    botFrame.grid(row=2,column=0,columnspan=2)
    saveGenre = Button(botFrame,text="Save",width=17,height=2,command=commGenre)
    saveGenre.pack(side=RIGHT,padx=5,pady=5)
    cancelGenre = Button(botFrame,text="Cancel",width=17,height=2)
    cancelGenre.pack(side=LEFT,padx=5,pady=5)

def attach_genre(movie,genre,comman):
    if comman == "add":
        cursor.execute("INSERT INTO movie_genre(movie_number,genre_name)VALUES(?,?)",
                       (movie[0],genre[0]))
    else:
        cursor.execute("DELETE from movie_genre WHERE (movie_number =? AND genre_name = ?)",
                       (movie[0],genre[0]))
    dbase.commit()
    gWindow.destroy()
    genre_window(movie)
    
def show_genre(movie):
    for frame in thisFrame.winfo_children():
        frame.destroy()

    
    row,column=0,0
    for genre in genreList:
        if column==2:
            row += 1
            column = 0
        tFrame = Frame(thisFrame,highlightbackground="black", highlightthickness=1,height=100, width=165)
        tFrame.grid(row=row,column=column,padx=5,pady=5)
        tFrame.propagate(0)
        Label(tFrame,text=genre[0],font='Helvitica 12 bold').pack(side=TOP,pady=3)
        buttons = Frame(tFrame)
        buttons.pack(side=TOP)
        addTo = Button(buttons,text="Add",width=9,command=lambda x=genre:attach_genre(movie,x,"add"))
        addTo.grid(row=0,column=0,padx=2,pady=(2,0))
        remove = Button(buttons,text="Remove",width=9,command=lambda x=genre:attach_genre(movie,x,"remove"))
        remove.grid(row=0,column=1,padx=2,pady=(2,0))
        detail = Button(buttons,text="View Details",width=20)
        detail.grid(row=1,column=0,columnspan=2,padx=2,pady=(4,0))
        column += 1
    fFrame = Frame(thisFrame, height=1000, width=100)
    fFrame.grid(row=row+1,column=0,columnspan=2)
    fFrame.grid_propagate(0)
    
def genre_window(movie):
    def refresh():
        gWindow.destroy()
        mWindow.destroy()
        movie_window("edit",movie)
    def fill_up():
        if movie!=[]:
            cursor.execute("SELECT genre_name FROM movie_genre WHERE movie_number=? ",
                           (movie[0],))
            movieGen=[x[0] for x in cursor.fetchall()]
            for gen in movieGen:
                allGenre.insert(END,gen+",")
            
    global gWindow
    gWindow = Toplevel()
    gWindow.geometry("400x500")
    gWindow.resizable(0,0)
    
    genreFrame = LabelFrame(gWindow,text="Pick Genre",font='Helvitica 12 bold')
    genreFrame.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(genreFrame,text="Movie's genre\t:",anchor=W).grid(row=0,column=0,padx=(5,0),pady=5)
    allGenre = Entry(genreFrame,width=43)
    allGenre.grid(row=0,column=1,padx=5,pady=5)
    fill_up()
    
    wrapper = LabelFrame(genreFrame)
    wrapper.grid(row=1, column=0,columnspan=2,padx=5)
    mycanvas = Canvas(wrapper, width=350,height=330)
    global thisFrame
    thisFrame= Frame(mycanvas)
    yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
    yscrollbar.pack(side=RIGHT, fill="y")
    mycanvas.pack(side=LEFT)
    mycanvas.configure(yscrollcommand=yscrollbar.set)
    mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    mycanvas.create_window((0,0), window=thisFrame, anchor="nw")

    addGenre = Button(genreFrame,text="Add New Genre",width=52,height=2, command=lambda:command_genre("add",[]))
    addGenre.grid(row=2,column=0,columnspan=2,padx=5,pady=(5,0))
    saveGenre = Button(genreFrame,text="Attach Genre to Movie",width=52,height=2,command=refresh)
    saveGenre.grid(row=3,column=0,columnspan=2,padx=5,pady=(5,0))
    show_genre(movie)
    
def movie_window(comm,movie):
    update_list()
    global mWindow
    mWindow = Toplevel()
    mWindow.geometry("600x330")
    mWindow.resizable(0,0)

    def command():
        if movieTitle.get()=="" or maturity.get()=="" or language.get()=="" or movieGenre.get("1.0",END)=="" or movieSynopsis.get("1.0",END)=="":
            messagebox.showinfo("Theater Management System","Failed to input all fields.",parent=mWindow)
        else:
            if comm == "edit":
                cursor.execute("UPDATE movie_list SET movie_title=?, movie_synopsis=?, movie_maturity=?, movie_language=? WHERE movie_number=?",
                               (movieTitle.get(),movieSynopsis.get("1.0",END),maturity.get(),language.get(),movie[0]))
            else:
                cursor.execute("INSERT INTO movie_list(movie_title,movie_synopsis,movie_maturity,movie_language)VALUES(?,?,?,?)",
                               (movieTitle.get(),movieSynopsis.get("1.0",END),maturity.get(),language.get()))
            dbase.commit()
            mWindow.destroy()
            show_movies()

    def delete_movie():
        reponse = messagebox.askyesno("Theater Management System","Delete this movie?")
        if reponse == 0:
            return
        cursor.execute("DELETE from movie_list WHERE movie_number=?",(movie[0],))
        dbase.commit()
        show_movies()
    
    that = LabelFrame(mWindow,text="Add Movie Details" if comm=="add" else "Edit Movie Details",font='Helvitica 12 bold')
    that.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(that,text="Title\t:",anchor=W).grid(row=1,column=0,padx=5,pady=5,sticky=W)
    movieTitle = Entry(that,width=83)
    movieTitle.grid(row=1,column=1,columnspan=5,padx=5,pady=5)
    Label(that,text="Maturity\t:",anchor=W).grid(row=2,column=0,padx=5,pady=5,sticky=W)
    maturity = Entry(that,width=23)
    maturity.grid(row=2,column=1,padx=5,pady=5)
    Label(that,text="Language\t:",anchor=W).grid(row=2,column=2,padx=5,pady=5,sticky=W)
    language = Entry(that,width=38)
    language.grid(row=2,column=3,columnspan=3,padx=5,pady=5)
    Label(that,text="Genre\t:",anchor=W).grid(row=3,column=0,padx=5,pady=5,sticky=W)
    movieGenre = Text(that,width=42,height=2)
    movieGenre.grid(row=3,column=1,rowspan=2,columnspan=3,padx=5,pady=5)
    pick = Button(that,text="Pick Genre",width=21,height=2, command=lambda:genre_window(movie))
    pick.grid(row=3,column=4,rowspan=2,columnspan=2,padx=5,pady=5)
    Label(that,text="Synopsis\t:",anchor=W).grid(row=5,column=0,padx=5,pady=5,sticky=W)
    movieSynopsis=Text(that,width=63,height=7)
    movieSynopsis.grid(row=5,column=1,rowspan=7,columnspan=5,padx=5,pady=5)
    buttFrame=Frame(that)
    buttFrame.grid(row=12,column=0,columnspan=6)
    commMovie = Button(buttFrame,text="Add" if comm=="add" else "Edit",width=38,height=2, command=command)
    commMovie.grid(row=0,column=1,padx=5,pady=5)
    cancel = Button(buttFrame,text="Cancel" if comm=="add" else "Delete",width=38,height=2,command=mWindow.destroy)
    cancel.grid(row=0,column=0,padx=5,pady=5)

    if comm == "edit":
        movieTitle.insert(0,movie[1])
        maturity.insert(0,movie[3])
        language.insert(0,movie[4])
        allGenre=""
        for xgenre in mgenList:
            if xgenre[1] == movie[0]:
                allGenre+=xgenre[2]+","
        movieGenre.insert(END,allGenre[:-1])
        movieSynopsis.insert(END,movie[2])
        cancel.config(command=lambda:delete_movie())
    movieGenre.config(state=DISABLED)
    
def show_movies(*args):
    update_list()
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thatEntry.get()

    this.config(text="LIST OF ALL MOVIES")
    addButton.config(text="Add Movie", command=lambda:movie_window("add",[]))

    row, column = 0,0
    for movie in movieList:
        if movie[1].lower().startswith(searchword.lower()):
            if column == 5:
                row += 1
                column = 0
            movie_Frame = Frame(listFrame, highlightbackground="black", highlightthickness=1, height=215, width=200)
            movie_Frame.propagate(0)
            movie_Frame.grid(row=row, column=column, padx=5, pady=(13,0))
            picFrame = Frame(movie_Frame, highlightbackground="black", highlightthickness=1, height=90, width=70)
            picFrame.propagate(0)
            picFrame.pack(pady = 10)
            movie_title = Text(movie_Frame, height=2)
            movie_title.pack(padx=30,pady=10)
            movie_title.insert(END, movie[1])
            movie_title.config(state=DISABLED)
            movie_title.tag_configure("center", justify='center')
            movie_title.tag_add("center", 1.0, "end")
            view_details = Button(movie_Frame, text="View Details", height=2, width=18, command=lambda x=movie:movie_window("edit",x))
            view_details.pack(side=BOTTOM, pady=10)
            column += 1

def schedule_window(comm,sched,strainer):
    update_list()
    global sWindow
    sWindow = Toplevel()
    sWindow.geometry("600x150")
    sWindow.resizable(0,0)

    def sCommand():
        if cDrop.get()=="" or screenDate.get()=="" or screenTime.get()=="" or mDrop.get()=="":
            messagebox.showinfo("Theater Management System","Failed to input all fields.",parent=sWindow)
        else:
            if len(screenDate.get().split("/")) != 3:
                messagebox.showinfo("Theater Management System","Invalid date format (MM/DD/YYYY).",parent=sWindow)
                return
            if len(screenDate.get().split("/")[0])!=2 or len(screenDate.get().split("/")[1])!=2 or len(screenDate.get().split("/")[2])!=4:
                messagebox.showinfo("Theater Management System","Invalid date format (MM/DD/YYYY).",parent=sWindow)
                return
            if screenDate.get().split("/")[0].isdigit()==False or screenDate.get().split("/")[1].isdigit()==False or screenDate.get().split("/")[2].isdigit()==False:
                messagebox.showinfo("Theater Management System","Invalid date format (MM/DD/YYYY).",parent=sWindow)
                return
            if len(screenTime.get().split("-")) != 2:
                messagebox.showinfo("Theater Management System","Invalid time format (HH:MM-HH:MM).",parent=sWindow)
                return
            if len(screenTime.get().split("-")[0]) != 5 or len(screenTime.get().split("-")[1]) != 5:
                messagebox.showinfo("Theater Management System","Invalid time format (HH:MM-HH:MM).",parent=sWindow)
                return
            if len(screenTime.get().split("-")[0].split(":")[0]) != 2 or len(screenTime.get().split("-")[0].split(":")[1]) != 2 or len(screenTime.get().split("-")[1].split(":")[0]) != 2 or len(screenTime.get().split("-")[1].split(":")[1]) != 2:
                messagebox.showinfo("Theater Management System","Invalid time format (HH:MM-HH:MM).",parent=sWindow)
                return
            if screenTime.get().split("-")[0].split(":")[0].isdigit()==False or screenTime.get().split("-")[0].split(":")[1].isdigit()==False or screenTime.get().split("-")[1].split(":")[0].isdigit()==False or screenTime.get().split("-")[1].split(":")[1].isdigit()==False:
                messagebox.showinfo("Theater Management System","Invalid time format (HH:MM-HH:MM).",parent=sWindow)
                return

            for sched in schedList:
                if cDrop.get()==sched[2] and screenDate.get()==sched[4] and screenTime.get()==sched[3] and mDrop.get()==sched[1]:
                    messagebox.showinfo("Theater Management System","Record already exists.",parent=sWindow)
                    return
            for movie in movieList:
                if mDrop.get() == movie[1]:
                    mNumber = movie[0]
            for cinema in cinemaList:
                if cDrop.get() == cinema[1]:
                    cNumber = cinema[0]
            if comm == "edit":
                cursor.execute("UPDATE sched_list SET movie_number=?, cinema_number=?, screen_time=?, screen_date=? WHERE sched_number=?",
                               (mNumber,cNumber,screenTime.get(),screenDate.get(),sched[0]))
            else:
                cursor.execute("INSERT INTO sched_list(movie_number,cinema_number,screen_time,screen_date)VALUES(?,?,?,?)",
                               (mNumber,cNumber,screenTime.get(),screenDate.get()))
            dbase.commit()
            sWindow.destroy()
            show_showing()

    those = LabelFrame(sWindow,text="Schedule Details",font='Helvitica 12 bold')
    those.pack(padx=5,pady=5,fill='both',expand='yes')
    Label(those, text="Movie\t:", anchor=W).grid(row=0,column=0,padx=5,pady=5,sticky=W)
    mDrop = ttk.Combobox(those,state='readonly',width=80)
    mDrop['values'] = [title[1] for title in movieList]
    mDrop.grid(row=0,column=1,padx=5,pady=5)
    tempFrame = Frame(those)
    tempFrame.grid(row=1,column=0,columnspan=2)
    Label(tempFrame, text="Cinema\t:", anchor=W).grid(row=0,column=0,padx=5,pady=5,sticky=W)
    cDrop = ttk.Combobox(tempFrame,state='readonly',width=29)
    cDrop['values'] = [name[1] for name in cinemaList]
    cDrop.grid(row=0,column=1,padx=5,pady=5)
    Label(tempFrame, text="Date\t:", anchor=W).grid(row=0,column=2,padx=5,pady=5,sticky=W)
    screenDate = Entry(tempFrame,width=12)
    screenDate.grid(row=0,column=3,padx=5,pady=5)
    Label(tempFrame, text="Time\t:", anchor=W).grid(row=0,column=4,padx=5,pady=5,sticky=W)
    screenTime = Entry(tempFrame,width=12)
    screenTime.grid(row=0,column=5,padx=5,pady=5)
    tempFrame1 = Frame(those)
    tempFrame1.grid(row=2,column=0,columnspan=2)
    sCancel = Button(tempFrame1,text="Cancel",width=30,height=2,command=sWindow.destroy)
    sCancel.pack(side=LEFT,padx=5,pady=5)
    sSave = Button(tempFrame1,text="Save",width=30,height=2,command=sCommand)
    sSave.pack(side=RIGHT,padx=5,pady=5)

    if comm == "edit":
        mDrop.set(sched[1])
        cDrop.set(sched[2])
        screenDate.insert(END,sched[4])
        screenTime.insert(END,sched[3])
def delete_sched(sched):
    reponse = messagebox.askyesno("Theater Management System","Delete this schedule?")
    if reponse == 0:
        return
    cursor.execute("DELETE from sched_list WHERE sched_number=?",(sched[0],))
    dbase.commit()
    show_showing()
def show_showing(*args):
    update_list()
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thoseEntry.get()

    for cinema in cinemaList:
        if strainer == cinema[0]:
            showTitle = cinema[1]
    this.config(text="SHOWING | ALL CINEMAS" if strainer=="" else "SHOWING | " + showTitle)
    addButton.config(text="Add Schedule", command=lambda:schedule_window("add",[],strainer))

    if strainer != "":
        cursor.execute("""SELECT sched_list.sched_number,movie_list.movie_title,cinema_list.cinema_name,sched_list.screen_time,sched_list.screen_date FROM sched_list
                       INNER JOIN movie_list ON sched_list.movie_number=movie_list.movie_number INNER JOIN cinema_list ON sched_list.cinema_number=cinema_list.cinema_number
                       WHERE sched_list.cinema_number=?""",(strainer,))
    else:
        cursor.execute("""SELECT sched_list.sched_number,movie_list.movie_title,cinema_list.cinema_name,sched_list.screen_time,sched_list.screen_date FROM sched_list
                       INNER JOIN movie_list ON sched_list.movie_number=movie_list.movie_number INNER JOIN cinema_list ON sched_list.cinema_number=cinema_list.cinema_number""")
    filtered = cursor.fetchall()

    
    row=0
    for movie in filtered:
        if movie[1].lower().startswith(searchword.lower()):
            movie_Frame = Frame(listFrame, highlightbackground="black", highlightthickness=1, height=80, width=1040)
            movie_Frame.propagate(0)
            movie_Frame.grid(row=row, column=0, padx=5, pady=(11,0))
            temp1 = Frame(movie_Frame)
            temp1.pack(side=LEFT)
            Label(temp1, text=movie[2]+"\t|\t"+movie[4]+"\t|\t"+movie[3]).grid(row=0,column=0,padx=5,pady=2)
            Label(temp1, text=movie[1],font = 'Helvitica 27 bold').grid(row=1,column=0,padx=5,pady=2,sticky=W)
            temp2 = Frame(movie_Frame)
            temp2.pack(side=RIGHT)
            viewBooking = Button(temp2,text="View Booking List",width=20,height=2, command=lambda x=movie:show_booking(x))
            viewBooking.grid(row=0,column=0,padx=5,pady=2)
            for x in movieList:
                if movie[1]==x[1]:
                    y = movie
            viewMovie = Button(temp2,text="View Movie Details",width=20,height=2,command=lambda x=y:movie_window("edit",x))
            viewMovie.grid(row=0,column=1,padx=5,pady=2)
            editMovie = Button(temp2,text="Update Schedule",width=20,height=2,command=lambda x=movie:schedule_window("edit",x,""))
            editMovie.grid(row=1,column=0,padx=5,pady=2)
            deleteMovie = Button(temp2,text="Delete Schedule",width=20,height=2,command=lambda x=movie:delete_sched(x))
            deleteMovie.grid(row=1,column=1,padx=5,pady=2)
            row += 1  

def show_booking(schedule):
    def add_record():
        cursor.execute("INSERT INTO booking_list(movie_number,cinema_number,numberOf_tickets)VALUES(?,?,?)",
                       (mBook,cBook,seats.get()))
        commit_refresh()
    def edit_record():
        cursor.execute("UPDATE booking_list SET numberOf_tickets=? WHERE booking_number=?",
                       (seats.get(),tree.item(tree.focus())['values'][0]))
        commit_refresh()
    def delete_record():
        cursor.execute("DELETE from booking_list WHERE booking_number=?",(tree.item(tree.focus())['values'][0],))
        commit_refresh()
    def clicked(*args):
        if tree.item(tree.focus())['values'] != "":
            editButton['state'] = NORMAL
            deleteButton['state'] = NORMAL
            addButton['state'] = DISABLED
            seats.delete(0,'end')
            seats.insert(0,tree.item(tree.focus())['values'][1])
    def cancel():
        seats.delete(0,'end')
        bookWindow.destroy()
        show_booking(schedule)
    def commit_refresh():
        dbase.commit()
        bookWindow.destroy()
        show_booking(schedule)
        
    update_list()
    bookWindow = Toplevel()
    bookWindow.geometry("450x690")
    bookWindow.resizable(0,0)

    description = Frame(bookWindow,highlightbackground="black", highlightthickness=1, height=100, width=430)
    description.propagate(0)
    description.pack(padx=5,pady=5)
    
    for movie in movieList:
        if movie[1]==schedule[1]:
            global mBook
            mBook=movie[0]
    for cinema in cinemaList:
        if cinema[1]==schedule[2]:
            global cBook
            cBook=cinema[0]
            cSeats=cinema[2]
    records = []
    for book in bookList:
        if book[1]==mBook and book[2]==cBook:
            records.append(book)
    total = 0
    for x in records:
        total += x[3]
    cSeats -= total
    
    title = Text(description,height=1,width=29,font='Helvitica 18 bold')
    title.insert(END, schedule[1])
    title.config(state=DISABLED)
    title.place(relx=.05, rely=.15)
    Label(description, text=schedule[2]+"   |   "+schedule[3]+"   |   "+str(schedule[4])+"   |   "+str(cSeats)+" free seats", font='Helvitica 10',anchor=W).place(relx=.05, rely=.55)

    tree = ttk.Treeview(bookWindow,height=23)
    tree.pack(padx=5,pady=5)
    tree['columns'] = ["order","seats"]

    tree.column('#0',width=0, stretch=NO)
    tree.column("order", anchor=CENTER, width=225)
    tree.column("seats", anchor=CENTER, width=200)
    tree.heading("order", text="Order Number", anchor=CENTER)
    tree.heading("seats", text="Number of Tickets", anchor=CENTER)

    tree['displaycolumns'] = ("order","seats")

    for i in tree.get_children():
        tree.delete(i)
        
    counter=0
    for record in records:
        tree.insert(parent='',  index='end', iid=counter, values=(record[0],record[3]))
        counter += 1

    footer = Frame(bookWindow,highlightbackground="black", highlightthickness=1)
    footer.pack(padx=5,pady=5)
    Label(footer,text="Number of Seats\t:").grid(row=0,column=0,padx=5,pady=5)
    seats = Entry(footer,width=50)
    seats.grid(row=0,column=1,padx=5,pady=5)
    
    buttons = Frame(footer)
    buttons.grid(row=2,column=0,columnspan=4,padx=5,pady=5)
    addButton = Button(buttons,text="Add Record", state=NORMAL, width=12, command=add_record)
    addButton.pack(side=LEFT,padx=(10,0))
    editButton = Button(buttons,text="Edit Record", state=DISABLED, width=12, command=edit_record)
    editButton.pack(side=LEFT,padx=(10,0))
    deleteButton = Button(buttons,text="Delete Record", state=DISABLED, width=12, command=delete_record)
    deleteButton.pack(side=LEFT,padx=(10,0))
    cancel = Button(buttons,text="Cancel", width=12, command=cancel)
    cancel.pack(side=LEFT,padx=(10,0))

    tree.bind("<ButtonRelease-1>", clicked)

def show_user():
    update_list()
    uWindow = Toplevel()
    uWindow.resizable(0,0)

    def add_record():
        cursor.execute("INSERT INTO user_list (user_name,password)VALUES(?,?)",
                       (uName.get(),uPass.get()))
        commit_refresh()
    def edit_record():
        cursor.execute("UPDATE user_list SET user_name=?, password=? WHERE user_number=?",
                       (uName.get(),uPass.get(),ttree.item(ttree.focus())['values'][0]))
        commit_refresh()
    def delete_record():
        cursor.execute("DELETE from user_list WHERE user_number=?",(ttree.item(ttree.focus())['values'][0],))
        commit_refresh()

    def clicked(*args):
        if ttree.item(ttree.focus())['values'] != "":
            editButton['state'] = NORMAL
            deleteButton['state'] = NORMAL
            addButton['state'] = DISABLED
            uName.delete(0,'end')
            uPass.delete(0,'end')
            uName.insert(0,ttree.item(ttree.focus())['values'][1])
            uPass.insert(0,ttree.item(ttree.focus())['values'][2])

    def cancel():
        uName.delete(0,'end')
        uPass.delete(0,'end')
        uWindow.destroy()
        show_user()
    def commit_refresh():
        dbase.commit()
        uWindow.destroy()
        show_user()
        
    box = LabelFrame(uWindow,text="User List",font='Helvitica 12 bold')
    box.pack(padx=5,pady=5,fill='both',expand='yes')
    ttree = ttk.Treeview(box,height=23)
    ttree.pack(padx=5,pady=5)
    ttree['columns'] = ["userid","username","password"]

    ttree.column('#0',width=0, stretch=NO)
    ttree.column("userid",width=0, stretch=NO)
    ttree.column("username", anchor=W, width=200)
    ttree.column("password", anchor=W, width=200)
    ttree.heading("username", text="Username", anchor=CENTER)
    ttree.heading("password", text="Password", anchor=CENTER)

    ttree['displaycolumns'] = ("username","password")

    for i in ttree.get_children():
        ttree.delete(i)
        
    counter=0
    for user in userList:
        ttree.insert(parent='', index='end', iid=counter, values=(user[0],user[1],user[2]))
        counter += 1
        
    footer = Frame(box,highlightbackground="black", highlightthickness=1)
    footer.pack(padx=5,pady=5)
    Label(footer,text="Username\t:").grid(row=0,column=0,padx=5,pady=5)
    Label(footer,text="Password\t:").grid(row=1,column=0,padx=5,pady=5)
    uName = Entry(footer,width=46)
    uName.grid(row=0,column=1,padx=5,pady=5)
    uPass = Entry(footer,width=46)
    uPass.grid(row=1,column=1,padx=5,pady=5)
    buttons = Frame(footer)
    buttons.grid(row=2,column=0,columnspan=4,padx=5,pady=5)
    addButton = Button(buttons,text="Add Record", state=NORMAL, width=11, command=add_record)
    addButton.pack(side=LEFT,padx=5)
    editButton = Button(buttons,text="Edit Record", state=DISABLED, width=11, command=edit_record)
    editButton.pack(side=LEFT,padx=5)
    deleteButton = Button(buttons,text="Delete Record", state=DISABLED, width=11, command=delete_record)
    deleteButton.pack(side=LEFT,padx=5)
    cancel = Button(buttons,text="Cancel", width=11, command=cancel)
    cancel.pack(side=LEFT,padx=5)

    ttree.bind("<ButtonRelease-1>", clicked)
    
header = Frame(main, height=100, width=1080, highlightbackground="black", highlightthickness=1)
header.propagate(0)
header.grid(row=0,column=0)
Label(header, text="THEATER MANAGEMENT SYSTEM", font = 'Helvitica 32 bold').place(relx=.5, rely=.35, anchor='c')
Label(header, text="-- Layawa, Madidis, Maisog --", font = 'Helvitica 14 italic').place(relx=.5, rely=.70, anchor='c')

midFrame = Frame(main,height=50, width=1080, highlightbackground="black", highlightthickness=1)
midFrame.propagate(0)
midFrame.grid(row=1,column=0,pady=1)
this = Label(midFrame, text="LIST OF CINEMAS", font = 'Helvitica 25 bold', anchor=CENTER)
this.grid(row=0,column=0,sticky=W+E)
searchFrame = Frame(midFrame)
searchFrame.grid(row=1,column=0,pady=10)
Label(searchFrame, text="SEARCH:", anchor=W, font = 'Arial 10').grid(row=0, column=0)
addButton = Button(searchFrame,text="Add Cinema",width=37)
addButton.grid(row=0,column=2,padx=8)

wrapper = LabelFrame(main)
wrapper.grid(row=2, column=0)
mycanvas = Canvas(wrapper, width=1052,height=465)
listFrame= Frame(mycanvas)
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=listFrame, anchor="nw")
    
lowFrame = Frame(main)
lowFrame.grid(row=3,column=0)
cinemaButton = Button(lowFrame, text="CINEMAS", width=35, height=2,command=lambda:diverge(0,""))
cinemaButton.pack(side=LEFT, padx=5,pady=5)
showingButton = Button(lowFrame, text="SHOWING", width=35, height=2,command=lambda:diverge(1,""))
showingButton.pack(side=LEFT, padx=5,pady=5,)
userButton = Button(lowFrame, text="USERS", width=35, height=2,command=show_user)
userButton.pack(side=RIGHT, padx=5,pady=5)
movieButton = Button(lowFrame, text="MOVIES", width=35, height=2,command=lambda:diverge(2,""))
movieButton.pack(side=RIGHT, padx=5,pady=5)

diverge(0,"")
main.mainloop() 
