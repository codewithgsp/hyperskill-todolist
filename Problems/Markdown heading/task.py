def heading(markdown, level=1):
    if level <= 0:
        return '#' + ' ' + markdown
    if level > 6:
        return '#' * 6 + ' ' + markdown
    return '#' * level + ' ' + markdown
