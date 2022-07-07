from random import randint
from tkinter import *
from tkinter import messagebox, ttk


from solve import IDS, UCS, Astart, IDAstar


class EightPuzzleGUI:
    '''
    GUI class for Eight Puzzle
    '''

    def __init__(self, root):
        root.minsize(width=400, height=200)
        root.place_slaves
        root.title("8 Puzzle")

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Inputs for numbers
        self.sq1 = IntVar()
        sq1_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq1)
        sq1_entry.grid(column=0, row=0, sticky=(W, E))

        self.sq2 = IntVar()
        sq2_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq2)
        sq2_entry.grid(column=1, row=0, sticky=(W, E))

        self.sq3 = IntVar()
        sq3_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq3)
        sq3_entry.grid(column=2, row=0, sticky=(W, E))

        self.sq4 = IntVar()
        sq4_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq4)
        sq4_entry.grid(column=0, row=1, sticky=(W, E))

        self.sq5 = IntVar()
        sq5_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq5)
        sq5_entry.grid(column=1, row=1, sticky=(W, E))

        self.sq6 = IntVar()
        sq6_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq6)
        sq6_entry.grid(column=2, row=1, sticky=(W, E))

        self.sq7 = IntVar()
        sq7_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq7)
        sq7_entry.grid(column=0, row=2, sticky=(W, E))

        self.sq8 = IntVar()
        sq8_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq8)
        sq8_entry.grid(column=1, row=2, sticky=(W, E))

        self.sq9 = IntVar()
        sq9_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.sq9)
        sq9_entry.grid(column=2, row=2, sticky=(W, E))

        # Select options
        self.release = IntVar()
        ttk.Radiobutton(self.mainframe, text="جست و جوی آگاهانه", variable=self.release,
                        value=1, command=self.is_select).grid(column=3, row=0, sticky=(W, E))
        ttk.Radiobutton(self.mainframe, text="جست و جوی ناآگاهانه", variable=self.release,
                        value=2, command=self.is_select).grid(column=3, row=1, sticky=(W, E))

        # Buttons for make random number and running
        ttk.Button(self.mainframe, text="Random", width=15, command=self.random_init).grid(
            column=3, row=4, columnspan=2, sticky=W)

        ttk.Button(self.mainframe, text="RUN", width=15, command=self.run).grid(
            column=3, row=5, columnspan=2, sticky=W)

        # Press Enter on Keyboard and run the program
        root.bind("<Return>", self.run)

    def random_init(self):
        '''
        Set random value for starting position
        '''
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        sq_values = [self.sq1, self.sq2, self.sq3,
                     self.sq4, self.sq5, self.sq6, self.sq7, self.sq8, self.sq9]
        for i in range(9):
            random_num = randint(0, len(nums)-1)
            sq_values[i].set(nums[random_num])
            del(nums[random_num])

    def is_select(self):
        '''
        Check which radiobtton selected and make option menu from their value.
        '''
        option_list = []
        if self.release.get() == 1:
            option_list = ('A* (misplace)', 'A* (manhattan)',
                           'IDA* (misplace)', 'IDA* (manhattan)',
                           'A* (euclidean)', 'IDA* (euclidean)')
        elif self.release.get() == 2:
            option_list = ('UCS', 'IDS')

        self.option_select = StringVar()
        ttk.OptionMenu(self.mainframe, self.option_select, option_list[0], *
                       option_list).grid(column=3, row=3, sticky=(W, E))

    def run(self):
        '''
        Get all values for start process. Processes are get from another file.
        '''
        try:
            state = [self.sq1.get(), self.sq2.get(), self.sq3.get(), self.sq4.get(),
                     self.sq5.get(), self.sq6.get(), self.sq7.get(), self.sq8.get(), self.sq9.get()]
            select_value = self.option_select.get()
            if select_value == 'A* (misplace)':
                method = Astart(start_pos=state, heuristic='misplace')
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'A* (manhattan)':
                method = Astart(start_pos=state, heuristic='manhattan')
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'IDA* (misplace)':
                method = IDAstar(start_pos=state, heuristic='misplace')
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'IDA* (manhattan)':
                method = IDAstar(start_pos=state, heuristic='manhattan')
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'A* (euclidean)':
                method = Astart(start_pos=state, heuristic='euclidean')
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'IDA* (euclidean)':
                method = IDAstar(start_pos=state, heuristic='euclidean')
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'UCS':
                method = UCS(start_pos=state)
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
            elif select_value == 'IDS':
                method = IDS(start_pos=state)
                (status, pop, max_size, depth, p), time, space = method.solve()
                messagebox.showinfo(message='solve:{}\nnode pop:{}\nnode expand:{}\ndepth:{}\nmoves:{}\ncost:{}\ntime:{}\nspace:{}'.format(
                    status, pop, max_size+pop, depth, p.print_move(), p.path_cost, time, space))
        except TclError:
            messagebox.showinfo(
                message='تمام ورودی ها عدد نیستند، لطفا ورودی ها را مجددا چک بفرمایید')
        except NameError:
            messagebox.showinfo(
                message='یکی از روش های جست و جو رو انتخاب کنید')


if __name__ == '__main__':
    '''
    Main of the program
    '''
    root = Tk()
    EightPuzzleGUI(root)
    root.mainloop()
