"""Рендер аватара из tools/avatar.svg в avatar.png (1024x1024) и превью в круге.

    python tools/render_avatar.py

Рисует безоконный Chromium через Playwright: фильтры SVG (преломление, мазок кисти)
в нём выглядят так же, как в браузере на GitHub.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "tools" / "avatar.svg"


def main() -> None:
    svg = SVG.read_text(encoding="utf-8")
    html = ("<html><body style='margin:0;background:transparent'>"
            f"<div id='a' style='width:1024px;height:1024px'>{svg}</div>"
            "<div id='c' style='width:1024px;height:1024px;border-radius:50%;overflow:hidden;"
            f"background:#fff'>{svg}</div></body></html>")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1024, "height": 2048}, device_scale_factor=1)
        page.set_content(html)
        page.wait_for_timeout(300)
        page.locator("#a").screenshot(path=str(ROOT / "avatar.png"))
        page.locator("#c").screenshot(path=str(ROOT / "tools" / "avatar-circle-preview.png"), omit_background=True)
        browser.close()
    # GitHub принимает аватар не больше 1 МБ, а PNG с зерном весит ~1.3 МБ.
    # JPEG 92 весит ~150 КБ и на глаз не отличается - его и загружать в профиль.
    from PIL import Image
    Image.open(ROOT / "avatar.png").convert("RGB").save(
        ROOT / "avatar.jpg", quality=92, optimize=True, progressive=True)
    print("avatar.png, avatar.jpg")


if __name__ == "__main__":
    main()
