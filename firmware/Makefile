# Arduino 1.0 Makefile
#
# Based on Makefile by Kerry Wong http://www.kerrywong.com
# Arduino adaptation by mellis, eighthave, oli.keller


# Change this to match your arduino installation directory
INSTALL_DIR        = /home/dkobozev/lib/arduino
PORT               = /dev/ttyUSB0
UPLOAD_RATE        = 57600
AVRDUDE_PROGRAMMER = stk500v1
MCU                = atmega328p
F_CPU              = 16000000

VERSION        = 1.0
ARDUINO        = $(INSTALL_DIR)/hardware/arduino/cores/arduino
VARIANTS       = $(INSTALL_DIR)/hardware/arduino/variants/standard
ARDUINO_LIB    = $(INSTALL_DIR)/libraries
AVR_TOOLS_PATH = /usr/bin
AVRDUDE_PATH   = /usr/bin
AVRDUDE_CONF   = /etc/avrdude.conf

# Note that if your program has dependencies other than those
# already listed below, you will need to add them accordingly.
C_MODULES =  \
$(ARDUINO)/wiring_pulse.c \
$(ARDUINO)/wiring_analog.c \
$(ARDUINO)/wiring.c \
$(ARDUINO)/wiring_digital.c \
$(ARDUINO)/WInterrupts.c \
$(ARDUINO)/wiring_shift.c \

CXX_MODULES = \
$(ARDUINO)/Tone.cpp \
$(ARDUINO)/Print.cpp \
$(ARDUINO)/HardwareSerial.cpp \
$(ARDUINO)/CDC.cpp \
$(ARDUINO)/HID.cpp \
$(ARDUINO)/IPAddress.cpp \
$(ARDUINO)/new.cpp \
$(ARDUINO)/Stream.cpp \
$(ARDUINO)/USBCore.cpp \
$(ARDUINO)/WMath.cpp \
$(ARDUINO)/WString.cpp \
$(ARDUINO)/main.cpp \
$(ARDUINO_LIB)/EEPROM/EEPROM.cpp \
$(ARDUINO_LIB)/Servo/Servo.cpp \
leg.cpp \

SRC     = $(C_MODULES)
CXX_SRC = $(CXX_MODULES) main.cpp
FORMAT  = ihex

# -----------------------------------------------------------------------------
# COMPILER FLAGS
# -----------------------------------------------------------------------------

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
#DEBUG = stabs
DEBUG =

OPT = s

# Place -D or -U options here
CDEFS   = -DF_CPU=$(F_CPU)L -DARDUINO=$(VERSION)
CXXDEFS = -DF_CPU=$(F_CPU)L -DARDUINO=$(VERSION)

# Place -I options here
CINCS   = -I$(ARDUINO) -I$(VARIANTS) -I$(ARDUINO_LIB)
CXXINCS = -I$(ARDUINO) -I$(VARIANTS) -I$(ARDUINO_LIB)

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
#CSTANDARD = -std=gnu99

CDEBUG = -g$(DEBUG)

CWARN = -Wall #-Wstrict-prototypes
#CWARN = -w #suppress all warnings

#CTUNING = -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums
CTUNING = -ffunction-sections -fdata-sections
CXXTUNING = -fno-exceptions -ffunction-sections -fdata-sections

#CEXTRA = -Wa,-adhlns=$(<:.c=.lst)

CFLAGS   = $(CDEBUG) -O$(OPT) $(CWARN) $(CTUNING) $(CDEFS) $(CINCS) $(CSTANDARD) $(CEXTRA)
CXXFLAGS = $(CDEBUG) -O$(OPT) $(CWARN) $(CXXTUNING) $(CDEFS) $(CINCS)

#ASFLAGS = -Wa,-adhlns=$(<:.S=.lst),-gstabs

LDFLAGS = -O$(OPT) -Wl,--gc-sections

ALL_CFLAGS   = $(CFLAGS)   -mmcu=$(MCU)
ALL_CXXFLAGS = $(CXXFLAGS) -mmcu=$(MCU)
ALL_ASFLAGS  = -x assembler-with-cpp $(ASFLAGS) -mmcu=$(MCU)
ALL_LDFLAGS  = $(LDFLAGS)  -mmcu=$(MCU)

OBJS     = $(SRC:.c=.o)
OBJS_CXX = $(CXX_SRC:.cpp=.o)
OBJS_ALL = $(OBJS) $(OBJS_CXX)

# -----------------------------------------------------------------------------
# AVR
# -----------------------------------------------------------------------------

AVRDUDE_PORT  = $(PORT)
AVRDUDE_FLAGS = -V -F -C $(AVRDUDE_CONF) \
-p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) \
-b $(UPLOAD_RATE) -D

CC      = $(AVR_TOOLS_PATH)/avr-gcc
CXX     = $(AVR_TOOLS_PATH)/avr-g++
LD      = $(AVR_TOOLS_PATH)/avr-gcc
OBJCOPY = $(AVR_TOOLS_PATH)/avr-objcopy
OBJDUMP = $(AVR_TOOLS_PATH)/avr-objdump
AR      = $(AVR_TOOLS_PATH)/avr-ar
SIZE    = $(AVR_TOOLS_PATH)/avr-size
NM      = $(AVR_TOOLS_PATH)/avr-nm
AVRDUDE = $(AVRDUDE_PATH)/avrdude

REMOVE = rm -f
MV     = mv -f

# auto-reset
RESET_DEVICE = stty -F $(PORT) hupcl

# flash size
HEXSIZE = $(SIZE) --target=$(FORMAT) main.hex

# -----------------------------------------------------------------------------
# RULES
# -----------------------------------------------------------------------------

.PHONY: all build clean upload size

# default target
all: build size

build: main.elf main.hex

main.elf: $(OBJS) $(OBJS_CXX)
	$(LD) -lc -lm $(ALL_LDFLAGS) -o $@ $^ -lc

$(OBJS): %.o: %.c
	$(CC) -c $(ALL_CFLAGS) $< -o $@

$(OBJS_CXX): %.o: %.cpp
	$(CXX) -c $(ALL_CXXFLAGS) $< -o $@

main.hex: main.elf
	$(OBJCOPY) -O $(FORMAT) -R .eeprom $< $@

clean:
	$(RM) $(OBJS)
	$(RM) $(OBJS_CXX)
	$(RM) main.elf main.hex
	$(RM) dependencies dependencies_cxx

upload: main.hex
	$(RESET_DEVICE)
	$(AVRDUDE) $(AVRDUDE_FLAGS) -U flash:w:main.hex

size:
	@if [ -f main.elf ]; then $(HEXSIZE); fi

# generate header file dependencies
dependencies: $(SRC)
	$(CC) -M $(ALL_CFLAGS) $^ > $@

dependencies_cxx: $(CXX_SRC)
	$(CXX) -M $(ALL_CXXFLAGS) $^ > $@

include dependencies dependencies_cxx
