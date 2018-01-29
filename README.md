# Binary protocol implementation for SkyTraq Venus 6 GPS over UART

Based on Application Note 0003 version 1.4.19, published on 2011-10-26 (alas, a document full of errors).

## Requirements

- Python3
- PySerial (`pip install pyserial` or `sudo apt install python3-serial`)

## TODO:

- Read the application note and finish the code. Easy, but boring.
- Write more doctests (using the examples in the application note).

## Usage:

1. Open two terminals on the computer (e.g. RPI) that is connected to the Venus.
2. Run `./interpret_messages.py` in one terminal.
3. Run one of these in the other terminal:

  - `./query.py`
  - `./configure_datum.py`
  - `./configure_update_rate.py`
  - `./turn_off_position_pinning.py`
