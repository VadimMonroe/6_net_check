import os
import socket
import threading

import netifaces

socket.setdefaulttimeout(0.9)
print_lock = threading.Lock()

list_of_working_base_ip = []
list_of_working_ip = []
threads = []


def net_info() -> None:
    """Посмотреть активность сетевых устройств"""
    print(os.system('netstat -nr'))
    print(os.system('arp -a'))

    """Получить все имена сетевых портов"""
    print(netifaces.interfaces())

    """Получить своё сетевое имя и айпи"""
    print('ip: ', socket.gethostbyname_ex(socket.gethostname()))


def port_searching(ip: str) -> None:
    """Проверяем порты конкретного ip"""
    for i in range(0, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn = s.connect_ex((ip, i))
            with print_lock:
                if conn == 0:
                    print(f'{ip} Port {i}: OPEN')
            s.close()
        except Exception as E3port:
            print('E3port:', E3port)


def threading_port(ip_list: list):
    """Запускаем параллельный поиск портов в нескольких IP"""
    for _ in ip_list:
        check_ip_port = threading.Thread(target=port_searching, args=[_])
        check_ip_port.start()
        threads.append(check_ip_port)


def threading_ping(ip: str, ip_list: list) -> None:
    """Параллельная проверка работающих айпишников"""
    a = os.popen(f'ping -c 1 -t 1 {ip}').readlines()
    if '100.0% packet loss' not in a[3]:
        ip_list.append(ip)


def check_base_list(ip_list) -> None:
    """Generate all IPs from 192.168.0.1 - 192.168.255.1"""
    for i in range(256):
        base_ip = f'192.168.{i}.1'
        check_ip_thread = threading.Thread(target=threading_ping, args=[base_ip, ip_list])
        check_ip_thread.start()
        threads.append(check_ip_thread)


def check_ip_list(ip_list) -> None:
    """Generate all IPs from 192.168....0 - 192.168....255"""
    for _ in list_of_working_base_ip:
        for j in range(256):
            temp = _.split('.')
            temp[3] = str(j)
            check_ip_thread = threading.Thread(target=threading_ping, args=['.'.join(temp), ip_list])
            check_ip_thread.start()


def main() -> None:
    print('\033[034mCheck base ip:\033[0m')
    check_base_list(list_of_working_base_ip)
    print(list_of_working_base_ip)
    print('\033[034mCheck next level ip:\033[0m')
    check_ip_list(list_of_working_ip)
    for thread in threads:
        thread.join()
    print(list_of_working_ip)
    print('\033[034mCheck ports:\033[0m')
    threading_port(list_of_working_ip)
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
    # net_info()
