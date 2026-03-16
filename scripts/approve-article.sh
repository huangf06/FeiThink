#!/bin/bash
# Approve and move article from drafts to Hugo content

ARTICLE_ID=$1

if [ -z "$ARTICLE_ID" ]; then
    echo "Usage: ./scripts/approve-article.sh <article-id>"
    echo "Example: ./scripts/approve-article.sh 137279583"
    exit 1
fi

# Find files
EN_FILE=$(find output/drafts -name "${ARTICLE_ID}-*.en.md" 2>/dev/null | head -1)
ZH_FILE=$(find output/drafts -name "${ARTICLE_ID}-*.zh.md" 2>/dev/null | head -1)

if [ -z "$EN_FILE" ]; then
    echo "❌ Error: Article $ARTICLE_ID not found in output/drafts/"
    exit 1
fi

echo "Found files:"
echo "  EN: $(basename "$EN_FILE")"
echo "  ZH: $(basename "$ZH_FILE")"

# Copy to content/posts
cp "$EN_FILE" content/posts/
cp "$ZH_FILE" content/posts/

# Update draft status to false in English file
EN_DEST="content/posts/$(basename "$EN_FILE")"
sed -i 's/draft: true/draft: false/' "$EN_DEST"
sed -i 's/draft: True/draft: false/' "$EN_DEST"

# Update draft status in Chinese file
ZH_DEST="content/posts/$(basename "$ZH_FILE")"
sed -i 's/draft: true/draft: false/' "$ZH_DEST"
sed -i 's/draft: True/draft: false/' "$ZH_DEST"

echo ""
echo "✅ Approved and moved:"
echo "   → content/posts/$(basename "$EN_FILE")"
echo "   → content/posts/$(basename "$ZH_FILE")"
echo ""
echo "📝 Next steps:"
echo "   1. Review files in content/posts/"
echo "   2. git add content/posts/$(basename "$EN_FILE") content/posts/$(basename "$ZH_FILE")"
echo "   3. git commit -m \"feat: add translated article $ARTICLE_ID\""
echo "   4. git push"
