import os
import socket
import netifaces


def net_info() -> None:
    """
    Посмотреть активность сетевых устройств
    Используются команды mac-os
    """
    print(os.system('netstat -nr'))
    print(os.system('arp -a'))

    """Получить все имена сетевых портов"""
    print(netifaces.interfaces())

    """Получить своё сетевое имя и айпи"""
    print('ip: ', socket.gethostbyname_ex(socket.gethostname()))

# net_info()
