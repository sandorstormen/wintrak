import eel
# Set web files folder
eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    return 'Hello from {}'.format(x)

eel.say_hello_js('Python World!')

eel.start('index.html', mode='electron')
#eel.start('hello.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])