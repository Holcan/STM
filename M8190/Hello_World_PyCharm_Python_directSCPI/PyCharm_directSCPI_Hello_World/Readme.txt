RsInstrument is a Python module that provides convenient way of communicating with R&S instruments over VISA
It uses PyVisa to build instrument model layer that provides all the required tasks you might need when remote-controlling your instrument:

- Initializing a new session with setting all the required VISA and instrument registers depending on the session type
- Identification of the instrument, supported models, evaluation of the instrument options
- Special actions, e.g. Self-test, reset
- Typical text communication - Write / Query / Query<type>
- OPC-synchronised actions - Write / Query with OPC. The synchronization mechanism can be: Status byte polling / *OPC? query, Service Request
- Asynchronous events-driven OPC-synchronised actions. After the instrument has finished the operation, a registered event handler is invoked
- Binary data transfer - Write / Query bin data
- Transfer of files between PC and Instrument, the size is unlimited
- Binary or ASCII arrays transfers - adaptable querying of float / double / integer arrays
	The response is processed correctly regardless whether it arrives as binary data or ASCII data
- Instrument status checking (SYSTem:ERRor?) after each command. This can be switched OFF if desired
- Optional feature of sending (*OPC?) after each Write command
- Sharing of the already openeed session with another RsInstrument instance, so the physical VISA session is still only one
- Generating events if:
	- controller sends data
	- instrument returns data
	- big transferred data (write or read) are split into segments. This allows for showing the transfer progress,
		or in case of read operation processing partial data without having to wait for the complete response.
	
------------------------------------------------------------------------------------------------------------------------------------------------------

Requirements:
- Python 3.7 or newer
- R&S Visa 5.12.3 + or any other Visa installation

------------------------------------------------------------------------------------------------------------------------------------------------------
Installation:

RsInstrument is hosted on pypi.org. You can install it with pip.exe (Windows), or if you are using Pycharm direct in the Pycharm packet management GUI

Option 1: Install using pip.exe:
- Start the command console: WinKey + R, type cmd and hit ENTER
- Change the working directory to your instaled Python (adjust the user name and python version in the path):
	cd c:\Users\John\AppData\Local\Programs\Python\Python37\Scripts
- install RsInstrument with the command: pip install Rsinstrument

Option 2: Install in Pycharm:
- In Pycharm Menu File->Settings->Project->Project Interpreter click on the '+' button on the top right
- Type 'rsinstrument' in the search box
- Install the version 1.2.0.25 or newer
- If you are behind a Proxy server, configure it in Menu File->Settings->Appearance->System Settings->HTTP Proxy

For more details check our Instrument remote control Getting started page:
https://www.rohde-schwarz.com/driver-pages/remote-control/getting-started_231558.html

------------------------------------------------------------------------------------------------------------------------------------------------------

Version history:

Version 1.2.0.25 (03.08.2020)
- Fixed reading of long strings for NRP-Zxx sessions

Version 1.1.0.24 (16.06.2020)
- Fixed simulation mode switching
- Added Repeated capability

Version 1.0.0.21
- First released version