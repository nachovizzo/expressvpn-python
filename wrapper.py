import random
import subprocess

VPN_CONNECT = 'expressvpn connect'
VPN_LIST = 'expressvpn list'
VPN_DISCONNECT = 'expressvpn disconnect'


class ConnectException(Exception):
    pass


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return list([
        str(v).replace('\\t', ' ').replace('\\n',
                                           ' ').replace('b\'', '').replace(
                                               '\'', '').replace('b"', '')
        for v in iter(p.stdout.readline, b'')
    ])


def activation_check():
    print('Checking if the client is activated... (Please wait)')
    out = connect()
    if not is_activated(out):
        print('Run <expressvpn activate> and provide your activation key.')
        exit(1)
    print('Client is successfully logged in.')
    disconnect()


def connect():
    return check_connection(run_command(VPN_CONNECT))


def disconnect():
    run_command(VPN_DISCONNECT)
    return


def is_activated(connect_output):
    return not check_output(connect_output, 'Please activate your account')


def check_connection(out):
    if check_output(
            out, 'We were unable to connect to this VPN location'):
        raise ConnectException()
    if check_output(out, 'not found'):
        raise ConnectException()
    print('VPN Successfully connected')
    return True


def check_output(out, string):
    for item in out:
        if string in item:
            return True
    return False


def print_output(out):
    for o in out:
        print('- {}'.format(o))


def connect_alias(alias):
    command = VPN_CONNECT + ' ' + str(alias)
    out = run_command(command)
    if check_output(
            out, 'We were unable to connect to this VPN location'):
        raise ConnectException()
    if check_output(out, 'not found'):
        raise ConnectException()
    print('Successfully connected to {}'.format(alias))


def extract_aliases(vpn_list):
    try:
        return extract_aliases_1(vpn_list)
    except:
        return extract_aliases_2(vpn_list)


def extract_aliases_1(vpn_list):
    """
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    """
    aliases = []
    for vpn_item in vpn_list[2:]:
        alias = vpn_item.split()[0]
        aliases.append(alias)
    return aliases


def extract_aliases_2(vpn_list):
    """
    Recommended locations:
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    """
    aliases = []
    for vpn_item in vpn_list[3:]:
        try:
            alias = vpn_item.split()[0]
            aliases.append(alias)
        except IndexError:
            return aliases
    return aliases


def random_connect():
    # activation_check()
    disconnect()
    vpn_list = run_command(VPN_LIST)[
        0:46]  # we use only US, UK, HK and JP VPN. Fastest ones!
    print_output(vpn_list)
    aliases = extract_aliases(vpn_list)
    random.shuffle(aliases)
    selected_alias = aliases[0]
    print('Selected alias : {}'.format(selected_alias))
    connect_alias(selected_alias)  # might raise a ConnectException.


if __name__ == '__main__':
    random_connect()
