from app.factory import VideoFactory, YoutubeVideos

"""
This helper script will parse an extracted bookmark file, and generate a unique list of youtube URLs and metadata.

This list will have to be parsed by hand, and appropriate categories given (Song, Playlist, Neither)
"""


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
        for url in matches:
            write_file.write(f"{url}\n")
    with open(output, "r") as read:
        lines = 0
        for url in read:
            lines += 1
    print(f"Found {lines} unique urls")


def enrich_links(input, output):
    """"""
    with open(input, "r", encoding="utf-8") as input_file:
        with open(output, "w+", encoding='utf-8') as output_file:
            for line in input_file:
                vid = VideoFactory(f"https://www.youtube.com/watch?v={line.rstrip()}").classify()
                if isinstance(vid, YoutubeVideos):
                    output_file.write(f"{vid.url}|{vid.type}|{vid.duration}|{vid.title}|{vid.description}\n")
                    output_file.flush()


if __name__ == "__main__":
    input = "../temp/bookmarks.html"
    output = "../temp/raw_links"
    extract_links_from_file(input, output)
    enrich_links(output, output + "_enriched")
