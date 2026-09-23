#!/bin/bash
# Re-creates the user-space LibreOffice used for rendering (no root). Idempotent.
set -e
cd /tmp
LO=/home/user/.cache/lo; mkdir -p $LO
if [ ! -x $LO/opt/libreoffice26.2/program/soffice ]; then
  URL=https://download.documentfoundation.org/libreoffice/stable/26.2.6/deb/x86_64/LibreOffice_26.2.6_Linux_x86-64_deb.tar.gz
  echo "downloading $URL"; curl -sSL -o lo.tgz "$URL"; ls -la lo.tgz
  mkdir -p lo_x && tar -xzf lo.tgz -C lo_x && rm lo.tgz
  for d in $(find lo_x -name '*.deb' | grep -Ev 'base|calc|writer|math|gnome|kde|qt|firebird|postgresql|mailmerge|librelogo|help|xsltfilter|pyuno|python'); do dpkg -x "$d" $LO; done
  rm -rf lo_x
fi
mkdir -p /tmp/debs && cd /tmp/debs
for spec in "libnss3 n/nss" "libnspr4 n/nspr" "libcups2t64 c/cups" "libavahi-client3 a/avahi" "libavahi-common3 a/avahi"; do
  set -- $spec
  ls ${1}_*.deb >/dev/null 2>&1 || apt-get download $1 >/dev/null 2>&1 || true
  if ! ls ${1}_*.deb >/dev/null 2>&1; then
    f=$(curl -s http://deb.debian.org/debian/pool/main/$2/ | grep -o "${1}_[^\"]*_amd64.deb" | sort -V | tail -1); echo "pool $1 -> $f"; curl -sSL -o "$f" "http://deb.debian.org/debian/pool/main/$2/$f"
  fi
done
for d in *.deb; do dpkg -x "$d" $LO; done
cat > /home/user/.cache/render.sh <<'EOS'
#!/bin/bash
# usage: ~/.cache/render.sh /abs/path/deck.pptx /abs/outdir  [pdf-filter-options-json]  -> PDF in outdir
export HOME=/home/user LD_LIBRARY_PATH=/home/user/.cache/lo/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
OPTS=${3:-'{"Quality":{"type":"long","value":"82"},"ReduceImageResolution":{"type":"boolean","value":"true"},"MaxImageResolution":{"type":"long","value":"150"}}'}
mkdir -p "$2"; timeout 900 /home/user/.cache/lo/opt/libreoffice26.2/program/soffice --headless --norestore --convert-to "pdf:impress_pdf_Export:$OPTS" --outdir "$2" "$1"
EOS
chmod +x /home/user/.cache/render.sh
echo "LO ready: $(ls $LO/opt/libreoffice26.2/program/soffice)"; du -sh $LO
