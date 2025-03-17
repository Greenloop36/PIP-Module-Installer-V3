## PIP Module Installer

from colorama import Fore, Back, Style, init
from typing import Literal, TypedDict
import subprocess
import os
from ..libraries import output as out

# Types
ErrorList = TypedDict("TypedDict", {"Package": str, "Result": subprocess.CompletedProcess})

## Methods
def StatusOut(Action: Literal["message", "OK", "FAIL"] = "message", Message: str = None, Prefix: str = "\t| ") -> None:
    if Action == "message":
        print(f"{Prefix}[ {Style.DIM}..{Style.RESET_ALL} ] {Message}", end = "\r", flush = True)
    else:
        if Action == "OK":
            print(f"{Prefix}[ {Fore.GREEN}OK{Fore.RESET} ]")
        else:
            print(f"{Prefix}[{Fore.LIGHTRED_EX}FAIL{Fore.RESET}]")

def InstallationAction(Packages: list[str], args: list[str], Message: str, SuffixArgs: list[str] = []):
    AMOUNT: int = len(Packages)
    ERRORS: ErrorList = {}
    ERROR_COUNT: int = 0

    if AMOUNT == 1:
        print(f"{Message}ing {Fore.LIGHTBLUE_EX}1{Fore.RESET} package:")
    else:
        print(f"{Message}ing {Fore.LIGHTBLUE_EX}{AMOUNT}{Fore.RESET} packages:")

    ## Installation
    for Name in Packages:
        COMMAND = ["pip", "--no-python-version-warning", *args, Name, *SuffixArgs]
        out.debug(str(COMMAND), f"InstallationAction: {Message.lower()}")
        StatusOut(Message=f"{Message.lower()}ing {Fore.LIGHTCYAN_EX}{Name}{Fore.RESET}...")

        RESULT: subprocess.CompletedProcess = subprocess.run(
            COMMAND, 
            capture_output=True,
            shell=True
            )

        if RESULT.returncode == 0:
            StatusOut("OK")
        else:
            StatusOut("FAIL")
            ERRORS[ERROR_COUNT] = {
                "Package": Name,
                "Result": RESULT
            }

            ERROR_COUNT += 1
    
    print()
    
    ## Check errors
    ERROR_COUNT = len(ERRORS)
    if ERROR_COUNT > 0:
        if ERROR_COUNT == 1:
            out.warn(f"{Message.lower()}ation of 1 package failed!")
        else:
            out.warn(f"{Message.lower()}ation of {ERROR_COUNT} packages failed!")
    
        for Index, Result in ERRORS.items():
            print(f"\t| Failed to {Message} \"{Fore.LIGHTCYAN_EX}{str(Result['Package'])}{Fore.RESET}\":")
            out.debug(Result["Result"].stderr.decode("utf-8"), f"InstallationAction: error")
            out.debug(Result["Result"].returncode, f"InstallationAction: error")
            
            # if Index != ERROR_COUNT: print()
    else:
        if AMOUNT == 1:
            out.success(f"{Message}ed 1 package.")
        else:
            out.success(f"{Message}ed {AMOUNT} packages.")

def install(Packages: list[str]):
    InstallationAction(Packages, ["install"], "Install")

def remove(Packages: list[str]):
    InstallationAction(Packages, ["uninstall", "--yes"], "Uninstall")

def install_to(Package: str, Path: str):
    InstallationAction([Package], ["install"], "Install", [f"-t", Path])


## Runtime
def main():
    init(True)
    install(["requests", "colorama"])

if __name__ == "__main__": main()