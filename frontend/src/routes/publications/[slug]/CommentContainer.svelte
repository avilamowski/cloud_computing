<script>
	import CommentInput from './CommentInput.svelte';
	import Comment from './Comment.svelte';

	export let comments;
	// export let user;
</script>

<div class="col-xs-12 col-md-8 offset-md-2">
	<!-- {#if user}
		<div>
			<CommentInput {user} />
		</div>
	{:else}
		<p>
			<a href="/login">Sign in</a>
			or
			<a href="/register">sign up</a>
			to add comments on this article.
		</p>
	{/if} -->
	<div>
		<CommentInput on:commentForm/>
	</div>
	{#each comments as comment (comment.comment_id)}
		<Comment {comment} />
	{/each}
	
</div>
