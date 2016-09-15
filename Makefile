OUTPUT = target/contrib-code-toc.md

all: $(OUTPUT)

target/contrib-code-toc.md: community/contrib-code.md
	rm -f $@
	./md2toc -l 2 -h 3 $? > $@
	chmod ugo-w $@

clean:
	rm -f $(OUTPUT)

