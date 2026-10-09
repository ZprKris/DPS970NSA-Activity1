import shutil
import tempfile
import unittest
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from pathlib import Path

from email_filter import classify, load_entries, process_directory

ROOT = Path(__file__).resolve().parents[1]
ALLOW = load_entries(ROOT / "allow.txt")
RESTRICT = load_entries(ROOT / "restrict.txt")
BAD_WORDS = load_entries(ROOT / "bad_words.txt")


def parse_file(name):
    # Load and turn an .eml into EmailMessage obj.
    return BytesParser(policy=policy.default).parsebytes((ROOT / "test_data" / "incoming" / name).read_bytes())


class EmailAgentTests(unittest.TestCase):
    def test_allow_list_overrides_bad_words(self):
        self.assertEqual(classify(parse_file("allowed.eml"), ALLOW, RESTRICT, BAD_WORDS), "email")

    def test_restrict_list_overrides_normal_body(self):
        self.assertEqual(classify(parse_file("restricted.eml"), ALLOW, RESTRICT, BAD_WORDS), "spam")

    def test_six_bad_words_is_spam(self):
        self.assertEqual(classify(parse_file("spam.eml"), ALLOW, RESTRICT, BAD_WORDS), "spam")

    def test_normal_email(self):
        self.assertEqual(classify(parse_file("normal.eml"), ALLOW, RESTRICT, BAD_WORDS), "email")

    def test_exactly_five_not_spam(self):
        msg = EmailMessage()
        msg["From"] = "person@unknown.com"
        msg.set_content("win free prize urgent bonus")
        self.assertEqual(classify(msg, ALLOW, RESTRICT, BAD_WORDS), "email")

    def test_text_attachment_is_read(self):
        msg = EmailMessage()
        msg["From"] = "person@unknown.com"
        msg.set_content("Hello")
        msg.add_attachment("win free prize urgent bonus cash", subtype="plain", filename="offer.txt")
        self.assertEqual(classify(msg, ALLOW, RESTRICT, BAD_WORDS), "spam")

    def test_moves_into_correct_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            incoming = Path(temp) / "incoming"
            output = Path(temp) / "output"
            shutil.copytree(ROOT / "test_data" / "incoming", incoming)
            results = process_directory(incoming, output, ALLOW, RESTRICT, BAD_WORDS)
            self.assertEqual(len(results), 4)
            self.assertEqual(sorted(p.name for p in (output / "spam").glob("*.eml")), ["restricted.eml", "spam.eml"])
            self.assertEqual(sorted(p.name for p in (output / "email").glob("*.eml")), ["allowed.eml", "normal.eml"])
            self.assertEqual(list(incoming.glob("*.eml")), [])


if __name__ == "__main__":
    # Finds methods which names start with test_, runs them, 
    # and reports which passed or failed.
    unittest.main()
