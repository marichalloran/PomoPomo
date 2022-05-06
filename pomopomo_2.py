"""
Marianne's Pomodoro tracking
"""
import os
import os.path as op

import datetime as dt
import pandas as pd
import tkinter
from tkinter import messagebox
import winsound

log_path = op.join(r'C:\Users', f'{op.expanduser("~")}', 'Documents')
pomo_path = op.join(log_path, 'pomo_log.csv')
if op.exists(pomo_path):
    pomo_log = pd.read_csv(pomo_path)
else:
    pomo_log = pd.DataFrame([])
total_pomodoros = 0


def Pomobox():
    """Fancy Pomodoro Timer"""

    """ Pomo class """
    frame = tkinter.Tk()
    frame.title("PomoPomo")
    frame.geometry("250x200")

    title = tkinter.Label(frame, text="Pomodoro Timer", font='Helvetica 18 bold')
    title.grid(row=1, column=1)
    title.place(x=125, y=25, anchor="center")

    def run_pomo():
        """ Run Single Pomodoro Routine """
        t_now = dt.datetime.now()
        # Focus time
        ct = chill_time.get(1.0, "end-1c")
        ft = focus_time.get(1.0, "end-1c")
        time_stop_focus = t_now + dt.timedelta(0, (int(ft) * 60))
        # Chill time
        time_stop_chill = t_now + dt.timedelta(0, (int(ft) * 60) + (int(ct) * 60))

        alert = tkinter.Tk()
        alert.withdraw()
        messagebox.showinfo(
            'Pomodoro Timer Started!',
            f'It is now {t_now.strftime("%H:%M %p")}. Timer set for {ft} minutes.')
        while True:
            t_now = dt.datetime.now()
            if t_now > time_stop_focus:
                #  Pomodoro time over!
                for sound_timer in range(2):
                    winsound.Beep((sound_timer + 100), 700)
                messagebox.showinfo(
                    'BREAK TIME!',
                    f'It is now {t_now.strftime("%H:%M %p")}. \n Timer set for {ct} minutes.')
                # Chill time
                time_stop_chill = t_now + dt.timedelta(0, (int(ct) * 60))
                time_stop_focus = t_now + dt.timedelta(0, (int(ft) * 60) + (int(ct) * 60))
                global total_pomodoros
                total_pomodoros += 1
                print(f'Now {t_now}')
                print(f'New chill time {time_stop_chill}')
                #  Chill time over!
                message_board.after(10, lambda: message_board.config(
                    text=f'Chill Time will end at \n{time_stop_chill.strftime("%H:%M %p")}'))

            if t_now > time_stop_chill:
                for sound_timer in range(1):
                    winsound.Beep((sound_timer + 100), 700)
                messagebox.showinfo(
                    'BREAK TIME!',
                    f'It is now {t_now.strftime("%H:%M %p")}')
                # Focus time
                time_stop_focus = t_now + dt.timedelta(0, (int(ft) * 60))
                time_stop_chill = time_stop_focus + dt.timedelta(0, (int(ct) * 60) + (int(ft) * 60))
                message_board.after(10, lambda: message_board.config(
                    text=f'Pomodoro done!\nYou have done {total_pomodoros} so far!'))
                break
        global pomo_log
        global pomo_path
        pomo_log = pomo_log.append({
            'Day': dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'Number of Pomos': total_pomodoros
        }, ignore_index=True)
        pomo_log.to_csv(pomo_path, index=False)
        print('One Pomo done!')

    def print_start():
        """ Start Stop options  """
        ct = chill_time.get(1.0, "end-1c")
        ft = focus_time.get(1.0, "end-1c")
        message_board.config(text=f'Starting pomodoro for {ft} minutes \n and {ct} minutes for a break')
        time_stop_focus = dt.datetime.now() + dt.timedelta(0, (int(ft) * 60))
        message_board.after(600, lambda: message_board.config(
            text=f'Focus Time will end at \n{time_stop_focus.strftime("%H:%M %p")}'))
        run_pomo()

    # Text box for pomo time
    focus_time = tkinter.Text(frame, height=1, width=10)
    title = tkinter.Label(frame, text="Focus Time", font='Helvetica 10')
    title.grid(row=1, column=1)
    title.place(x=75, y=50, anchor="center")
    focus_time.place(x=75, y=80, anchor="center")

    # Text box for pomo time
    chill_time = tkinter.Text(frame, height=1, width=10)
    title = tkinter.Label(frame, text="Chill Time", font='Helvetica 10')
    title.grid(row=1, column=1)
    title.place(x=175, y=50, anchor="center")
    chill_time.place(x=175, y=80, anchor="center")

    # Button Creation
    start_button = tkinter.Button(frame, text="Start", command=print_start)
    start_button.place(x=125, y=120, anchor="center")

    # Label Creation
    message_board = tkinter.Label(frame, text="")
    message_board.place(x=125, y=160, anchor="center")

    frame.mainloop()


def main():
    """
    Creates the pomodoro for the defined times in the variables pomo_time and chill_time
    """
    Pomobox()


if __name__ == "__main__":
    from genmarkpy.utils.parsers import ArgumentParser

    parser = ArgumentParser(description='PomoPomo')

    args = vars(parser.parse_args())
    main(**args)
