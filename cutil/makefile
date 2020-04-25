TARGETNAME=cutil
DEFFILE=cutil
OUTDIR=.\chk

ALL : "$(OUTDIR)\$(TARGETNAME).dll"


"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

CPP_PROJ=\
	/MT\
	/W4\
    /EHsc\
	/Fo"$(OUTDIR)\\"\
	/Fd"$(OUTDIR)\\"\
	/c

LINK32=link.exe

LINK32_FLAGS=\
	/subsystem:windows\
	/pdb:"$(OUTDIR)\$(TARGETNAME).pdb"\
	/debug\
	/RELEASE\
	/out:"$(OUTDIR)\$(TARGETNAME).dll"\
	/DLL\
	/DEF:$(DEFFILE).def

LINK32_OBJS= \
	"$(OUTDIR)\$(TARGETNAME).obj"

"$(OUTDIR)\$(TARGETNAME).dll" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) $(LINK32_FLAGS) $(LINK32_OBJS)

.cpp{$(OUTDIR)}.obj::
   $(CPP) $(CPP_PROJ) $<