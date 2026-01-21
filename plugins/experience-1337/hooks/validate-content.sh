#!/bin/bash
# Content validation hook for docs/experience/content/ markdown files
# Suggests fixes without blocking - per collaborative agency principle

# Read stdin once (tool input as JSON)
INPUT=$(cat)

# Parse file path and content
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty')
CONTENT=$(echo "$INPUT" | jq -r '.content // empty')

# Only validate files in docs/experience/content/
if [[ ! "$FILE_PATH" =~ docs/experience/content/.*\.md$ ]]; then
    exit 0
fi
ISSUES=""

# Check for .md extensions in links: [text](path.md) or [text](path.md#anchor)
if echo "$CONTENT" | grep -qE '\]\([^)]*\.md[)#]'; then
    ISSUES="${ISSUES}
- Links should not have .md extension (use /explore/reference not ./reference.md)"
fi

# Check for relative links starting with ./ or ../
if echo "$CONTENT" | grep -qE '\]\(\.\.?/'; then
    ISSUES="${ISSUES}
- Use absolute paths for internal links (start with /)"
fi

# Check if parent directory needs index.md
DIR=$(dirname "$FILE_PATH")
BASENAME=$(basename "$FILE_PATH")
if [[ "$BASENAME" != "index.md" && ! -f "$DIR/index.md" ]]; then
    ISSUES="${ISSUES}
- Directory $DIR has no index.md - breadcrumbs will 404"
fi

# Output issues as suggestion (not blocking)
if [[ -n "$ISSUES" ]]; then
    echo "Content structure suggestions:$ISSUES"
    echo ""
    echo "See CLAUDE.md > Experience App > Content Authoring for details."
fi

exit 0
