from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
from IPython import embed
import time

f = open("villagers.txt", "r")
villagers = eval(f.read())
f.close()

def see_sort(villagers, sorted, top=10):
    root = Tk()
    root.title('Results')
    frm = ttk.Frame(root, padding=10)
    var = IntVar()
    def on_exit():
        var.set(1) # prevents stuck on wait
        root.destroy()
        sys.exit()
    root.protocol('WM_DELETE_WINDOW', on_exit)

    total_size = root.winfo_screenwidth() * 0.9 # margin
    side = int(total_size/top)

    frm.grid()
    imagestop = [None]*top
    for i in range(top):
        villager = villagers[sorted[i]]
        ttk.Label(frm, text= str(i+1) + ". " + villager["Name"]).grid(column=i, row=0)
        imagestop[i] = Image.open("images/"+villager["Poster"])
        imagestop[i] = imagestop[i].resize((side, side), Image.ANTIALIAS)
        imagestop[i] = ImageTk.PhotoImage(imagestop[i])
        ttk.Label(frm, image=imagestop[i]).grid(column=i, row=1)
        #root.update()

    ttk.Label(frm, text= " ").grid(column=0, row=2)

    imagesbot = [None]*top
    for i in range(top):
        j = len(villagers) - (i+1)
        villager = villagers[sorted[j]]
        ttk.Label(frm, text= str(j+1) + ". " + villager["Name"]).grid(column=i, row=3)
        imagesbot[i] = Image.open("images/"+villager["Poster"])
        imagesbot[i] = imagesbot[i].resize((side, side), Image.ANTIALIAS)
        imagesbot[i] = ImageTk.PhotoImage(imagesbot[i])
        ttk.Label(frm, image=imagesbot[i]).grid(column=i, row=4)
        #root.update()

    button = ttk.Button(frm, text="Continue", command=lambda: var.set(-1)).grid(column=(top-1), row=5)
    root.update()
    root.wait_variable(var)
    root.destroy()



def get_sort(villagers, expected=2800):
    starttime = time.time()
    root = Tk()
    root.title('Villager Ranker')
    frm = ttk.Frame(root, padding=10)
    var = IntVar()
    def on_exit():
        var.set(1) # prevents stuck on wait
        root.destroy()
        sys.exit()
    root.protocol('WM_DELETE_WINDOW', on_exit)

    names = list(villagers)
    random.shuffle(names)
    lists = [[villager] for villager in names]

    count = 0

    while (len(lists) > 1):
        print("Advancing stage...",len(lists),"sets needing merge")
        nextlists = []
        while(len(lists) > 0):
            if (len(lists) == 1):
                nextlists += [lists[0]]
                break
            merge1 = lists[0]
            merge2 = lists[1]
            lists = lists[2:]
            merged = []
            #begin merging
            while (len(merge1) > 0) and (len(merge2) > 0):
                cand1 = merge1[0]
                cand2 = merge2[0]

                #GET PREFERENCE
                for widget in frm.winfo_children():
                    widget.destroy()
                image1 = Image.open("images/"+villagers[cand1]["Poster"])
                image1 = image1.resize((256, 256), Image.ANTIALIAS)
                image1 = ImageTk.PhotoImage(image1)
                image2 = Image.open("images/"+villagers[cand2]["Poster"])
                image2 = image2.resize((256, 256), Image.ANTIALIAS)
                image2 = ImageTk.PhotoImage(image2)

                frm.grid()
                ttk.Label(frm, text=str(int((100*count)/expected))+"%").grid(column=0, row=0)
                if count > 10:
                    secs_per_count = (time.time()-starttime)/count
                    mins = max(int((expected-count)*(secs_per_count/60)), 1)
                    ttk.Label(frm, text="~"+str(mins)+" mins left").grid(column=1, row=0)
                else:
                    ttk.Label(frm, text="~? mins left").grid(column=1, row=0)

                ttk.Label(frm, text=villagers[cand1]["Name"]).grid(column=0, row=1)
                ttk.Label(frm, text=villagers[cand2]["Name"]).grid(column=1, row=1)


                ttk.Label(frm, image=image1).grid(column=0, row=2)
                ttk.Label(frm, image=image2).grid(column=1, row=2)

                ttk.Label(frm, text=villagers[cand1]["Personality"]).grid(column=0, row=3)
                ttk.Label(frm, text=villagers[cand2]["Personality"]).grid(column=1, row=3)
                ttk.Label(frm, text='"'+villagers[cand1]["Catchphrase"]+'"').grid(column=0, row=4)
                ttk.Label(frm, text='"'+villagers[cand2]["Catchphrase"]+'"').grid(column=1, row=4)

                button1 = ttk.Button(frm, text="Preferable", command=lambda: var.set(-1)).grid(column=0, row=5)
                root.bind('<Left>', lambda x : var.set(-1))
                button2 = ttk.Button(frm, text="Preferable", command=lambda: var.set( 1)).grid(column=1, row=5)
                root.bind('<Right>', lambda x : var.set(1))
                root.update()

                root.wait_variable(var,)
                prefers1 = var.get() < 0
                #prefers1 = random.choice([True, False])
                count += 1

                if prefers1:
                    print("Prefers",villagers[cand1]["Name"], "over", villagers[cand2]["Name"])
                    merged += [cand1]
                    merge1 = merge1[1:]
                else:
                    print("Prefers",villagers[cand2]["Name"], "over", villagers[cand1]["Name"])
                    merged += [cand2]
                    merge2 = merge2[1:]

            merged = merged + merge1 + merge2 # add leftovers
            print("Merged sets")

            nextlists += [merged]
        lists = nextlists

    print("Total choices:", count)
    root.destroy()
    sorted = lists[0]

    root = Tk()
    root.title('Village Ranker')
    frm = ttk.Frame(root, padding=10)
    var = IntVar()
    def on_exit():
        var.set(1) # prevents stuck on wait
        root.destroy()
        sys.exit()
    root.protocol('WM_DELETE_WINDOW', on_exit)
    frm.grid()
    ttk.Label(frm, text="Finished ranking").grid(column=0, row=0)
    ttk.Label(frm, text="Do you want to save?").grid(column=0, row=1)
    ttk.Label(frm, text="This will override older ranks.").grid(column=0, row=2)
    ttk.Label(frm, text="Back up the ranked.txt file if you want.").grid(column=0, row=3)
    ttk.Button(frm, text="Save results", command=lambda: var.set(1)).grid(column=0, row=4)

    root.wait_variable(var,)
    shouldsave = var.get() > 0
    if shouldsave:
        print("Saving results...")
        f = open("ranked.txt", "w")
        f.write(str(sorted))
        f.close()
    root.destroy()

    see_sort(villagers, sorted)
    return sorted

if __name__ == "__main__":
    sorted = get_sort(villagers)
    f = open("ranked.txt", "r")
    sorted = eval(f.read())
    f.close()
    see_sort(villagers, sorted)

    embed()
