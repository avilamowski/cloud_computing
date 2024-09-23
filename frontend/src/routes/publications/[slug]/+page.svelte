<script>
	import ArticleMeta from './ArticleMeta.svelte';
	import CommentContainer from './CommentContainer.svelte';
	import Markdown from '@magidoc/plugin-svelte-marked';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import * as api from '$lib/api';

	/** @type {import('./$types').PageData} */
	let data;
	let form;

	let toastMessage = '';
	let toastVisible = false;
	let toastType = ''; // 'success' or 'error'
	let publication = null;
	let comments = [];



	$: p = +($page.url.searchParams.get('page') ?? '1');
	$: title = publication?.title || 'Loading';
	$: content = publication?.content || '';

	onMount(async () => {

		const params = $page.params;
		// const article }, { comments }] = await Promise.all([
		// 	api.get(`articles/${params.slug}`, locals.user?.token),
		// 	api.get(`articles/${params.slug}/comments`, locals.user?.token)
		// ]);

		// const dirty = marked(article.body);
		// article.body = sanitizeHtml(dirty);

		const qPub = new URLSearchParams();
		qPub.set('publication_id', params.slug);
		const { publication: pub } = await api.get(`get_publications?${qPub}`);
		
		const qCom = new URLSearchParams();
		qCom.set('publication_id', params.slug);
		qCom.set('page', p);
		const com = await api.get(`get_comments?${qCom}`);

		data = { pub, page };
		publication = pub;
		comments = com;
	});


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

	const loadNewComment = async (e) => {
		// from url
		const publicationId = $page.params.slug;
		const comment = {
				...e.detail.comment,
				publication_id: publicationId
		}

		try {
			const response = await api.post(`create_comment`, comment);
			console.log("Success!")
			form = { success: 'Comment was created successfully' };
			console.log(data)
			comments = [comment, ...comments];
			// TODO: Fix this
		} catch (e) {
			console.log("Fail!", e)
			form = { error: 'Username or email are in use' };
		}
	};
</script>

<svelte:head>
	<title>{title}</title>
</svelte:head>

<div class="article-page">
	<div class="banner">
		<div class="container">
			<h1>{title}</h1>
		</div>
	</div>

	<div class="container page">
		<div class="row article-content">
			<div class="col-xs-12">
				<Markdown source={content || ''} />
			</div>
		</div>

		<hr />

		<!-- Comment section -->
		<div class="article-actions" />
		<div class="row">
			<CommentContainer comments={comments} errors={[]} on:commentForm={loadNewComment}/>
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
