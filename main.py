from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
from sorter import get_sort, see_sort
from utils import levnearest
import sys
import os

version = 1.0



def recommender(villagers, sorted):
    top = 10
    myvils = []
    myvilnames = []
    imagestop = [None]*10

    root = Tk()
    root.title("NMT Decision Helper")
    total_size = root.winfo_screenwidth() * 0.8 # margin
    side = int(total_size/top)
    var = IntVar()
    def on_exit():
        var.set(1) # prevents stuck on wait
        root.destroy()
        sys.exit()
    root.protocol('WM_DELETE_WINDOW', on_exit)

    frm1 = ttk.Frame(root, padding=10)
    frm1.grid()
    ttk.Label(frm1, text="It is recommended to first add your existing villagers for better accuracy").grid(column=0, row=0)

    frm2 = ttk.Frame(root, padding=10)
    frm2.grid()
    inputbox1 = Entry(frm2)
    inputbox1.grid(column=0, row=0)
    ttk.Button(frm2, text="Add Villager", command=lambda: var.set(1)).grid(column=1, row=0)

    frm3 = ttk.Frame(root, padding=10)
    frm3.grid()
    ttk.Label(frm3, text="After setting your villagers, use the boxes bellow to set how many NMTs you can spend and who is on the current island.").grid(column=0, row=0)
    ttk.Label(frm3, text="Pressing 'Calculate' will give you a suggestion on wether to accept the current villager and an estimate about future encounters.").grid(column=0, row=1)

    frm4 = ttk.Frame(root, padding=10)
    frm4.grid()
    ttk.Label(frm4, text="Tickets left").grid(column=0, row=0)
    inputbox_tickets = Entry(frm4)
    inputbox_tickets.grid(column=0, row=1)
    ttk.Label(frm4, text="Current Villager").grid(column=1, row=0)
    inputbox_vil = Entry(frm4)
    inputbox_vil.grid(column=1, row=1)
    ttk.Button(frm4, text="Calculate", command=lambda: var.set(2)).grid(column=2, row=1)

    frm5 = ttk.Frame(root, padding=10)
    frm5.grid()
    ttk.Button(frm5, text="Return", command=lambda: var.set(3)).grid(column=0, row=0)

    root.update()

    while True:

        root.wait_variable(var)
        res = var.get()
        if res == 1:
            input = inputbox1.get()
            inputbox1.delete(0, 'end')
            print("Request add villager",input)
            vilname = levnearest(input, list(villagers))
            print("Found similar", vilname)
            if (not (vilname in myvilnames)) and (len(myvils) < 10):
                pos = len(myvils)
                myvils += [villagers[vilname]]
                myvilnames += [vilname]
                villager = villagers[vilname]
                ttk.Label(frm2, text=villager["Name"]).grid(column=pos, row=1)
                imagestop[pos] = Image.open("images/"+villager["Poster"])
                imagestop[pos] = imagestop[pos].resize((side, side), Image.ANTIALIAS)
                imagestop[pos] = ImageTk.PhotoImage(imagestop[pos])
                ttk.Label(frm2, image=imagestop[pos]).grid(column=pos, row=2)
                ttk.Label(frm2, text=villager["Personality"]).grid(column=pos, row=3)
                root.update()
        elif res == 2:
            frm5.destroy()
            frm5 = ttk.Frame(root, padding=10)
            frm5.grid()
            nmts = eval(inputbox_tickets.get())
            vilname = levnearest(inputbox_vil.get(), list(villagers))
            villager = villagers[vilname]
            position = 1 - (sorted.index(vilname)/len(sorted))
            sorted_acc = []
            for v in sorted:
                if not (v in myvilnames):
                    sorted_acc += [v]
            realposition = 1 - (sorted_acc.index(vilname)/len(sorted_acc))
            #embed()
            #print("position", position)
            #print("realposition", realposition)
            prob = 1 - (realposition ** nmts)
            ttk.Label(frm5, text=villager["Name"]).grid(column=0, row=0)
            img = Image.open("images/"+villager["Poster"])
            img = img.resize((side, side), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            ttk.Label(frm5, image=img).grid(column=0, row=1)
            ttk.Label(frm5, text="Personality: "+villager["Personality"]+"     Catchphrase: "+'"'+villager["Catchphrase"]+'"').grid(column=0, row=2)
            ttk.Label(frm5, text=villager["Name"]+" is preferable to "+str(int(position*100))+"% of villagers").grid(column=0, row=3)
            ttk.Label(frm5, text="The probability of finding a better villager in "+str(nmts)+" attempts is "+str(int(prob*100))+"%").grid(column=0, row=4)
            if (prob < 0.5):
                if villager["Gender"] == "Female":
                    ttk.Label(frm5, text="For this reason it is recommendable to invite her.").grid(column=0, row=5)
                else:
                    ttk.Label(frm5, text="For this reason it is recommendable to invite him.").grid(column=0, row=5)
            else:
                if villager["Gender"] == "Female":
                    ttk.Label(frm5, text="For this reason it is recommendable to skip her.").grid(column=0, row=5)
                else:
                    ttk.Label(frm5, text="For this reason it is recommendable to skip him.").grid(column=0, row=5)

            ttk.Button(frm5, text="Return", command=lambda: var.set(3)).grid(column=0, row=6)
            root.update()
        elif res == 3:
            root.destroy()
            return




def main(villagers):

    while True:

        root = Tk()
        root.title('Villager Recommender v'+str(version))
        frm = ttk.Frame(root, padding=10)
        var = IntVar()
        def on_exit():
            var.set(1) # prevents stuck on wait
            root.destroy()
            sys.exit()
        root.protocol('WM_DELETE_WINDOW', on_exit)

        frm.grid()

        ttk.Label(frm, text="Welcome to Villager Recommender").grid(column=0, row=0)
        ttk.Label(frm, text="To start you need to rank your villagers.").grid(column=0, row=1)
        try:
            f = open("ranked.txt", "r", encoding='ISO-8859-1')
            sorted = eval(f.read())
            f.close()
            ttk.Label(frm, text="Previous rank file found. Making a new rank file will override this.").grid(column=0, row=2)
            ttk.Button(frm, text="See Rank", command=lambda: var.set(2)).grid(column=0, row=4)
            ttk.Label(frm, text="After ranking your villagers use this to get NMT island decision help:").grid(column=0, row=5)
            ttk.Button(frm, text="Decision Helper", command=lambda: var.set(3)).grid(column=0, row=6)
        except:
            ttk.Label(frm, text="No rank file found. Please rank villagers first.").grid(column=0, row=2)
            ttk.Label(frm, text="After ranking your villagers you can use the decision helper.").grid(column=0, row=5)
        ttk.Button(frm, text="Rank Villagers", command=lambda: var.set(1)).grid(column=0, row=3)

        ttk.Button(frm, text="Exit", command=lambda: var.set(4)).grid(column=0, row=7)

        root.update()

        root.wait_variable(var)
        res = var.get()
        root.destroy()

        if res == 1:
            sorted = get_sort(villagers)
        elif res==2:
            see_sort(villagers, sorted)
        elif res==3:
            recommender(villagers, sorted)
        elif res==4:
            return

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    with open("villagers.txt", "r", encoding='ISO-8859-1') as f:
        villagers = eval(f.read())

    main(villagers)
