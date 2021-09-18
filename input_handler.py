from pynput import keyboard

curr_held = []


def on_press(key):
    if key not in curr_held:
        curr_held.append(key)


def on_release(key):
    curr_held.remove(key)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
