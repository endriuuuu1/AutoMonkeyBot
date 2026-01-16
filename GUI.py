import FreeSimpleGUI as fsg
from bot import session_init

# running: bool = True

# crash/stop the program/instance/process manually
# and return error catches as logs in the debug popup menu
# explaining why the process needed to be stopped
def crash(process):
    pass

# end/quit any process passed in here
def destroy(process):
    pass

if __name__ == "__main__":

    fsg.theme('BluePurple')

    layout = [
        [fsg.Text('Browser Instance:'), fsg.Text('Chrome Instance')],
        [fsg.Button("Launch")],
        [fsg.Button("Close")],
    ]

    window = fsg.Window('Browser Instance', layout)
    while True:
        event, values = window.read()
        if event == fsg.WIN_CLOSED or event == 'Close':
            break
        elif event == 'Launch':
            window.perform_long_operation(session_init(), '-BOT-FINISHED-')
        elif event == '-BOT-FINISHED-':
            fsg.popup('Browser Instance Closed')
    window.close()

    # while running:
    #     event, values = window.read()
    #     if event == fsg.WIN_CLOSED or event == 'Exit':
    #         break
    #     print('You entered:', values[0])
    #window.close()
