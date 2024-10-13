import difflib

def starts_with(line, keyword, threshold=0.6, debug=False):
    start_of_line = line[:len(keyword)]
    similarity_ratio = difflib.SequenceMatcher(None, start_of_line, keyword).ratio()
    if debug and similarity_ratio >= threshold:
         print(f"Match found: {start_of_line}, Similarity ratio: {similarity_ratio * 100:.2f}%")
    return similarity_ratio >= threshold
    
