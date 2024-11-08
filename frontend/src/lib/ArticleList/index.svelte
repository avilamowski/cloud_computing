<script>
	import { page } from '$app/stores';
	import ArticlePreview from './ArticlePreview.svelte';
	import * as api from "$lib/api";

	export let publications;

	const deletePublication = async ({detail: id}) => {
		const publication = {publication_id: id};
		const response = await api.post(`delete_publication`, publication);
		publications = publications.filter((p) => p.publication_id !== id);
	};
</script>

{#if publications.length === 0}
	<div class="article-preview">No publications are here... yet.</div>
{:else}
	<div>
		{#each publications as publication (publication.publication_id)}
			<ArticlePreview {publication} user={$page.data.user} on:deletePublication={deletePublication}/>
		{/each}
	</div>
{/if}
