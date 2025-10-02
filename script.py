from janome.tokenizer import Tokenizer

t = Tokenizer()

def make_ruby(text):
    result = []
    for token in t.tokenize(text):
        surface = token.surface  # the word as written
        features = token.part_of_speech.split(",")
        reading = token.reading  # katakana reading (may be "*")
        if reading != "*" and surface != reading:
            # Convert katakana reading to hiragana
            hira = "".join(
                chr(ord(ch) - 0x60) if "ァ" <= ch <= "ン" else ch
                for ch in reading
            )
            result.append(f"<ruby>{surface}<rt>{hira}</rt></ruby>")
        else:
            result.append(surface)
    return "".join(result)

def convert(kanji_file, output_file="lyrics.html"):
    with open(kanji_file, encoding="utf-8") as f:
        lines = f.readlines()

    html_lines = []
    for line in lines:
        if line.strip() == "":
            html_lines.append("<br/>")
        else:
            html_lines.append(f'<span class="line">{make_ruby(line.strip())}</span>')

    template = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<title>Lyrics with Furigana</title>
<style>
body {{
  font-family: "Noto Sans JP", sans-serif;
  background: #0f172a;
  color: #e6eef8;
  padding: 40px;
  line-height: 2.2;
}}
ruby rt {{
  font-size: 0.55em;
  color: #9fb0d3;
}}
.line {{
  display:block;
  margin: 4px 0;
}}
</style>
</head>
<body>
<div class="lyrics">
{''.join(html_lines)}
</div>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"✅ Done! Output saved to {output_file}")

if __name__ == "__main__":
    convert("kanji.txt", "lyrics.html")

