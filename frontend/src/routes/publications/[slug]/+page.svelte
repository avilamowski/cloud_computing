<script>
	import CommentContainer from './CommentContainer.svelte';
	import Markdown from '@magidoc/plugin-svelte-marked';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import * as api from '$lib/api';
  import Toast from '../../Toast.svelte';
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
		comments = [...comments, ...com];
	});


	$: if (form?.success) {
		toastMessage = 'Comment created successfully!';
		toastType = 'success';
		toastVisible = true;
		console.log("Reactivity! success")
	}

	$: if (form?.error) {
		toastMessage = form.error;
		toastType = 'error';
		toastVisible = true;
		console.log("Reactivity! fail")
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
				user: {
						username: e.detail.comment.username,
						email: e.detail.comment.email
				},
				publication_id: publicationId,
				created_at: new Date().toISOString()
		}
		console.log("Comment", comment)

		try {
			const response = await api.post(`create_comment`, comment);
			comment.comment_id = response.comment_id;
			console.log("Success!")
			form = { success: 'Comment was created successfully' };
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
			<CommentContainer {comments} errors={[]} on:commentForm={loadNewComment}/>
		</div>
	</div>
	<Toast message={toastMessage} visible={toastVisible} type={toastType} />

</div>

