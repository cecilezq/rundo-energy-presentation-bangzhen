"""Publish the presentation through 2026, then deploy only an expiry notice."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "_site"
CUTOFF = datetime.fromisoformat("2027-01-01T00:00:00+08:00")
EXPIRED = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>RunDo 演示已到期</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f8f9f4;color:#193b35;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}main{max-width:620px;padding:40px}b{color:#2e7c54;font-size:30px}h1{font-size:28px;margin:28px 0 16px}p{line-height:1.8;color:#63766d}</style></head><body><main><b>RunDo</b><h1>本次在线演示已结束公开访问</h1><p>公开演示有效期已于2026年12月31日结束（马来西亚时间）。<br>如需继续查看，请联系汇报提供方获取最新版本。</p></main></body></html>'''


def build(now=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("A timezone-aware timestamp is required")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    if now >= CUTOFF:
        (OUTPUT / "index.html").write_text(EXPIRED, encoding="utf-8")
        (OUTPUT / "404.html").write_text(EXPIRED, encoding="utf-8")
        print("Expired: deployment contains only the expiry notice.")
    else:
        shutil.copyfile(ROOT / "presentation.html", OUTPUT / "index.html")
        print("Active: publishing the presentation until 2027-01-01 00:00 MYT.")
    (OUTPUT / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", help="Timezone-aware ISO timestamp for expiry validation")
    args = parser.parse_args()
    build(datetime.fromisoformat(args.now) if args.now else None)
