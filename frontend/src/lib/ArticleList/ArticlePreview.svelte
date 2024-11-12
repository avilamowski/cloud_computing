<script>
  import { createEventDispatcher, onMount } from "svelte";
  import * as api from "$lib/api";

  export let publication;
  let isAdmin = false;

  function getFirstChars(content, count) {
    content = content.replace(/!\[.*\]\(.*\)/g, ""); // Remove markdown images
    if (content.length <= count) return content;
    return content.slice(0, count) + "..."; // Truncate text and add ellipsis
  }

  onMount(async () => {
    isAdmin = await api.isAdmin();
  });

  const dispatch = createEventDispatcher();

  const deletePublication = () => {
    dispatch("deletePublication", publication.publication_id);
  };
</script>

<div class="article-preview">
  <div class="article-meta">
    <div class="info" style="margin: 0;">
      {publication.user.username}
      <span class="date">{new Date(publication.created_at).toDateString()}</span
      >
    </div>

    {#if isAdmin}
      <button class="trash-icon" on:click={deletePublication}>
        <i class="ion-trash-a"></i>
      </button>
    {/if}
  </div>

  <a href="/publications/{publication?.publication_id}" class="preview-link">
    <h1>{publication?.title}</h1>
    {getFirstChars(publication?.content, 20)}
    <br />

    <!-- Tags -->
    <div class="tag-list">
      {#each publication.tags as tag}
        <span class="tag-pill">{tag}</span>
      {/each}
    </div>

    <span>Read more...</span>
  </a>
</div>

<style>
  .article-preview {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    transition: transform 0.2s;
  }

  .article-preview:hover {
    transform: scale(1.02);
  }

  .article-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    color: #666;
  }

  .info {
    display: flex;
    flex-direction: column;
  }

  .info .date {
    color: #888;
  }

  .preview-link:hover {
    text-decoration: underline;
  }

  /* Tag list styling */
  .tag-list {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
  }

  .tag-pill {
    background-color: #e0e0e0;
    border-radius: 20px;
    padding: 6px 12px;
    font-size: 0.9rem;
    color: #333;
    cursor: pointer;
    transition:
      background-color 0.3s,
      transform 0.1s;
  }

  .trash-icon {
    font-size: 1.5em;
    background: none;
    border: none;
    color: #333;
    cursor: pointer;
    transition: color 0.3s;
    position: absolute;
    right: 0;
  }

  .trash-icon:hover {
    color: #ff0000; /* Cambia el color al pasar el cursor */
  }

  .tag-pill.Miscellaneous {
    background-color: #ffa500; /* Naranja */
    color: white;
  }

  .tag-pill.Teacher {
    background-color: #800080; /* Violeta */
    color: white;
  }

  .tag-pill.Career {
    background-color: #ff69b4; /* Rosa */
    color: white;
  }

  .tag-pill.Subject {
    background-color: #1e90ff; /* Azul */
    color: white;
  }
</style>
