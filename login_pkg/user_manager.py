import os
import logging

logger = logging.getLogger(__name__)

file_name = 'usr_data/level.txt'

def decrypt(msg):
    #construct the dic for lower case alphabets
    low_alphas = 'abcdefghijklmnopqrstuvwxyz'
    low_alpha_num_dic = {}
    for n in range(26):
        low_alpha_num_dic[low_alphas[n]] = n

    #construct the dic for upper case alphabets
    upp_alphas = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    upp_alpha_num_dic = {}
    for n in range(26):
        upp_alpha_num_dic[upp_alphas[n]] = n

    ##
    pwd = 'EngG'
    d_msg = ''
    msg_index = 0
    pwd_index = 0
    #main decryption loop
    while msg_index < len(msg):
        if msg[msg_index] in low_alphas:
            if pwd[pwd_index] in low_alphas:
                new_char_val = low_alpha_num_dic[msg[msg_index]] - low_alpha_num_dic[pwd[pwd_index]]
                if new_char_val < 0:
                    new_char_val += 26
                for key,val in low_alpha_num_dic.items():
                    if val == new_char_val:
                        d_msg += key
                        break
            if pwd[pwd_index] in upp_alphas:
                new_char_val = low_alpha_num_dic[msg[msg_index]] - upp_alpha_num_dic[pwd[pwd_index]]
                if new_char_val < 0:
                    new_char_val += 26
                for key,val in low_alpha_num_dic.items():
                    if val == new_char_val:
                        d_msg += key
                        break

        elif msg[msg_index] in upp_alphas:
            if pwd[pwd_index] in low_alphas:
                new_char_val = upp_alpha_num_dic[msg[msg_index]] - low_alpha_num_dic[pwd[pwd_index]]
                if new_char_val < 0:
                    new_char_val += 26
                for key,val in upp_alpha_num_dic.items():
                    if val == new_char_val:
                        d_msg += key
                        break
            if pwd[pwd_index] in upp_alphas:
                new_char_val = upp_alpha_num_dic[msg[msg_index]] - upp_alpha_num_dic[pwd[pwd_index]]
                if new_char_val < 0:
                    new_char_val += 26
                for key,val in upp_alpha_num_dic.items():
                    if val == new_char_val:
                        d_msg += key
                        break

        else:
            d_msg += msg[msg_index]

        msg_index += 1
        pwd_index += 1
        if pwd_index == len(pwd):
            pwd_index = 0
    logging.debug('decrypt')
    logging.debug(msg)
    logging.debug(d_msg)
    logging.debug('decrypt')

    return d_msg

def encrypt(msg):
    #construct the dic for lower case alphabets
    low_alphas = 'abcdefghijklmnopqrstuvwxyz'
    low_alpha_num_dic = {}
    for n in range(26):
        low_alpha_num_dic[low_alphas[n]] = n
    #construct the dic for upper case alphabets
    upp_alphas = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    upp_alpha_num_dic = {}
    for n in range(26):
        upp_alpha_num_dic[upp_alphas[n]] = n
    ##
    pwd = 'EngG'
    e_msg = ''
    msg_index = 0
    pwd_index = 0
    #main encryption loop
    while msg_index < len(msg):
        if msg[msg_index] in low_alphas:
            if pwd[pwd_index] in low_alphas:
                new_char_val = low_alpha_num_dic[msg[msg_index]] + low_alpha_num_dic[pwd[pwd_index]]
                if new_char_val > 25:
                    new_char_val -= 26
                for key,val in low_alpha_num_dic.items():
                    if val == new_char_val:
                        e_msg += key
                        break
            if pwd[pwd_index] in upp_alphas:
                new_char_val = low_alpha_num_dic[msg[msg_index]] + upp_alpha_num_dic[pwd[pwd_index]]
                if new_char_val > 25:
                    new_char_val -= 26
                for key,val in low_alpha_num_dic.items():
                    if val == new_char_val:
                        e_msg += key
                        break

        elif msg[msg_index] in upp_alphas:
            if pwd[pwd_index] in low_alphas:
                new_char_val = upp_alpha_num_dic[msg[msg_index]] + low_alpha_num_dic[pwd[pwd_index]]
                #print(new_char_val)
                if new_char_val > 25:
                    new_char_val -= 26
                for key,val in upp_alpha_num_dic.items():
                    if val == new_char_val:
                        e_msg += key
                        break
            if pwd[pwd_index] in upp_alphas:
                new_char_val = upp_alpha_num_dic[msg[msg_index]] + upp_alpha_num_dic[pwd[pwd_index]]
                if new_char_val > 25:
                    new_char_val -= 26
                for key,val in upp_alpha_num_dic.items():
                    if val == new_char_val:
                        e_msg += key
                        break

        else:
            e_msg += msg[msg_index]

        msg_index += 1
        pwd_index += 1
        if pwd_index == len(pwd):
            pwd_index = 0
            
    return e_msg

def load_data():
    '''
    if not os.path.exists('level.txt'):
        return []
    '''
    with open(file_name,'r') as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines]

def save_data(usr_name,password,level):
    logging.debug([usr_name,password,level])
    #encrypt the password
    password = encrypt(password)
    #open the file and append new data in
    with open(file_name,'a') as file:
        file.write(f'{usr_name},{password},{level}\n')

def delete_all():
    #opening the file as w will delete all data automatically
    with open(file_name,'w') as file:
        pass

def update_data(usr_name,level):
    #load data
    datas = load_data()
    #find the target usr and change the level
    for data in datas:
        if usr_name == data[0]:
            data[2] = level
            break
    #delete all old data before writing back the new data
    delete_all()
    for data in datas:
        data[1] = decrypt(data[1])
        save_data(data[0],data[1],data[2])


