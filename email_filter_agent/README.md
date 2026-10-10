# Email-filtering simple reflex agent
An email-filtering agent classifies incoming messages as email or spam using allow and restrict lists of sender domains, and a list of bad words checked against message bodies and attachments.

## Rules 
1. Sender domain in `allow.txt` -> `email/` regardless of contents.
2. Otherwise, sender domain in `restrict.txt` -> `spam/`.
3. Otherwise, **more than five occurrences** of words from `bad_words.txt` in readable plain-text body and `.txt`/text/plain attachments -> `spam/`.
4. Otherwise -> `email/`.

## Run the agent

Use a disposable input folder because the agent moves emails out of it:

```bash
mkdir -p demo_incoming
cp test_data/incoming/*.eml demo_incoming/
python email_filter.py --incoming demo_incoming --output results --allow allow.txt --restrict restrict.txt --bad-words bad_words.txt
```

Expected classifications:
- `allowed.eml` -> `results/email/`
- `normal.eml` -> `results/email/`
- `restricted.eml` -> `results/spam/`
- `spam.eml` -> `results/spam/`

## Run automated tests

From this directory, run:

```bash
python -m unittest discover -s tests -v
```

## GitHub Actions
The workflow at `.github/workflows/tests.yml` automatically runs the tests on every push and pull request. See the repository's **Actions** tab for results.
