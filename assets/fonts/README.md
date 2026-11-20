# Embedded font subsets

`archivo-800.woff2` and `dmmono-400.woff2` are printable-ASCII subsets of
[Archivo](https://github.com/Omnibus-Type/Archivo) 800 and
[DM Mono](https://github.com/googlefonts/dm-mono) 400. They are embedded as
data URIs inside `assets/hero.svg` so the nameplate keeps its typography when
GitHub serves the image through its Camo proxy. Browsers block external
resources inside SVG images, so the fonts have to travel with the file.

Both families are licensed under the SIL Open Font License 1.1. The license
text is kept beside the subsets as `OFL-Archivo.txt` and `OFL-DMMono.txt`.

## Rebuilding a subset

Download the static TTF from Google Fonts, then:

```sh
python -m fontTools.subset archivo-800.ttf \
  --unicodes=U+0020-007E \
  --layout-features='*' \
  --flavor=woff2 \
  --output-file=assets/fonts/archivo-800.woff2
```

The same command works for `dmmono-400.ttf`. Subsetting needs `fonttools` and
`brotli` locally; the profile build itself only uses the Python standard
library.
