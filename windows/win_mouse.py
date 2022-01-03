# click function stolen from https://stackoverflow.com/questions/18983675/python-script-to-control-mouse-clicks
import win32con
import win32api
import keyboard
import time

def click(x=None,y=None, button=1):
    """
    Clicks on given position x,y with the given button

    :param int x: Horizontal position in pixels, starts from top-left position
    :param int y: Vertical position in pixels, start from top-left position
    :param int button: If 1, it will check for mouse event on the left button, if 2, it will check for mouse event on the right button
    """

    if button == 1:
        event_down = win32con.MOUSEEVENTF_LEFTDOWN
        event_up = win32con.MOUSEEVENTF_LEFTUP
    elif button == 2:
        event_down = win32con.MOUSEEVENTF_RIGHTDOWN
        event_up = win32con.MOUSEEVENTF_RIGHTUP
    else:
        raise BaseException('button parameter can only be 1 or 2.')

    if x == None or y == None:
        xx, yy = win32api.GetCursorPos()
    if x == None:
        x = xx
    if y == None:
        y = yy

    win32api.SetCursorPos((x,y))
    win32api.mouse_event(event_down,x,y,0,0)
    win32api.mouse_event(event_up,x,y,0,0)

def auto_clicker(stoploop_key: str='q', x=None, y=None, button=1, delay=0.1):
    """
    Clicks the specified mouse button after the specified delay time inside a loop.

    :param  str stoploop_key: stops the loop

    :param int x: teleports mouse x position to the specified x position

    :param int y: teleports mouse y position to the specified y position

    :param int button: selects the mouse button to press. (there's 2 buttons only: left mouse button that is 1 and right mouse button that is 2)
    
    :param int delay: presses the button specified after the specified delay(this)
    """
    t_start = time.time()
    while True:
        t_end = time.time()
        if keyboard.is_pressed(stoploop_key):
            break
        if t_end-t_start >= delay:
            click(x,y,button)
            t_start = time.time()