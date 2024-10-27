from bs4 import BeautifulSoup, PageElement

def assert_list_has_exactly_one_element(l: list, gt_message: str | None, lt_message: str | None) -> bool:
    if len(l) > 1:
        if gt_message:
            print(gt_message)
        return False
    
    if len(l) == 0:
        if lt_message:
            print(lt_message)
        return False
    
    return True

def find_exactly_one_element(soup: BeautifulSoup, elem_type: str, text: str) -> PageElement:
    matches = soup.find_all(elem_type, string=text)
    gt_message = f"More than two matches found for elem type: {elem_type} and text: {text}"
    lt_message = f"No matches found for elem type: {elem_type} and text: {text}"
    if assert_list_has_exactly_one_element(matches, gt_message, lt_message):
        return matches[0]

    return None