import sys
import os
import time

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import curses
import logging

logger = logging.getLogger(__name__)

import user_manager
#import time

def input_info(stdscr, line, msg):
    stdscr.clear()
    stdscr.addstr(line, 0, msg)
    stdscr.refresh()

    curses.echo()
    usr_input = stdscr.getstr(line + 1, 0).decode('utf-8')
    logging.debug(usr_input)

    return usr_input

def login_manager(stdscr):
    stdscr.nodelay(0) #allow waiting for input
    
    name = input_info(stdscr,0,'User Name: ')

    while name == '':
        _ = input_info(stdscr,0,'No empty user name! Press ENTER to enter a proper user name. ')
        name = input_info(stdscr,0,'User Name: ')
    usrs_info = user_manager.load_data()
    #logging.debug(usrs_info)
    usr_info = []
    all_names = []
    found = False
    for info in usrs_info:
        if info[0] == name:
            usr_info = info
            logging.info(info)
            logging.info(usr_info)
            found = True
        all_names.append(info[0])

    skip = False
    if found:
        attempt_allowed = 3
        attempt = 1
        while attempt <= attempt_allowed:
            password = input_info(stdscr,0,'Password: ')
            if password == user_manager.decrypt(usr_info[1]):
                level = usr_info[2]
                if int(level) >= 4:
                    _ = input_info(stdscr,0,'Although the level can be infinite. You have reached the maximum level that the plot can support! Press ENTER to exit.')
                    return False,None,None,None
                _ = input_info(stdscr,0,f'Successful login! Welcome {name}! Press ENTER to start!')
                _ = input_info(stdscr,0,'Skip the plots? (y/n)')
                logging.debug(_)
                if _ == 'y':
                    skip = True
                    logging.debug(skip)
                else:
                    skip = False
                break
            else:
                logging.info(f'Failed login. Plz try again. You still have {attempt_allowed-attempt} attempts allowed.')
                _ = input_info(stdscr,0,f'Failed login. Plz try again. You still have {attempt_allowed-attempt} attempts allowed. Press ENTER to continue.')
                #time.sleep(1)
                attempt+=1
        if attempt == attempt_allowed+1:
            _ = input_info(stdscr,0,f'Service denied. Press ENTER to quit the game. ')
            #time.sleep(5)
            return False,None,None,None
    else:
        _ = input_info(stdscr,0,f'User not found, plz create an account! Press ENTER to create your account! If you want to quit the game, press x and then press enter. ')
        if _ == 'x':
            logging.info('x')
            return False,None,None,None
        else:
            name = input_info(stdscr,0,'Create User Name: ')
            while name == '':
                _ = input_info(stdscr,0,'No empty user name! Press ENTER to enter a proper user name. ')
                name = input_info(stdscr,0,'User Name: ')
            while name in all_names:
                _ = input_info(stdscr,0,f'This name has been used. Press ENTER to rename. ')
                name = input_info(stdscr,0,'Create User Name: ')
            password = input_info(stdscr,0,'Set your password: ')
            while password == '':
                _ = input_info(stdscr,0,'No empty password! Press ENTER to select a proper password. ')
                password = input_info(stdscr,0,'Set your password(Letters only for better encryption protection!): ')
            _ = input_info(stdscr,0,f'Your password has been encrypted and stored! Press ENTER to enter the game! If you want to quit the game, press x and then press enter. ')
            if _ == 'x':
                logging.info('x')
                return False,None,None,None
            level = 1
            user_manager.save_data(name,password,level)
            logging.info([name,password,level])
            _ = input_info(stdscr,0,'Skip the plots? (y/n)')
            if _ == 'y':
                skip = True
            else:
                skip = False
    
    stdscr.refresh()
    stdscr.clear
    #switch back to the no-waiting input mode
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    return True,name,level,skip

#wzl
