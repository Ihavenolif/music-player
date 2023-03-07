from pynput import keyboard

def on_press(key):
    print("{0} pressed".format(key))

def on_release(key):
    print("{0} released".format(key))

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()