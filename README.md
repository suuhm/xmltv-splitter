# xmltv-splitter
tool to filter an XMLTV EPG file by specific channels. Ideal for use with TVHeadend, Plex, or any XMLTV-compatible app

**XMLTV Splitter** is a lightweight Python script that filters large XMLTV EPG files down to only the channels you care about — by name or from a remote source.

---

## ✅ Features

- Filter EPG data for specific channels by display name
- Accepts input from a local file or remote URL
- Automatically removes broken `stop="19700101..."` entries
- Fixes common character encoding issues (Latin-1 interpreted as UTF-8)
- Outputs clean, valid XMLTV for use with TVHeadend, Plex, etc.

---

## 📦 Requirements

- Python 3.6+
- `lxml` library

Install via pip:

```bash
pip install lxml
````

---

## 🚀 Usage

### From a local file:

```bash
python3 xmltv-splitter.py \
  --input epg.xml \
  --output epg_filtered.xml \
  --channels RTL,ProSieben,ProSieben Maxx
```

### From a remote URL:

```bash
python3 xmltv-splitter.py \
  --url-extern https://example.com/guide.xml \
  --output epg_filtered.xml \
  --channels RTL,ProSieben
```

## Import to TVHeadend EPG XMLTV Grabber

```bash
cat epg_filtered.xml | socat - UNIX-CONNECT:/etc/tvheadend/epggrab/xmltv.sock
```

---

## 📂 Arguments

| Option         | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| `--input`      | Path to local XMLTV input file *(optional if `--url-extern`)* |
| `--url-extern` | URL to download XMLTV file *(optional if `--input` used)*     |
| `--output`     | Path to save the filtered XMLTV result                        |
| `--channels`   | Comma-separated list of display names to include              |

---

## 🧹 Post-processing

Filtered XMLTV output will:

* Contain only matching `<channel>` and `<programme>` entries
* Remove broken stop-times (`1970-01-01`)
* Normalize character encodings (fix `GÃ¼nther` → `Günther`)

---

## 📜 License

MIT License. Use at your own risk.

---

## 💡 Contributions

Feel free to submit pull requests or open issues!
