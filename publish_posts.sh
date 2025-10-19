# publish_posts.sh
set -e
rm -rf docs/_posts
mkdir -p docs/_posts
rsync -av --include="*.md" --exclude="*" content/ docs/_posts/

