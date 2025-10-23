serve:
	cd docs && bundle exec jekyll serve --drafts --future --livereload

publish: publish_posts export_nbs

publish_posts:
	bash publish_posts.sh

export_nbs:
	bash export_notebooks.sh

