# jq - Complete Reference

## Overview

`jq` is like `sed` for JSON data - you can use it to slice and filter and map and transform structured data with the same ease that `sed`, `awk`, `grep` and friends let you play with text. It is the industry standard for processing JSON in the terminal.

## Why Use This Tool?

- **Power**: A complete functional programming language for transforming JSON.
- **Necessity**: Modern APIs return JSON. `grep` and `awk` are terrible at parsing JSON. `jq` is built for it.
- **Developer Experience**: Pretty-prints JSON by default, making it readable.

## Installation

See `scripts/install-jq.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install jq

# Linux
sudo apt install jq

# Cargo (unofficial implementations exist, but standard is C based)
# Best to use system package manager
```

## Common Usage Patterns

### Basic Usage

**Pretty print JSON:**
```bash
echo '{"foo": "bar"}' | jq .
```

**Extract a value:**
```bash
cat data.json | jq .name
# Output: "John"
```

**Extract value without quotes (raw string):**
```bash
cat data.json | jq -r .name
# Output: John
```

### Advanced Usage

**Filter array of objects:**
```bash
# Get names of users with id > 10
cat users.json | jq '.[] | select(.id > 10) | .name'
```

**Construct new JSON object:**
```bash
# Create new object with specific fields
cat users.json | jq '{user: .name, location: .address.city}'
```

**Update/Modify values:**
```bash
# Set all 'active' flags to true
cat users.json | jq 'map(.active = true)'
```

### Integration with Other Tools

**Process API response:**
```bash
curl -s https://api.github.com/repos/jqlang/jq | jq .stargazers_count
```

**Use in loops:**
```bash
for url in $(cat urls.json | jq -r '.[]'); do
    curl -s $url
done
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-r`, `--raw-output` | Output strings without quotes | `jq -r .name` |
| `-c`, `--compact-output` | Output JSON on single line | `jq -c .` |
| `-S`, `--sort-keys` | Sort keys of objects | `jq -S .` |
| `--arg <name> <val>` | Pass variable to jq script | `jq --arg user "bob" ...` |
| `-e`, `--exit-status` | Set exit code based on output | `jq -e .success` |
| `-s`, `--slurp` | Read entire input stream into array | `jq -s .` |

## Configuration

`jq` does not typically use a global config file. It relies on arguments.

## Tips & Tricks

1.  **Debugging**: Use `debug` inside your filter to print intermediate values.
    `jq 'map(debug | .id)'`
2.  **Null checks**: Use the `?` operator to suppress errors if a field doesn't exist.
    `jq '.users[].address?.city'`
3.  **String interpolation**:
    `jq -r '"The user \(.name) is \(.age) years old"'`

## Gotchas & Common Issues

- **Issue**: Shell quoting.
  **Solution**: Always wrap your jq filter in single quotes `'...'` to prevent the shell from interpreting special characters like `|`, `&`, `()`.

- **Issue**: Numbers losing precision.
  **Solution**: JSON (and jq) uses 64-bit floats. Large integers (64-bit) might lose precision. Use strings for large IDs if possible.

## See Also

- Official documentation: https://jqlang.github.io/jq/manual/
- jqplay (Online sandbox): https://jqplay.org/
- Related tools: `yq` (for YAML), `fq` (for binary formats).
