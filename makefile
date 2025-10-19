serve:
	bundle exec jekyll serve --source docs --livereload

publish: publish_posts export_nbs

publish_posts:
	bash publish_posts.sh

export_nbs:
	bash export_notebooks.sh

