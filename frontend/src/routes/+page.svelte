<script>
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import ArticleList from '$lib/ArticleList/index.svelte';
	import Pagination from './Pagination.svelte';
	import { Carta, MarkdownEditor } from 'carta-md';
	import { attachment } from '@cartamd/plugin-attachment';
	import 'carta-md/default.css';
	import '@cartamd/plugin-attachment/default.css';
	import Toast from './Toast.svelte';
	import Searchbar from './Searchbar.svelte';
	import { afterUpdate, onMount } from 'svelte';
	import * as api from '$lib/api';
	import { afterNavigate } from '$app/navigation';

	const carta = new Carta({
		extensions: [
			attachment({
				upload: async (file) => {
					const formData = new FormData();
					formData.append('image', file);
					const url = await uploadImage(formData);
					return url;
				}
			})
		]
	});


	const uploadImage = async (formData) => {
		try {
			const file = formData.get('image');
			
			const buffer = await file.arrayBuffer();
			const base64Image = btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''));

			// get file extension
			const extension = file.name.split('.').pop();

			const response = await api.post(`upload_image`,
				{
						image_data: base64Image,
						file_type: extension
				},
			);

			return response.url;

		} catch (error) {
			console.error('Error uploading image:', error);
			return null;
		}
	}



	let data; 
	let form;

	let showModal = false;
	let tag, tab, p, page_link_base, searchTerm;
	let publications;
	let toastVisible = false;  // State for toast visibility
	let toastMessage = '';     // Message to display in the toast

	$: p = +($page.url.searchParams.get('page') ?? '1');
	$: searchTerm = $page.url.searchParams.get('search') ?? '';
	$: publications = data?.publications ?? [];
	// $: tag = $page.url.searchParams.get('tag');
	// $: tab = $page.url.searchParams.get('tab') ?? 'all';
	// $: page_link_base = `tag=${tag}&tab=${tab}`;

	function toggleModal() {
		showModal = !showModal;
		if (showModal) {
			document.body.style.overflow = 'hidden';
		} else {
			document.body.style.overflow = '';
		}
	}

	afterNavigate(async () => {
		const q = new URLSearchParams();

		q.set('page', p);
		if (searchTerm) q.set('search_term', searchTerm);

		const {publications, total_pages, total_publications } = await api.get(`get_publications?${q}`);
		const tags = [];

		data = {
			publications,
			pages: total_pages,
			tags
		};
	});

	const createPublication = async (e) => {
		e.preventDefault();
		console.log("event", e)

		const data = new FormData(e.target);
		console.log(data.get('content'))

		try {
			const response = await api.post(`create_publication`,
				{
						title: data.get('title'),
						content: data.get('content'),
						username: data.get('username'),
						email: data.get('email'),
						// tagList: data.get('tagList').split(' ')

				},
				// locals.user.token			
			);
			return {success: "Publication was created successfully"};
		} catch (e) {
			return {error: "Username or email are in use"}
		}
	}

	/** @type {import('./$types').PageData} */

	$: if (form?.success) {
		toastMessage = 'Publication created successfully!'; // Set the toast message
		toastVisible = true; // Show the toast
		toggleModal();
	}

</script>

<svelte:head>
	<title>Soul Pupils</title>
</svelte:head>

<div class="home-page">
	<div class="banner">
		<div class="container">
			<h1 class="logo-font">Soul pupils</h1>
			<p>A place to discuss what matters</p>
		</div>
	</div>

	<div class="container page">
		<div class="row">
			<div class="col-md-9">
				{#if data}
				<ArticleList publications={data.publications} />
				{#key p}
					<Pagination pages={data.pages} {p} href={(p) => `/?page=${p}`} />
				{/key}
				{/if}
			</div>

			<div class="col-md-3">
				<Searchbar {searchTerm} href={(t) => `/?search=${t}`}/>
				<button class="btn btn-lg btn-primary btn-block" on:click={toggleModal} type="button">
					Create Publication
				</button>
				<div class="sidebar">
					<!-- Modal -->
					{#if showModal}
						<div class="modal" role="dialog">
							<div class="modal-content">
								{#if form?.error}
									<div class="alert alert-danger">{form.error}</div>
								{/if}
								<span class="close" on:click={toggleModal} role="button" tabindex="0" aria-label="Close" aria-hidden="true" aria-controls="modal"> &times;</span>
								<h2>Create New Publication</h2>
								<form method="POST" action="?/createPublication" on:submit={createPublication}>
									<div>
										<label for="username">Username</label>
										<input type="text" id="username" name="username" class="form-control" required />
									</div>
									<div>
										<label for="email">Email</label>
										<input type="email" id="email" name="email" class="form-control" required />
									</div>
									<div>
										<label for="title">Title</label>
										<input type="text" id="title" name="title" class="form-control" required />
									</div>
									<div>
										<label for="content">Content</label>
										<MarkdownEditor {carta} textarea={{ 'name': "content", "required": true}}/>
									</div>
									<div class="form-group">
										<button class="btn btn-primary" type="submit">Submit</button>
										<button class="btn btn-secondary" type="button" on:click={toggleModal}>Cancel</button>
									</div>
								</form>
							</div>
						</div>
					{/if}

					<!-- Popular Tags -->
					<!-- <p>Popular Tags</p>
					<div class="tag-list">
						{#each data.tags as tag}
							<a href="/?tag={tag}" class="tag-default tag-pill">{tag}</a>
						{/each}
					</div> -->
				</div>
			</div>
		</div>
	</div>

	<!-- Toast Notification -->
	<Toast message={toastMessage} visible={toastVisible} />
</div>

<style>
	.modal {
		display: block;
		position: fixed;
		z-index: 1;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		overflow: auto;
		background-color: rgba(0, 0, 0, 0.4);
	}

	.modal-content {
		background-color: #fefefe;
		/* center horizontally */
		margin: 5% auto;
		padding: 20px;
		border: 1px solid #888;
		width: 80%;
	}

	.close {
		color: #aaa;
		float: right;
		font-size: 28px;
		font-weight: bold;
	}

	.close:hover,
	.close:focus {
		color: black;
		text-decoration: none;
		cursor: pointer;
	}

	button {
		margin: 10px 0;
	}

	.btn-block {
		width: 100%;
		margin-bottom: 20px;
	}
	
	:global(.carta-wrapper) {
		height: 400px;
		overflow: auto;
	}

	:global(.carta-container) {
		height: 100%;
		overflow: hidden;
	}

	:global(.carta-font-code) {
		font-family: '...', monospace;
		font-size: 1.1rem;
	}
</style>
