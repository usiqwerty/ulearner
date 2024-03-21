def letter_index(index: int):
    return "abcdefghijklmnopqrstuvwxyz"[index]


def extract_blocks(blocks: list[dict]) -> dict[str, list[dict]]:
    typed_blocks={}
    for block in blocks:
        btype = block['$type']
        if btype not in typed_blocks:
            typed_blocks[btype]=[]
        typed_blocks[btype].append(block)
    return typed_blocks
