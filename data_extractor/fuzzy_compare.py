import difflib


def contains(line, keyword, threshold=0.6):
    words = line.split(" ")
    for word in words:
        similarity_ratio = difflib.SequenceMatcher(None, word, keyword).ratio()
        if similarity_ratio >= threshold:
            return True
    return False


def starts_with(line, keyword, threshold=0.6, debug=False):
    start_of_line = line[: len(keyword)]
    similarity_ratio = difflib.SequenceMatcher(None, start_of_line, keyword).ratio()
    if debug and similarity_ratio >= threshold:
        print(
            f"Match found: {start_of_line},"
            " Similarity ratio: {similarity_ratio * 100:.2f}%"
        )
    return similarity_ratio >= threshold
