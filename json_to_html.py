import argparse
import datetime as dt
import html
import json
from pathlib import Path


def _safe_text(value):
    if value is None:
        return ""
    return html.escape(str(value))


def _parse_time(value):
    if not value:
        return None
    try:
        # Handles RFC3339 like "2025-07-13T19:37:00+08:00"
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def render_html(data, title):
    moments = data.get("Moments", [])

    rows = []
    for idx, m in enumerate(moments, start=1):
        content = _safe_text(m.get("content", ""))
        time_text = _safe_text(m.get("timeText", ""))
        timestamp = m.get("timestamp", "")
        ts = _parse_time(timestamp)
        ts_text = _safe_text(ts.isoformat()) if ts else _safe_text(timestamp)
        sender = _safe_text(m.get("senderQQ", ""))
        likes = _safe_text(m.get("likes", 0))
        views = _safe_text(m.get("views", 0))
        deleted = "Yes" if m.get("isDeleted") else "No"
        reconstructed = "Yes" if m.get("isReconstructed") else "No"

        images = m.get("imageURLs") or []
        img_tags = []
        for url in images:
            if not url:
                continue
            safe_url = html.escape(str(url), quote=True)
            img_tags.append(
                f'<img loading="lazy" src="{safe_url}" alt="image" />'
            )
        imgs_html = "\n".join(img_tags) if img_tags else ""

        rows.append(
            f"""
            <article class="moment">
              <div class="meta">
                <span class="idx">#{idx}</span>
                <span class="sender">senderQQ: {sender}</span>
                <span class="time">{time_text}</span>
                <span class="timestamp">{ts_text}</span>
              </div>
              <div class="content">{content or "<em>(empty)</em>"}</div>
              {"<div class='images'>" + imgs_html + "</div>" if imgs_html else ""}
              <div class="stats">
                <span>likes: {likes}</span>
                <span>views: {views}</span>
                <span>deleted: {deleted}</span>
                <span>reconstructed: {reconstructed}</span>
              </div>
            </article>
            """
        )

    body = "\n".join(rows)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_safe_text(title)}</title>
  <style>
    :root {{
      --bg: #f6f2ea;
      --card: #ffffff;
      --text: #1f2328;
      --muted: #667085;
      --border: #e6e1d8;
      --accent: #0f766e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Noto Serif SC", "Source Han Serif SC", "PingFang SC",
        "Microsoft YaHei", serif;
      background: linear-gradient(180deg, #fbf8f2 0%, #f1e9dd 100%);
      color: var(--text);
    }}
    header {{
      padding: 28px 20px 10px;
      text-align: center;
    }}
    header h1 {{
      margin: 0 0 6px;
      font-size: 24px;
      letter-spacing: 0.5px;
    }}
    header p {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 20px;
      display: grid;
      gap: 14px;
    }}
    .moment {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 1px 0 rgba(0,0,0,0.03);
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px 12px;
      font-size: 12px;
      color: var(--muted);
    }}
    .idx {{
      color: var(--accent);
      font-weight: 600;
    }}
    .content {{
      margin-top: 10px;
      font-size: 16px;
      line-height: 1.6;
      white-space: pre-wrap;
    }}
    .images {{
      margin-top: 12px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 8px;
    }}
    .images img {{
      width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    .stats {{
      margin-top: 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px 16px;
      font-size: 12px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <header>
    <h1>{_safe_text(title)}</h1>
    <p>导出时间: {_safe_text(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</p>
  </header>
  <main>
    {body}
  </main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Convert Qzone export JSON to a readable HTML file."
    )
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument(
        "output",
        nargs="?",
        help="Output HTML file path (default: <input>.html)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    title = input_path.stem
    html_text = render_html(data, title)

    output_path.write_text(html_text, encoding="utf-8")
    print(f"HTML written to: {output_path}")


if __name__ == "__main__":
    main()
