import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")

    # TODO Write code here

    menu_items = []

    # Find all menu section titles
    sections = page.locator(".foodmenu__menu-section")

    # Iterate through each menu section
    for section in sections.all():
        section_name = section.locator(".foodmenu__menu-section-title").inner_text()

        items = section.locator(".foodmenu__menu-item")

        # Process each menu item
        for item in items.all():
            item_text = item.inner_text()
            menu_item = extract_menu_item(section_name, item_text)
            menu_items.append(menu_item.to_dict())

    df = pd.DataFrame(menu_items)
    df.to_csv("cache/tullys_menu.csv", index=False)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)
