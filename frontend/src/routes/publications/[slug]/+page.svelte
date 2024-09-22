<script>
	import ArticleMeta from './ArticleMeta.svelte';
	import CommentContainer from './CommentContainer.svelte';
	import { publicationStore } from '../../publicationStore.js';
	import Markdown from '@magidoc/plugin-svelte-marked';

	/** @type {import('./$types').PageData} */
	export let data;
	export let form;

	let toastMessage = '';
	let toastVisible = false;
	let toastType = ''; // 'success' or 'error'

	$: if (form?.success) {
		toastMessage = 'Comment created successfully!';
		toastType = 'success';
		toastVisible = true;
	}

	$: if (form?.error) {
		toastMessage = form.error;
		toastType = 'error';
		toastVisible = true;
	}

	$: if (toastVisible) {
		setTimeout(() => {
			toastVisible = false;
		}, 3000);
	}
</script>

<svelte:head>
	<title>{data.publication.title}</title>
</svelte:head>

<div class="article-page">
	<div class="banner">
		<div class="container">
			<h1>{data.publication.title}</h1>
		</div>
	</div>

	<div class="container page">
		<div class="row article-content">
			<div class="col-xs-12">
				<Markdown source={data.publication.content} />
			</div>
		</div>

		<hr />

		<!-- Comment section -->
		<div class="article-actions" />
		<div class="row">
			<CommentContainer comments={data.comments} errors={[]} />
		</div>
	</div>
</div>

<!-- Toast Notification -->
{#if toastVisible}
	<div class="toast {toastType}">
		{toastMessage}
	</div>
{/if}

<style>
	.toast {
		position: fixed;
		bottom: 20px;
		right: 20px;
		color: white;
		padding: 15px;
		border-radius: 5px;
		z-index: 1000;
		transition: opacity 0.3s ease;
	}

	.toast.success {
		background-color: #28a745; /* Green background for success */
	}

	.toast.error {
		background-color: #dc3545; /* Red background for error */
	}
</style>
