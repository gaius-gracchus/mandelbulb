F2=f2py
F90FLAGS=-fopenmp
F2FLAGS= --f90flags="$(F90FLAGS)" -lgomp

mandelpow: mandelpow.f90
	$(F2) -c $(F2FLAGS) -m $@ $<

.PHONY: clean

clean:
	rm -f *.so