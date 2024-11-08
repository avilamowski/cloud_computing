<script>
  import * as api from "$lib/api";
  import { createEventDispatcher } from "svelte";
  import { onMount } from "svelte";
  export let comment;

  const dispatch = createEventDispatcher();
  let isAdmin = false;
  const deleteComment = async (e) => {
    dispatch("commentDelete", {
      comment: { comment_id: comment.comment_id },
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
    <div>
      <span>
        {comment.user.username}
      </span>
      <span class="date-posted"
        >{new Date(comment.created_at).toDateString()}</span
      >
    </div>

    {#if isAdmin}
      <button
        class="trash-button"
        aria-label="Delete comment"
        on:click={deleteComment}
      >
        <i class="ion-trash-a" />
      </button>
    {/if}
  </div>
</div>

<style>
  .card-footer {
    position: relative; /* Establece el contenedor como relativo */
    padding: 1rem; /* Espacio dentro del contenedor */
    display: flex;
    align-items: center; /* Centra el contenido verticalmente */
    justify-content: space-between; /* Distribuye el espacio entre los elementos */
  }

  .trash-button {
    background: none;
    border: none;
    padding: 0;
    margin: 0;
    opacity: 0.6;
    cursor: pointer;
    font-size: 1.5rem;
    margin-left: auto;
    color: #333;
    transition:
      opacity 0.3s ease,
      color 0.3s ease; /* Transición suave para la opacidad y el color */
  }

  .trash-button:hover {
    opacity: 1; /* Hace que el botón sea completamente visible al hacer hover */
    color: red; /* Cambia el color a rojo */
  }
</style>
