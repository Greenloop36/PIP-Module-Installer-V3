# PIP Module Installer (Version 3)
The third iteration of PIP Module Installer, now more robust and efficient than ever!
developed by @gl36

## Installation
1. Go to the **Releases** section of this repository, and download the latest available version
2. Extract the installed files into a suitable directory
3. Launch the `Application.py` file in this directory
    * Ensure you have **Python 3.12.x** (or any other compatible version) installed, as well as all of the built-in libraries that come with it
4. The software will automatically install its required dependencies. Once it does so, restart the software
5. The software may begin a "first-setup", complete the instructions provided there
6. The software has successfully been installed. See below for more information on its usage.

## Usage

### Installing Packages
* Use the `install` command to install a package.
 * You can specify multiple packages by separating them with a space

**Example Usage**
* `install colorama`
* `install colorama requests` (installs both of the packages)

### Removing Packages
* Use the `rm` command to uninstall a package. Does not include dependencies.
 * You can specify multiple packages by separating them with a space
 * **warning**: This command does not ask for confirmation!

**Example Usage**
* `rm colorama`
* `rm colorama requests` (removes both of the packages)

### Installing Packages to a Directory
* Use the `at` command to install a singular package to a given directory
* A directory selection dialog will appear after you run the command.

**Example Usage**
* `at colorama`


## Dependencies
Built for Windows 10/11. Not suitable for any other operating system.
The program attempts to install all of the required dependencies, but should it run into an error, you may install them manually:
* PIP (Python Package Index);
* colorama;
* requests;
* pyyaml.

## Licensing
This software is licensed under the Apache 2.0 license.
For more information, view the `LICENSE` file located in this directory, or visit https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0.

### Requests
This utility makes the use of the `requests` library, developed by Kenneth Reitz.

### Colorama
This utility makes the use of the `colorama` library, developed by Jonathan Hartley.




*Developed using Python 3.12. All rights reserved.*