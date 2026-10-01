# json-unwrap

**Smartly extract the main list from common JSON wrapper formats.**

Many CLIs and APIs return JSON like this:

```json
{
  "total": 42,
  "candidates": [ ... ],
  "summary": { ... }
}
```
or
```json
{
  "items": [ ... ]
}
```
`json-unwrap` automatically finds the list and writes a clean array.

## Installation
```bash
# Just drop it on your PATH
chmod +x json-unwrap
mv json-unwrap ~/.local/bin/   # or /usr/local/bin/
```
Or clone this repo and symlink it

## Usage
```bash
# Basic – extract the list
json-unwrap hygiene-candidates.json

# Only show what it would do (dry-run)
json-unwrap hygiene-candidates.json --check

# Custom output file
json-unwrap data.json -o cleaned.json

# Tell it which keys to try (in order)
json-unwrap data.json --keys candidates,items,results

# Pretty-print with different indent
json-unwrap data.json --indent 4
```
## Examples
```bash
$ json-unwrap hygiene-candidates.json
Used key: "candidates"
Found 3 items
Wrote → hygiene-candidates-clean.json
```
```bash
$ json-unwrap hygiene-candidates.json --check
Used key: "candidates"
Found 3 items
(check mode — no file written)
```
```bash
$ json-unwrap some-api-response.json --keys items,results,data
Used key: "items"
Found 128 items
Wrote → some-api-response-clean.json
```
