if __name__ == "__main__":
    import sys

    sys.path.append("code")
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price: str) -> float:
    return float(price.replace("$", "").replace(",", ""))


def clean_scraped_text(scraped_text: str) -> list[str]:
    # Split and filter empty lines
    lines = [line.strip() for line in scraped_text.split("\n")]
    lines = [line for line in lines if line]

    # Remove unwanted items
    unwanted = ["NEW", "NEW!", "GS", "V", "P", "S"]
    lines = [line for line in lines if line not in unwanted]

    return lines


def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    cleaned = clean_scraped_text(scraped_text)

    # Get name from first line
    name = cleaned[0]

    # Find price (line starting with $)
    price = next((line for line in cleaned if line.startswith("$")), "$0.00")
    price = clean_price(price)

    # Get description (everything after price)
    price_index = next(
        (i for i, line in enumerate(cleaned) if line.startswith("$")), -1
    )
    if price_index >= 0 and price_index + 1 < len(cleaned):
        description = " ".join(cleaned[price_index + 1 :])
    else:
        description = "No description available for this item"

    return MenuItem(category=title, name=name, price=price, description=description)


if __name__ == "__main__":
    pass
