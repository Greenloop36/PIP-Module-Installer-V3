## Init
from internal.runtime.init import main as ProgramInit
import sys
import os
if not ("!noinit" in sys.argv):
    if ProgramInit() != True:
        input("Init failed. Press RETURN to exit.")
        sys.exit(1)
else:
    os.system("cls")
    print("starting...")

os.chdir("C:/")


## Configuration
USR_DATA_TEMPLATE = {}
DIR = os.path.dirname(__file__)

## Imports
import colorama
from colorama import Fore, Back, Style
import json
import yaml
import ctypes
import ast

from tkinter import filedialog

from internal.libraries.utils import UserInput
import internal.runtime.update as update
import internal.libraries.output as out
import internal.runtime.installer as installer

## Core Methods
def GetFile(*args) -> tuple[bool, str]:
    PATH = DIR
    EXISTS = False

    for i in args:
        PATH = f"{PATH}\\{i}"
    
    EXISTS = os.path.exists(PATH)

    return EXISTS, PATH

def EnsureFile(*PATH, ReturnStream: bool = False):
    FILE_EXISTS, FILE = GetFile(*PATH)

    if FILE_EXISTS:
        if ReturnStream:
            return open(FILE)
        else:
            with open(FILE, "r") as Target:
                return Target.read()
    else:
        PATH_DIR = os.path.dirname(FILE)

        if not os.path.exists(PATH_DIR):
            os.makedirs(PATH_DIR)
        
        open(FILE, "x")

        return EnsureFile(*PATH)

## Variables
Login = os.getlogin() # notice: this just gets your local username (to be displayed in the input prefix)
DataFile = GetFile("internal", "persistent", "UserData.json")
Configuration = yaml.safe_load(EnsureFile("internal", "data", "Configuration.yaml", ReturnStream=True))
## Functions
    
# Out
def toggle_console(visible):
    console_window = ctypes.windll.kernel32.GetConsoleWindow()
    if console_window:
        ctypes.windll.user32.ShowWindow(console_window, 1 if visible else 0)      

def ClearWindow():
    os.system("cls")

## Data
def Data_Get() -> dict:
    File = EnsureFile("internal", "persistent", "UserData.json", ReturnStream=True)

    # with open(DataFile_Path, "r") as File:
    DATA = File.read()

    try: DATA = json.loads(DATA)
    except:
        DATA = {}
    finally:
        return DATA

def Data_Write(Data: dict) -> bool:
    DataFile_Exists, DataFile_Path = GetFile("internal", "persistent", "UserData.json")
    if not DataFile_Exists: return False

    try:
        with open(DataFile_Path, "w") as File:
            File.write(json.dumps(Data))
    except Exception as e:
        print(f"[Data_Set]: failed because \"{e}\"!")
        return False
    else:
        return True

# Other
def init():
    colorama.init()

def IsUserDataValid(Data: dict) -> bool:
    VALID = True

    for Key, Value in USR_DATA_TEMPLATE:
        if not Key in Data:
            VALID = False
    
    return VALID

def GetInputPrefix(Process: str = "Main", Instruction: str = None) -> str:
    if Instruction != None:
        Instruction = f"{Fore.RESET}: {Fore.LIGHTBLUE_EX}{Instruction}\n{Fore.BLUE}> {Fore.RESET}"
    else:
        Instruction = f"\n{Fore.MAGENTA}$ {Fore.RESET}"

    Name: str = Configuration['ProgramName'].lower()
    Name = Name.replace(" ", "-")

    return f"\n{Fore.GREEN}{Login}@{Name}{Fore.RESET} {Style.DIM}~{Style.RESET_ALL} {Fore.YELLOW}{Process}{Instruction}"

def Pause():
    os.system("pause")

def Quit(Message: str | None = None):
    if Message:
        out.exception(f"\n{Message}")
        print("\n\nThe program will now exit.")
        Pause()
        sys.exit(0)
    else:
        out.exception("\nQuitting...")
        sys.exit(0)

def FirstSetup():
    try:
        Data = USR_DATA_TEMPLATE

        ClearWindow()
        out.notice("Performing first time setup:\nControl+C to skip\n\n")
        
        for Key in Data.keys():
            RESULT = input(GetInputPrefix("Setup", f"{Key}:"))
            Data[Key] = RESULT
        

        Success = Data_Write(Data)
        if not Success:
            out.warn("Failed to save data")
            Pause()

        ClearWindow()
    except KeyboardInterrupt:
        print()
        out.warn("Some functionality may be limited, as setup is incomplete.")
        Pause()

        pass
    except Exception as e:
        print()
        out.traceback(e)
        Quit(f"Fatal error during setup!")

## Command Util Functions
def can_cast(value, type_name):
    # Map type names to their corresponding types
    type_map = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        # Add more types as needed
    }

    # Get the type from the type_map
    if type_name not in type_map:
        raise ValueError(f"Unsupported type: {type_name}")

    target_type = type_map[type_name]

    try:
        # Special handling for boolean since bool('False') returns True
        if target_type is bool:
            if value.lower() in ('true', 'false', 't', 'f', 'yes', 'no', 'y', 'n', '1', '0'):
                # Convert to the appropriate boolean value
                new_value = value.lower() in ('true', 't', 'yes', 'y', '1')
                return True, new_value, 'bool'
            else:
                return False, None, "unknown-type"

        # Attempt to convert the value to the target type
        if target_type is list or target_type is tuple or target_type is set:
            # Use ast.literal_eval for safe evaluation of strings representing containers
            parsed_value = ast.literal_eval(value)
            if isinstance(parsed_value, target_type):
                return True, parsed_value, type_name
            else:
                return False, None, "unknown-type"
        else:
            # For other types, try direct conversion
            new_value = target_type(value)
            return True, new_value, type_name
    except (ValueError, SyntaxError):
        return False, None, "unknown-type"

def EvaluateArgs(Query: str, *args) -> tuple[bool, str | list]:
    """
    
        Converts a query into a proper, typed, list of arguments.
        The arguments are specified after the Query, as individual parameters in the function.
        Arguments are formatted as "name:type".
        Add a question mark at the end of an argument's name for it to be optional.
        Strings should be kept till the end, so they're not cut off.

        Examples:
            ("12 hi", "Duration:int", "Reason:str") -> True, [12, "hi"]
            ("hi 12", "Duration:int", "Reason:str") -> False "Malformed argument #1, Duration: expected int, instead got str", 

        Returns tuple:
            success: bool, (whether the query is valid)
            result: str | list (an error message, if invalid (success == False), OR the formatted list of arguments)

    """

    if Query == None:
        return False, "No arguments provided!"

    PARSED_QUERY = Query.split(" ", len(args) - 1)
    RESULT = []

    for Argument in args:
        Argument: str = Argument
        Index: int = args.index(Argument)
        ARG = Argument.split(":")
        NAME = ARG[0]
        TYPE = ARG[1]

        # print(f"{ARGVALUE = }, {Index = }, {ARG =}, {NAME = }, {TYPE = }")

        if not NAME.endswith("?"):
            try: PARSED_QUERY[Index]
            except: return False, f"Missing required argument #{Index + 1}, \"{NAME}\": {TYPE}"
        else:
            try: PARSED_QUERY[Index]
            except:
                RESULT.append(None)

                continue
        ARGVALUE = PARSED_QUERY[Index]

        CAST_POSSIBLE, CASTED, _ORIGINAL_TYPE = can_cast(ARGVALUE, TYPE)
        # print(CAST_POSSIBLE, CASTED, _ORIGINAL_TYPE)

        if not CAST_POSSIBLE:
            return False, f"Malformed argument #{Index}, \"{NAME}\": expected {TYPE}, instead got {_ORIGINAL_TYPE}"
        else:
            RESULT.append(CASTED)
    
    return True, RESULT

## Commands
class Commands:

    ## Core/Built-in Commands
    def exit(*_):
        """
        Quits the application. Control+C also does this.
        """
        Quit()

    def update(*_):
        """
        Update to the latest available version, or repair your installation.
        """
        if Configuration["GitHub"] == False:
            return out.error("Not connected to any repository!")
        else:
            print("Preparing to update...")
            Latest = update.GetLatestVersionCode()
            
            if Latest == Configuration["ThisVersion"]:
                print(f"You are already using the latest version, {Fore.GREEN}{Latest}{Fore.RESET}.")
            else:
                print(f"You are about to upgrade to the latest version, {Fore.GREEN}{Latest}{Fore.RESET}.")
            
            if UserInput.YesNo("Continue to update?"):
                update.Update(DIR)
    
    def clear(*_):
        """
        Clears the interface.
        """
        ClearWindow()

    def help(*args):
        """
            Displays a list of commands, or information about those commands.

            Arguments:
                - CommandName: str?
        """

        ## Variables
        SUCCESS, ARGS = EvaluateArgs(args[0], "CommandName?:str")
        # print(f"{SUCCESS = }")
        # print(f"{ARGS = }")
        CommandName = ARGS[0] or None

        ## Command
        if not SUCCESS:
            print("This command is used to get information about other commands. Below is a list of all commands.\nYou can use \"help <command>\" to view more information about a specific command.")
            ToPrint = [attr for attr in dir(Commands) if callable(getattr(Commands, attr)) and not attr.startswith("__")]

            for Command in ToPrint:
                print(f"\t| {Command}")
        else:
            try: Command = getattr(Commands, CommandName)
            except: return out.error("This command doesn't exist.")

            if not callable(Command):
                return out.error("This command doesn't exist.")
            else:
                if Command.__doc__:
                    HELP: str = Command.__doc__
                    # HELP = HELP.replace("    ", "")
                    return HELP
                else:
                    return "There is no information for this command."
    
    ## Custom Commands
    def install(*args):
        """
        Installs the packages provided.

        Arguments:
            - PackageList: str
        """

        ## Variables
        SUCCESS, ARGS = EvaluateArgs(args[0], "PackageList:str")
        if not SUCCESS: return out.exception(ARGS)

        PackageList: str = ARGS[0]

        ## Install
        installer.install(PackageList.split(" "))
    
    def at(*args):
        """
        Install the package specified to a given directory.

        Arguments:
            - Package: str
        """

        ## Variables
        SUCCESS, ARGS = EvaluateArgs(args[0], "Package:str")
        if not SUCCESS: return out.exception(ARGS)

        Package: str = ARGS[0]

        try:
            PATH = filedialog.askdirectory(initialdir=DIR, title="Select where to install the package")
        except KeyboardInterrupt:
            return
        else:
            out.debug(f"{PATH = }")
            if PATH == "":
                return out.error("No directory was given!")

        ## Install
        installer.install_to(Package, PATH.replace("\\", "/"))
    
    def rm(*args):
        """
        Removes the packages provided.

        Arguments:
            - PackageList: str
        """

        ## Variables
        SUCCESS, ARGS = EvaluateArgs(args[0], "PackageList:str")
        if not SUCCESS: return out.exception(ARGS)

        PackageList: str = ARGS[0]

        ## Install
        installer.remove(PackageList.split(" "))
    
    def verbose(*args):
        """
        Enable verbose output. Toggled if no argument is given.

        Arguments:
            - Enable?: boolean
        """

        ## Variables
        SUCCESS, ARGS = EvaluateArgs(args[0], "Enable?:bool")
        if not SUCCESS: ARGS = [None]

        Flag: str = ARGS[0] or None

        if out.set_debug_flag(Flag) == True:
            out.info("Verbose output enabled")
        else:
            out.info("Verbose output disabled")

## Runtime

def main():
    SHOULD_UPDATE = False

    ## Init user data
    UserData = Data_Get()

    if not IsUserDataValid(UserData):
        FirstSetup()
        UserData = Data_Get()
        
    ## Greeting
    ClearWindow()
    print(f"{Configuration['ProgramName']} [Version {Configuration['ThisVersion']}]")
    print(f"Control+C to exit\n")

    ## Ensure that file version code & current version code (stored in Configuration) are the same
    try:
        Ver = EnsureFile("internal", "data", "VERSION.txt")

        FileVer = Ver.replace("\n", "")
        if FileVer != Configuration['ThisVersion']:
            out.warn(f"Mismatch between program version and file version! {Configuration['ThisVersion'] = } != {FileVer = }")
    except Exception as e:
        out.warn(f"Failed to read VERSION file: {e}")
    
    ## Check for updates
    if Configuration["GitHub"]:
        LatestVer = update.GetLatestVersionCode()

        if Configuration['ThisVersion'] != LatestVer and LatestVer != None:
            SHOULD_UPDATE = True
        elif LatestVer == None:
            out.warn("Failed to get latest update! Please check your internet connection.")

    ## ADD MISCELLANEOUS ITEMS HERE

    ## Main loop
    if SHOULD_UPDATE:
        out.notice(f"An update is available! Run \"update\" to install it. ({Fore.LIGHTRED_EX}{Configuration['ThisVersion']}{Fore.RESET} -> {Fore.LIGHTGREEN_EX}{LatestVer}{Fore.RESET})")
    
    while True:
        try:
            QUERY = input(GetInputPrefix())
        except KeyboardInterrupt:
            print()
            Quit()
        else:
            VALID, COMMAND, ARGS = UserInput.ParseCommandInput(QUERY)
            # print(VALID, COMMAND, ARGS)
            
            if VALID:
                METHOD = getattr(Commands, COMMAND, None)

                if not METHOD or not callable(METHOD):
                    out.exception(f"\"{COMMAND}\" is not recognised as an internal command.")
                    continue

                try:
                    RESULT = METHOD(ARGS)
                except Exception as e:
                    out.exception(f"An exception occured whilst running the command, {COMMAND}!")
                    out.traceback(e)
                else:
                    if RESULT != None:
                        print(RESULT)
    

if __name__ == "__main__":
    CatchErrors = True ## Debug flag

    if CatchErrors:
        try:
            main()
        except KeyboardInterrupt:
            Quit()
        except EOFError:
            Quit()
        except Exception as e:
            if e == "" or e == None:
                e = "Unknown exception"

            out.exception(f"\nA fatal error ocurred during runtime! The program will now exit. See details below.")
            out.traceback(e)
            Pause()
    else:
        ClearWindow()
        Warning("Errors will be uncaught!\n")
        Pause()
        main()
    