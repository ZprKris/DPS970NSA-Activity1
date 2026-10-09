"""Rule-based email classification agent for .eml files."""
import argparse
import re
import shutil
from email import policy
from email.parser import BytesParser
from pathlib import Path


def load_entries(path: Path) -> set[str]:
    """Read a domain or word list, ignoring blank lines and # comments."""
    return {
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def sender_domain(message) -> str:
    addresses = message["From"].addresses if message["From"] else ()
    if not addresses or not addresses[0].domain:
        return ""
    return addresses[0].domain.lower()


def readable_text(message) -> str:
    """Read text body and text attachments. Skip binary and encrypted parts."""
    chunks = []
    if message.is_multipart(): # Check for body and attachments.
        for part in message.walk(): # Visit the email and its nested parts recursively.
            if part.is_multipart(): # Skip containers.
                continue
            if part.get_content_type() == "text/plain":
                try:
                    chunks.append(part.get_content())
                except (UnicodeError, LookupError, ValueError, KeyError):
                    pass
    elif message.get_content_type() == "text/plain":
        try:
            chunks.append(message.get_content())
        except (UnicodeError, LookupError, ValueError, KeyError):
            pass
    return "\n".join(chunks)


def classify(message, allow: set[str], restrict: set[str], bad_words: set[str]) -> str:
    domain = sender_domain(message)
    if domain in allow:
        return "email"
    if domain in restrict:
        return "spam"
    # Extract all words from the email’s readable text. 
    # Not a split, because leaves out punctuation.
    words = re.findall(r"\b[\w']+\b", readable_text(message).lower())
    # Count matching word occurrences; six matches means spam.
    return "spam" if sum(word in bad_words for word in words) > 5 else "email"

def process_directory(incoming: Path, output: Path, allow: set[str], restrict: set[str], bad_words: set[str]) -> list[tuple[str, str]]:
    results = []
    if not incoming.is_dir():
        raise NotADirectoryError(incoming)
    if incoming.resolve() == (output / "spam").resolve() or incoming.resolve() == (output / "email").resolve():
        raise ValueError("Input directory must differ from output classification directories")
    for file in sorted(incoming.glob("*.eml")):
        with file.open("rb") as f:
            # Parses email structure, such as headers, and returns EmailMessage obj.
            message = BytesParser(policy=policy.default).parse(f)
        folder = classify(message, allow, restrict, bad_words)
        target_dir = output / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / file.name
        shutil.move(str(file), str(target))
        results.append((file.name, folder))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify incoming .eml emails")
    parser.add_argument("--incoming", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow", type=Path, required=True)
    parser.add_argument("--restrict", type=Path, required=True)
    parser.add_argument("--bad-words", type=Path, required=True)
    args = parser.parse_args()
    for filename, folder in process_directory(args.incoming, args.output, load_entries(args.allow), load_entries(args.restrict), load_entries(args.bad_words)):
        print(f"{filename} -> {folder}/")


if __name__ == "__main__":
    main()
