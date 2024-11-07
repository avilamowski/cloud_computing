<script>
	import * as api from '$lib/api';
	import { createEventDispatcher } from 'svelte';
	import { onMount } from "svelte";
	export let comment;

	const dispatch = createEventDispatcher();
	let isAdmin = false;
	const deleteComment = async (e) => {
		dispatch('commentDelete', {
			comment: {comment_id: comment.comment_id}
		});
		e.target.reset();
	};
	onMount(async () => {
		isAdmin = await api.isAdmin();
	});
</script>

<div class="card">
	<div class="card-block">
		<p class="card-text">{comment.content}</p>
	</div>

	<div class="card-footer">
		<!-- <a href="/profile/@{comment.author.username}" class="comment-author">
			<img src={comment.author.image} class="comment-author-img" alt={comment.author.username} />
		</a> -->

		<!-- <a href="/" class="comment-author"> -->
			{comment.user.username}
		<!-- </a> -->

		<span class="date-posted">{new Date(comment.created_at).toDateString()}</span>
		
		{#if isAdmin}
			<button class="ion-trash-a" aria-label="Delete comment" on:click={deleteComment}/>
		{/if}
	</div>
</div>

<style>
	button {
		background: none;
		border: none;
		padding: 0;
		margin: 0;
		font-size: inherit;
		margin-left: 5px;
		opacity: 0.6;
		cursor: pointer;
	}
</style>
