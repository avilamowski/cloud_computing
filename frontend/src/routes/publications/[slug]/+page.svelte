<script>
	import ArticleMeta from './ArticleMeta.svelte';
	import CommentContainer from './CommentContainer.svelte';
	import { publicationStore } from '../../publicationStore.js';
	import Markdown from '@magidoc/plugin-svelte-marked';

	/** @type {import('./$types').PageData} */

	export let data;

</script>

<svelte:head>
	<title>{data.publication.title}</title>
</svelte:head>

<div class="article-page">
	<div class="banner">
		<div class="container">
			<h1>{data.publication.title}</h1>
			<!-- <ArticleMeta article={data.article} user={data.user} /> -->
		</div>
	</div>

	<div class="container page">
		<div class="row article-content">
			<div class="col-xs-12">
				<Markdown source={data.publication.content} />
			</div>
		</div>


		<hr />

		<div class="article-actions" />

		<div class="row">
			<CommentContainer comments={data.comments} errors={[]} />
		</div>
	</div>
</div>

<!-- <div class="article-preview"> -->
	<!-- <div class="article-meta"> -->
		<!-- <a href="/profile/@{publication.author}"> -->
			<!-- <img src={article.author.image} alt={article.author.username} /> -->
		<!-- </a> -->

		<!-- <div class="info">
			<a class="author" href="/profile/@{publication.user}">{publication.author}</a>
			<span class="date">{new Date(publication.created_at).toDateString()}</span>
		</div> -->
	<!-- </div> -->

	<!-- <a href="/article/{$publication.publication_id}" class="preview-link" on:click={() => publicationStore.set(publication)}>
		<h1>{$publication.title}</h1>
		<p>{$publication.content}</p>
		<span>Read more...</span>
	</a> -->
<!-- </div> -->