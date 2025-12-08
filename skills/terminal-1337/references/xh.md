# xh - Complete Reference

## Overview

`xh` is a friendly and fast tool for sending HTTP requests. It reimplements as much as possible of HTTPie's excellent design, with a focus on improved performance (via Rust). It makes interacting with APIs from the terminal a joy compared to `curl`.

## Why Use This Tool?

- **Developer Experience**: Concise syntax. No more `-X POST -H "Content-Type: application/json" -d '{"foo":"bar"}'`. Just `xh post url foo=bar`.
- **Visuals**: Syntax highlighted JSON output and headers.
- **Defaults**: Assumes JSON content type by default.
- **Speed**: significantly faster startup and execution than Python-based HTTPie.

## Installation

See `scripts/install-xh.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install xh

# Linux
# Cargo recommended
cargo install xh
# or check package manager (xh)
```

## Common Usage Patterns

### Basic Usage

**GET request:**
```bash
xh httpbin.org/get
# Short for: xh GET httpbin.org/get
```

**POST JSON data:**
```bash
xh post httpbin.org/post name=John age:=30
# Sends JSON: {"name": "John", "age": 30}
# Note: `=` is string, `:=` is raw JSON (numbers, booleans)
```

**Set Headers:**
```bash
xh get httpbin.org/headers X-Api-Key:12345
# Headers use colon separator
```

### Advanced Usage

**Form data (instead of JSON):**
```bash
xh -f post httpbin.org/post name=John file@~/photo.jpg
```

**Download file:**
```bash
xh -d https://example.com/large-file.zip
```

**Show only response body (great for piping):**
```bash
xh -b get httpbin.org/json | jq .
```

**Print the request that would be sent (dry run):**
```bash
xh --print=HhBb post httpbin.org/post name=test
# Prints request headers, request body, response headers, response body
```

### Integration with Other Tools

**Pipe to jq for filtering:**
```bash
xh get https://api.github.com/users/octocat | jq .name
```

**Pass token from environment:**
```bash
xh get api.example.com Authorization:"Bearer $TOKEN"
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--json` | (Default) Send/Accept JSON | `xh --json post ...` |
| `-f`, `--form` | Send form data (application/x-www-form-urlencoded) | `xh -f post ...` |
| `-d`, `--download` | Download output to file | `xh -d url` |
| `-h`, `--headers` | Print only response headers | `xh -h url` |
| `-b`, `--body` | Print only response body | `xh -b url` |
| `-v`, `--verbose` | Print whole request and response | `xh -v url` |
| `--offline` | Construct request/print it but don't send | `xh --offline post ...` |
| `--https` | Force HTTPS | `xh --https example.com` |
| `-o`, `--output <file>` | Write output to file | `xh get url -o data.json` |
| `-I`, `--ignore-stdin` | Do not read from stdin | `xh -I post url` |

## Configuration

`xh` supports a config file at `~/.config/xh/config.json` (or `config.toml`).

**Common settings**:
```json
{
    "default_options": [
        "--style=monokai"
    ]
}
```

## Tips & Tricks

1.  **Magic JSON syntax**:
    - `field=value` -> String
    - `field:=value` -> Raw JSON (number, bool, list, object)
    - `field@file.txt` -> Read value from file
    - `field:=@file.json` -> Read JSON from file
2.  **Shortcuts**: `https://` is optional. `xh example.com` works.
    `localhost` shortcuts: `xh :8000/api` -> `http://localhost:8000/api`.
3.  **Sessions**: Persist headers/cookies across requests.
    `xh --session=mysession login.com user=me`
    `xh --session=mysession dashboard.com` (Uses cookies from previous req)

## Gotchas & Common Issues

- **Issue**: Trying to pass a URL parameter with `&`.
  **Solution**: Shell interprets `&` as background. Quote the URL: `xh "example.com?a=1&b=2"` OR use `xh example.com a==1 b==2` (xh query param syntax).

- **Issue**: Piping output disables colors.
  **Solution**: Use `--style=auto` or `--force-color` if you really need it, but usually you want plain text for pipes.

## See Also

- Official documentation: https://github.com/ducaale/xh
- Related tools: `curl` (ubiquitous), `httpie` (original python version).
