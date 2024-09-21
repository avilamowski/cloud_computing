<script>
  export let message = '';
  export let visible = false;

  $: if (visible) {
      setTimeout(() => visible = false, 3000);
  }
</script>

{#if visible}
  <div class="toast">
      {message}
  </div>
{/if}

<style>
  .toast {
      position: fixed;
      bottom: 20px;  /* Position at the bottom */
      right: 20px;   /* Position at the right */
      background-color: #28a745;
      color: white;
      padding: 15px;
      border-radius: 5px;
      z-index: 1000;
      transition: opacity 0.3s ease;  /* Optional: Add a fade effect */
  }
</style>
