TARGET	= libcudasim.so
LIBSRCS	= 
LIBOBJS	= cudasim.o symplectic.o

OPT	= -g -O3
PIC = -fpic
OMP   = -fopenmp
XPIC  = -Xcompiler -fpic
XOPT  = -Xptxas=-v -lineinfo #-G # only use -G for debugging / profiler
XARCH = -arch=sm_70

CXX	= nvcc
CXXFLAGS = --compiler-options "$(OPT) $(PIC) $(OMP)" $(XARCH) $(XOPT) $(XPIC)

CUDA_PATH ?= /appl/cuda/9.2
INCLUDES = -I$(CUDA_PATH)/include -I$(CUDA_PATH)/samples/common/inc

SOFLAGS = -shared
XLIBS	  = 

$(TARGET): $(LIBOBJS)
	$(CXX) -o $@ $(CXXFLAGS) $(SOFLAGS) $(INCLUDES) $^ $(XLIBS)

.SUFFIXES: .cu
.cu.o:
	$(CXX) -o $*.o -c $*.cu $(CXXFLAGS) $(SOFLAGS) $(INCLUDES) -dc

clean:
	/bin/rm -f $(TARGET) $(LIBOBJS) 
