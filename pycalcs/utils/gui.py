import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile, \
asksaveasfilename, askdirectory

class gui:
    default_button_width = 30
    def __init__(self, title,width=500,height=300):
        ''' initializes the gui manager object.
            which involes making a tk root.
            & corresponding top level window. 
            
            does not start displying window right away.
            call other gui methods to populate it first.
            '''

        root = tk.Tk()
        root.withdraw()
        root.title(title)
        
        self.toplevel = tk.Toplevel(width=width, height=height)
        self.toplevel.protocol('WM_DELETE_WINDOW',root.destroy)
        

    def mainloop(self): # wait for input
        '''To be run after main window is setup.
            this starts an unending loop & waits for users to 
            trigger callbacks.'''
        self.toplevel.mainloop()

    def add_button(self, title, command):
        '''adds a button to the main window.
            with the title title & when clicked will run command
            '''
        b = tk.Button(self.toplevel, 
            text=title,
            width=gui.default_button_width, 
            command=command)
        #It adds to the bottom of the last button
        b.pack()




def promptbox(prompt, validation = None, error_text = None, 
    repeat_on_error=True, title='',
    width=100):
    ''' This is a blocking function that opens up a new window with 
        a textbox to prompt the user for something.

        the window looks like so:
         ____________________ 
        |  title      {_} {x}|
        |--------------------|
        | Error text         |
        | message message    |
        | ________________   |
        | |   entry box   |  |
        | -----------------  |
        | {confirm} {cancel} |
        |____________________|

        this will block code execution until they hit either confirm or cancel
        so don't worry about asynchrony or anything like that. 
        the return is a string. 
        if they hit cancel it will return None.

        validation is a callback that will be applied to the text entered, 
        it will be assumed the return will be truthy for a valid entry
        and falsey for an invalid entry for any given string. 
        e.g. validate(entry) -> 
        truthy : return entry
        falsey : try again or return None 


        if falsey and repeat on error, validate_error_text will be shown and
        they can re-enter.

        If no validation is provided, return anything entered.

        if repeat_on_error is false it will just return None, just like canceling  

        by default it's 600px wide. but you can specify that if you feel like it.
    '''
    t = tk.Toplevel()
    t.title(title)

    err_text = tk.StringVar() # in case of error this will be populated
    msg_txt = tk.StringVar() # the body text container for messages

    # prepare to add text to window.
    err = tk.Message(t,textvariable=err_text,width=width)
    err.pack()
    msg = tk.Message(t,textvariable=msg_txt,width=width)
    msg.pack()

    # add body text
    msg_txt.set(prompt)

    # add entry box to the window
    entry = tk.Entry(t,width=width)
    entry.pack()

    f = tk.Frame(t) # this is to make the buttons horizontal.
    f.pack()
    # add confirm buttons
    confirm = tk.Button(f,text='confirm', command=t.quit)
    
    def quit_and_destroy():
        t.quit() # this doesn't remove the gui, 
        t.destroy() # this removes all gui components
        # if we try and access any components after 
        #   this it will throw tclError


    cancel = tk.Button(f,text='cancel', command=quit_and_destroy)
    confirm.pack(side=tk.LEFT)
    cancel.pack(side=tk.RIGHT)

    # make it so they can just hit return and it will sumbit
    t.bind('<Return>',lambda ev: t.quit()) 

    inp = None # container for the input given by user
    ret = None # the value to return
    while True: # iterate until we break
        t.mainloop() # cancel or confirm will break this.
        try:
            inp = entry.get().strip()
            
            # if no validation provided always return input.
            if not validation: return inp 
            # validate the input
            if not validation(inp): # if not valid.
                # clear the input. it's invalid anyway
                entry.delete(0,last=len(entry.get())) 
                
                if not repeat_on_error: # if we shouldn't repeat
                    # display the error text in such a way as they'll see it
                    tk.messagebox.showinfo(error_text.format(text=inp)) 
                    break
                else: # we should repeat
                    # display the error text
                    err_text.set(error_text.format(text=inp))  
            else: # their entry is valid
                ret = inp
                break # ret is updated. return that
        # and continue to the next iteration of the loop

        except tk.TclError:
            # that means t has been destroyed by cancel
            # just break and return None ret
            break
    t.destroy()
    return ret







