"""

This module handles taking an external file and parsing out youtube links.

This will be used on an extract of a bookmarks.html from mozilla.
"""
"https://www.youtube.com/watch?v=U18Ru3k5HrM"


def find_url(string):
    count, url, array = 0, "", []
    index = string.find("https://www.youtube.com/watch?v=")
    url = string[index+32:index+43]
    if index >= 0:
        count += 1
        array.append(url)
        find_url(string[index+43:])
    return count, array


def extract_links_from_file(input, output):
    """For each line in the input file, we need to find all the strings like
    https://www.youtube.com/watch?v=%
    where the % is an 11 char length string.
    """
    count = 0
    matches = []
    with open(input, "r", encoding="utf-8") as file:
        for line in file:
            inner_count, inner_matches = find_url(line)
            count += inner_count
            matches.extend(inner_matches)
    with open(output, "w+") as write_file:
        write_file.write(f"Total matches found: {count}\n")
        for url in matches:
            write_file.write(f"{url}\n")


if __name__ == "__main__":
    extract_links_from_file("./resources/bookmarks.html", "./resources/output")
