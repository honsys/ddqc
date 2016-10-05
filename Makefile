ifndef USRBIN
  USRBIN := $(HOME)/bin
endif

PYSCRPT := qcusb.py
 
$(info echo install $(PYSCRPT) in $(USRBIN) ... your PATH should include $(USRBIN))

grid:
	-cp -p $(PYSCRPT) $(USRBIN)

