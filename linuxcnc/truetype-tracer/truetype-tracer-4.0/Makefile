CFLAGS=$(shell pkg-config --cflags freetype2) -g -Wall -std=gnu99 -O2
LIBS=$(shell pkg-config --libs freetype2) -lm

prefix ?= /usr/local

PROGS=truetype-tracer-dxf truetype-tracer

all: $(PROGS)

demos: ja.ngc hi.ngc ja.dxf hi.dxf

%.o: %.c
	gcc $(CFLAGS) -o $@ -c $<

%_dxf.o: %.c
	gcc $(CFLAGS) -DDXF -o $@ -c $<

truetype-tracer: ttt.o
	gcc -o $@ $< $(LIBS)

truetype-tracer-dxf: ttt_dxf.o
	gcc -o $@ $< $(LIBS)

install: all
	install -d $(prefix)/bin $(prefix)/share/man/man1
	cp $(PROGS) $(prefix)/bin
	cp truetype-tracer.1 $(prefix)/share/man/man1
	(cd $(prefix)/share/man/man1; ln -s truetype-tracer.1 truetype-tracer-dxf.1)

clean:
	rm -f $(PROGS) *.o *~ *~*~
	dh_clean
	rm -f build-stamp

ja.ngc: truetype-tracer
	./truetype-tracer -f /usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf -u '数値制御' > ja.ngc

hi.ngc: truetype-tracer
	./truetype-tracer hi > hi.ngc


ja.dxf: truetype-tracer-dxf
	./truetype-tracer-dxf -f /usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf -u '数値制御' > ja.dxf

hi.dxf: truetype-tracer-dxf
	./truetype-tracer-dxf hi > hi.dxf

.PHONY: all demos install clean
