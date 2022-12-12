def strip_line(line):
    """Remove any whitespace and comments from a line."""
    comment_index = line.find("//")
    if comment_index != -1:
        return line[:comment_index].strip()
    return line.strip()
