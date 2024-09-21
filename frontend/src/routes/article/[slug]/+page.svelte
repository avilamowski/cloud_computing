<script>
	import ArticleMeta from './ArticleMeta.svelte';
	import CommentContainer from './CommentContainer.svelte';
	import { publicationStore } from '../../publicationStore.js';
	import { onMount } from 'svelte';

	// let publication;

	// onMount(() => {
	// 	const unsubscribe = publicationStore.subscribe(value => {
	// 		console.log("value", value);
	// 		publication = value;
	// 	});

	// 	return () => {
	// 		unsubscribe();
	// 	};
	// });

	/** @type {import('./$types').PageData} */
	export let comments;
</script>

<!-- <svelte:head> -->
	<!-- <title>{publication.title}</title> -->
<!-- </svelte:head> -->
<!-- if publication is empty -->
{#if $publicationStore}
	



<div class="article-page">
	<div class="banner">
		<div class="container">
			<h1>{$publicationStore.title}</h1>
			<!-- <ArticleMeta article={data.article} user={data.user} /> -->
		</div>
	</div>

	<div class="container page">
		<div class="row article-content">
			<div class="col-xs-12">
				<div>
					{$publicationStore.content}
				</div>
			</div>
		</div>

		<hr />

		<div class="article-actions" />

		<!-- <div class="row">
			<CommentContainer comments={comments} errors={[]} />
		</div> -->
	</div>
</div>

<div class="article-preview">
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
</div>
{/if}