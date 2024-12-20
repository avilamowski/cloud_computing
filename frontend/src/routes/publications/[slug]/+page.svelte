<script>
  import CommentContainer from "./CommentContainer.svelte";
  import Markdown from "@magidoc/plugin-svelte-marked";
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import * as api from "$lib/api";
  import Toast from "../../Toast.svelte";
  import { toastStore } from "../../store";
  import { fetchUserAttributes } from "aws-amplify/auth";

  let data;
  let form;
  let publication = null;
  let tags = []; // New variable to store tags
  let comments = [];
  let currentPage = 1;
  let totalPages = 1;
  let loading = false;
  let isAdmin = false;

  $: p = +($page.url.searchParams.get("page") ?? "1");
  $: title = publication?.title || "Loading";
  $: content = publication?.content || "";

  onMount(async () => {
    await fetchData();
    isAdmin = await api.isAdmin();
  });

  async function fetchData() {
    const params = $page.params;
    const qPub = new URLSearchParams();
    qPub.set("publication_id", params.slug);

    const { publication: pub } = await api.get(`get_publications?${qPub}`);
    publication = pub;
    tags = pub.tags || []; // Assign tags from publication to tags variable
    await loadComments();
  }

  async function loadComments() {
    if (loading || currentPage > totalPages) return;
    loading = true;

    const params = $page.params;
    const qCom = new URLSearchParams();
    qCom.set("publication_id", params.slug);
    qCom.set("page", currentPage);

    const { comments: com, total_pages } = await api.get(
      `get_comments?${qCom}`
    );

    comments = [...comments, ...com];
    console.log("Comments", comments);

    totalPages = total_pages;
    currentPage += 1;

    loading = false;
  }

  const loadNewComment = async (e) => {
    const publicationId = $page.params.slug;
    const comment = {
      ...e.detail.comment,
      // user: {
      //   username: e.detail.comment.username,
      //   email: e.detail.comment.email,
      // },
      publication_id: publicationId,
      created_at: new Date().toISOString(),
    };

    try {
      const response = await api.post(`create_comment`, comment);
      comment.comment_id = response.comment_id;
      const { email, preferred_username: username } =
        await fetchUserAttributes();
      comment.user = { username, email };

      form = { success: "Comment was created successfully" };
      comments = [comment, ...comments];

      toastStore.show("Comment created successfully!", "success");
    } catch (e) {
      console.log(e);
      form = { error: "An error ocurred" };
      toastStore.show(form.error, "error");
    }
  };

  const deletePublication = async (e) => {
    const publicationId = $page.params.slug;
    const publication = {
      publication_id: publicationId,
    };
    try {
      const response = await api.post(`delete_publication`, publication);
      window.location.href = "/";
    } catch (e) {
      form = { error: "Failed deleting publication" };
      toastStore.show(form.error, "error");
    }
  };

  const deleteComment = async (e) => {
    const comment_body = e.detail.comment;
    try {
      const response = await api.post(`delete_comment`, comment_body);
      comments = comments.filter(
        (c) => c.comment_id !== comment_body.comment_id
      );
    } catch (e) {
      form = { error: "Failed deleting comment" };
      toastStore.show(form.error, "error");
    }
  };
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="article-page">
  <div class="banner">
    <div class="container publication-title">
      <h1>{title}</h1>
      {#if isAdmin}
        <button class="trash-icon" on:click={deletePublication}>
          <i class="ion-trash-a"></i>
        </button>
      {/if}
      <hr />
    </div>
  </div>

  <div class="container page">
    <div class="row article-content">
      <div class="col-xs-12">
        <Markdown source={content || ""} />
      </div>
    </div>

    <!-- Display tags -->
    {#if tags.length > 0}
      <div class="tags-section">
        <div class="tag-container">
          {#each tags as tag}
            <span class="tag-pill">{tag}</span>
          {/each}
        </div>
      </div>
    {/if}

    <hr />
    <!-- Comments Section -->
    <div class="row">
      <CommentContainer
        {comments}
        errors={[]}
        on:commentForm={loadNewComment}
        on:commentDelete={deleteComment}
      />
    </div>

    <!-- Load more comments button -->
    {#if currentPage <= totalPages}
      <div style="display: flex; justify-content: center;">
        <button
          class="btn btn-primary"
          on:click={loadComments}
          disabled={loading}
        >
          {#if loading}
            Loading...
          {:else}
            Load more comments...
          {/if}
        </button>
      </div>
    {/if}
  </div>

  <Toast />
</div>

<style>
  /* Ocultar la sección si está vacía */
  .tags-section {
    margin-top: 15px;
    margin-bottom: 15px;
  }

  /* Contenedor de tags disponibles y seleccionados */
  .tag-container {
    display: inline-flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  /* Estilo general para los tags */
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

  .publication-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
  }

  .trash-icon {
    font-size: 1.5em;
    background: none;
    border: none;
    color: #f9f9f9;
    cursor: pointer;
    transition: color 0.3s;
    position: absolute;
    right: 0;
  }

  .trash-icon:hover {
    color: #ff0000; /* Cambia el color al pasar el cursor */
  }
</style>
