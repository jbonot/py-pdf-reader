import difflib

def starts_with(line, keyword, threshold=0.8):

    start_of_line = line[:len(keyword)]
    
    # Use SequenceMatcher to get the similarity ratio
    similarity_ratio = difflib.SequenceMatcher(None, start_of_line, keyword).ratio()
    if similarity_ratio > threshold:
        print(f"Match found: {start_of_line}")
        print(f"Similarity ratio: {similarity_ratio * 100:.2f}%")

    # Return True if the similarity ratio is above the threshold
    return similarity_ratio >= threshold
    
