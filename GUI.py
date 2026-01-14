import FreeSimpleGUI as fsg


running: bool = True

# crash/stop the program/instance/process manually
# and return error catches as logs in the debug popup menu
# explaining why the process needed to be stopped
def crash(process):
    pass



if __name__ == "__main__":

    fsg.theme('BluePurple')

    layout = [
        [fsg.Text('Browser Instance:'), fsg.Text('Chrome Instance')],
        [fsg.Button("Launch")],
        [fsg.Button("Exit")]
    ]

    window = fsg.Window('Test Window', layout)
    event, values = window.read()
    if event == fsg.WINDOW_CLOSED:
        print('You pressed', values[0])

    # while running:
    #     event, values = window.read()
    #     if event == fsg.WIN_CLOSED or event == 'Exit':
    #         break
    #     print('You entered:', values[0])
    #window.close()
