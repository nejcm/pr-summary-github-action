import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
from markdown_it import MarkdownIt
from markdown_it.token import Token

EMPTY_BLOCK = {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": []
    }
}

def parse_rich_text(token):
    if not hasattr(token, 'children') or token.children is None:
        return []

    rich_texts = []
    i = 0

    while i < len(token.children):
        child = token.children[i]

        if child.type == 'text':
            # Add text as is
            rich_texts.append({
                "type": "text",
                "text": {"content": child.content},
                "annotations": {
                    "bold": False,
                    "italic": False
                }
            })

        elif child.type == 'strong_open':
            # Add following text as bold
            if i + 1 < len(token.children) and token.children[i + 1].type == 'text':
                rich_texts.append({
                    "type": "text",
                    "text": {"content": token.children[i + 1].content},
                    "annotations": {
                        "bold": True,
                        "italic": False
                    }
                })
            i += 1  # Skip strong_close

        elif child.type == 'em_open':
            # Add following text as italic
            if i + 1 < len(token.children) and token.children[i + 1].type == 'text':
                rich_texts.append({
                    "type": "text",
                    "text": {"content": token.children[i + 1].content},
                    "annotations": {
                        "bold": False,
                        "italic": True
                    }
                })
            i += 1  # Skip em_close

        i += 1

    return rich_texts

def markdown_to_notion_blocks(markdown_text):
    md = MarkdownIt()
    tokens = md.parse(markdown_text)

    notion_blocks = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == 'heading_open':
            level = int(token.tag[-1])  # e.g., "h1" -> 1
            inline_token = tokens[i + 1]
            if inline_token.type == 'inline' and hasattr(inline_token, 'children'):
                rich_texts = parse_rich_text(inline_token)
                block_type = f"heading_{min(level, 3)}"  # Notion supports up to heading_3
                notion_blocks.append({
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": rich_texts
                    }
                })
            i += 2  # Skip heading_open and inline tokens

        elif token.type == 'paragraph_open':
            inline_token = tokens[i + 1]
            if inline_token.type == 'inline' and hasattr(inline_token, 'children'):
                rich_texts = parse_rich_text(inline_token)
                notion_blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": rich_texts
                    }
                })
            i += 2  # Skip paragraph_open and inline tokens

        else:
            i += 1  # Move to the next token

    return notion_blocks

def chunk_text(text, max_chunk_size=2000):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += (" " + sentence if current_chunk else sentence)
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def split_lines(text):
    return text.split('\n')