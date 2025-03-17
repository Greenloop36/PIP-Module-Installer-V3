## Coloured Output

from colorama import Fore, Back, Style, init
import traceback as tb

__DEBUG_ENABLE = False
__DEMOTEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam posuere."

__all__ = ["error", "success", "notice", "warn", "exception", "traceback", "info", "init", "critical"]

## Methods
def _CreatePrefix(Prefix: str = None):
    if Prefix != None:
        Prefix = f" {Style.BRIGHT}{Fore.WHITE}{Back.BLUE} {Prefix} {Style.RESET_ALL} "
    else:
        Prefix = " "
    return Prefix

def debug(Message: str, Prefix: str = None):
    if not __DEBUG_ENABLE: return False
    print(f"{Style.BRIGHT}{Fore.CYAN}debug{Style.RESET_ALL}:{_CreatePrefix(Prefix)}{Message}")

def info(Message: str, Prefix: str = None):
    print(f"{Style.BRIGHT}{Fore.BLUE}info{Style.RESET_ALL}:{_CreatePrefix(Prefix)}{Message}")

def error(Message: str, Prefix: str = None):
    print(f"{Style.BRIGHT}{Fore.RED}error{Style.RESET_ALL}:{_CreatePrefix(Prefix)}{Message}")
    # print(Style.BRIGHT + Fore.RED + "error" + Style.RESET_ALL + ": " + str(Message))

def success(Message: str, Prefix: str = None):
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}success{Style.RESET_ALL}:{_CreatePrefix(Prefix)}{Message}")
    # print(Fore.LIGHTGREEN_EX + "success" + Fore.RESET + ": " + str(Message))

def notice(Message: str, Prefix: str = None):
    print(f"{Style.BRIGHT}{Fore.MAGENTA}notice{Style.RESET_ALL}:{_CreatePrefix(Prefix)}{Message}")
    # print(Style.BRIGHT + Fore.MAGENTA + "notice" + Style.RESET_ALL + ": " + str(Message))

def warn(Message: str, Prefix: str = None):
    print(f"{Style.BRIGHT}{Fore.YELLOW}warning{Style.RESET_ALL}:{_CreatePrefix(Prefix)}{Message}")

def critical(Message: str, Prefix: str = None):
    print(f"{Style.BRIGHT}{Back.RED}{Fore.WHITE} ! {Style.RESET_ALL} {Fore.LIGHTRED_EX}CRITICAL{Fore.RED}:{_CreatePrefix(Prefix)}{Message}")

def exception(Message: str):
    print(Fore.LIGHTRED_EX + str(Message) + Fore.RESET)

def traceback(e):
    Name = type(e).__name__

    print(f"\n{Style.BRIGHT}{Fore.WHITE}{Back.RED} {Name} {Back.RESET}{Fore.RED}: {str(e)}{Style.RESET_ALL}")
    print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}Stack begin{Style.NORMAL}{Fore.LIGHTBLUE_EX}\n{tb.format_exc()}{Fore.LIGHTCYAN_EX}{Style.BRIGHT}Stack end{Style.RESET_ALL}\n")

def set_debug_flag(Flag: bool = None):
    global __DEBUG_ENABLE
    if Flag == None: Flag = not __DEBUG_ENABLE

    __DEBUG_ENABLE = Flag
    
    return __DEBUG_ENABLE

## Demo
def __demonstration():
    info(__DEMOTEXT)
    error(__DEMOTEXT)
    success(__DEMOTEXT)
    notice(__DEMOTEXT)
    warn(__DEMOTEXT)
    exception(__DEMOTEXT)
    critical(__DEMOTEXT)
    debug(__DEMOTEXT)

    notice(__DEMOTEXT, "meow")

    try:
        int(__DEMOTEXT)
    except Exception as e:
        traceback(e)


if __name__ == "__main__":
    from time import sleep
    init(True)
    __demonstration()
    sleep(5)