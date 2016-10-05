ifndef USRBIN
  USRBIN := $(HOME)/bin
endif

PYSCRPT := qcusb.py
 
$(info echo install $(PYSCRPT) in $(USRBIN))

grid:
	-cp -p $(PYSCRPT) $(USRBIN)

