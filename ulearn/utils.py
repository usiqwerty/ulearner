def letter_index(index: int):
    return "abcdefghijklmnopqrstuvwxyz"[index]


def extract_blocks(blocks: list[dict]) -> dict[str, dict]:
    return {block['$type']: block for block in blocks}
