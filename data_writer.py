
def open_data_file(path='soccor_data.log'):
    return open(path, 'w')

def when_receive_message(f, message):
    f.write('message')

def when_send_command(f, command):
    f.write(command)
