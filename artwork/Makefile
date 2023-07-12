# Makefile to regenerate icon files from artwork source
#
# Primary input: /artwork/mcomix_icon_artwork.svg
#
# Primary output: /mcomix/images/mcomix.svg
#
# Secondary outputs (generated from /mcomix/images/mcomix.svg):
#   /mcomix/images/mcomix.png (212-pixel-wide bitmap)
#   /mcomix/images/$(N)x$(N)/mcomix.png ($(N)-pixel-wide bitmaps)

PNG_SIZES = 16 22 24 32 48 256
PNG_OUTPUTS := $(foreach i,$(PNG_SIZES),../mcomix/images/$(i)x$(i)/mcomix.png)

.PHONY: svg-icon png-icons all
.DEFAULT_GOAL := all

svg-icon: ../mcomix/images/mcomix.svg

../mcomix/images/mcomix.svg: mcomix_icon_artwork.svg
	inkscape -C --export-type=svg --export-plain-svg \
	--export-filename=$@ $<

define PNG_template =
  ../mcomix/images/$(1)x$(1)/mcomix.png: ../mcomix/images/mcomix.svg mcomix_icon_artwork.svg
	inkscape -C -w $(1) --export-type=png \
		--export-filename=$$@ ../mcomix/images/mcomix.svg
endef

$(foreach i,$(PNG_SIZES),$(eval $(call PNG_template,$(i))))

../mcomix/images/mcomix.png: ../mcomix/images/mcomix.svg mcomix_icon_artwork.svg
	inkscape -C -w 212 --export-type=png \
		--export-filename=$@ ../mcomix/images/mcomix.svg

png-icons: $(PNG_OUTPUTS) ../mcomix/images/mcomix.png

all: svg-icon png-icons
