<script>
  import { enhance } from "$app/forms";
  import { page } from "$app/stores";
  import ArticleList from "$lib/ArticleList/index.svelte";
  import Pagination from "./Pagination.svelte";
  import { Carta, MarkdownEditor } from "carta-md";
  import { attachment } from "@cartamd/plugin-attachment";
  import "carta-md/default.css";
  import "@cartamd/plugin-attachment/default.css";
  import Toast from "./Toast.svelte";
  import Searchbar from "./Searchbar.svelte";
  import * as api from "$lib/api";
  import { afterNavigate, goto } from "$app/navigation";
  import { token, toastStore } from "./store";

  $: isAuthenticated = $token != undefined;

  let availableTags = []; // Lista de tags disponibles obtenidos desde la API
  let selectedTags = []; // Lista de tags seleccionados
  let tagFilter = ""; // Campo para buscar tags

  // Carta editor setup
  const carta = new Carta({
    extensions: [
      attachment({
        upload: async (file) => {
          const formData = new FormData();
          formData.append("image", file);

          if (
            !["png", "jpg", "jpeg", "gif"].includes(
              file.name.split(".").pop()
            ) ||
            file.size > 20 * 1024 * 1024
          )
            return "Unsupported file type or size";

          const url = await uploadImage(formData);
          return url;
        },
      }),
    ],
  });

  const uploadImage = async (formData) => {
    try {
      const file = formData.get("image");
      const buffer = await file.arrayBuffer();
      const base64Image = btoa(
        new Uint8Array(buffer).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          ""
        )
      );

      const extension = file.name.split(".").pop();

      const response = await api.post(`upload_image`, {
        image_data: base64Image,
        file_type: extension,
      });

      return response.url;
    } catch (error) {
      console.error("Error uploading image:", error);
      return null;
    }
  };

  let data;
  let form;
  let showModal = false;
  let tag, tab, p, page_link_base, searchTerm;
  let publications;

  // Al navegar, obtiene las publicaciones y tags
  $: p = +($page.url.searchParams.get("page") ?? "1");
  $: searchTerm = $page.url.searchParams.get("search") ?? "";
  $: publications = data?.publications ?? [];
  $: selectedTagsParam = selectedTags.length ? selectedTags.join(",") : "";
  afterNavigate(async () => {
    const searchParams = new URLSearchParams(window.location.search);
    p = +(searchParams.get("page") ?? "1");
    searchTerm = searchParams.get("search") ?? "";
    const tagsFromURL = searchParams.get("tags") ?? "";
    searchSelectedTags = tagsFromURL ? tagsFromURL.split(",") : [];

    try {
      const publicationsResponse = await api.get(
        `get_publications?page=${p}&search=${searchTerm}&tags=${tagsFromURL}`
      );
      const tagsResponse = await api.get(`get_tags`);
      console.log(tagsResponse);

      data = {
        publications: publicationsResponse.publications,
        pages: publicationsResponse.total_pages,
        tags: tagsResponse.tags,
      };

      availableTags = tagsResponse.tags ?? [];
    } catch (error) {
      console.error("Error fetching publications or tags:", error);
    }
  });

  // Función para crear la publicación
  const createPublication = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);

    try {
      const response = await api.post(`create_publication`, {
        title: data.get("title"),
        content: data.get("content"),
        tags: selectedTags.map(t => t.name), // Envía los tags seleccionados
      });
      document.body.style.overflow = "";
      goto(`/publications/${response.publication_id}`);

      toastStore.show("Publication created successfully!", "success");
    } catch (e) {
      form = { error: "There was an error creating the publication" };
      toastStore.show("There was an error creating the publication!", "error");
    }
  };

  function toggleModal() {
    showModal = !showModal;
    if (showModal) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
      clearTags();
    }
  }

  let searchSelectedTags = [];

  function toggleTag(tag) {
    if (selectedTags.includes(tag)) {
      selectedTags = selectedTags.filter((t) => t !== tag); // Eliminar tag
    } else if (selectedTags.length < 5) {
      selectedTags = [...selectedTags, tag]; // Agregar tag si hay espacio
    } else {
      toastStore.show("You can select up to 5 tags only", "warning");
    }
  }

  $: filteredTags = availableTags.filter((tag) => {
    const normalizedTag = tag.name
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
    const normalizedFilter = tagFilter
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");

    return (
      normalizedTag.toLowerCase().includes(normalizedFilter.toLowerCase()) &&
      !selectedTags.includes(tag)
    );
  });

  function clearTags() {
    selectedTags = [];
    tagFilter = "";
  }

  function toggleSearchTags(tag) {
    if (searchSelectedTags.includes(tag)) {
      searchSelectedTags = searchSelectedTags.filter((t) => t !== tag);
    } else {
      searchSelectedTags = [...searchSelectedTags, tag];
    }

    updateURLWithTags(); // Actualiza la URL para reflejar la búsqueda combinada
    fetchPublications(); // Llama a la función para buscar publicaciones
  }

  function updateURLWithTags() {
    const searchParams = new URLSearchParams();

    if (searchSelectedTags.length > 0) {
      searchParams.set("tags", searchSelectedTags.join(","));
    }

    // Mantiene el término de búsqueda en la URL si está presente
    if (searchTerm && searchTerm.trim() !== "") {
      searchParams.set("search", searchTerm);
    }

    const newURL = `/?${searchParams.toString()}`;
    goto(newURL, { replaceState: true });
  }

  async function fetchPublications() {
    const searchParams = new URLSearchParams();

    if (searchTerm && searchTerm.trim() !== "") {
      searchParams.set("search", searchTerm);
    }

    if (searchSelectedTags.length > 0) {
      searchParams.set("tags", searchSelectedTags.join(","));
    }

    const queryString = searchParams.toString();

    try {
      const response = await api.get(`/get_publications?${queryString}`);
      data.publications = response.publications;
    } catch (error) {
      console.error("Error fetching publications:", error);
    }
    console.log(searchSelectedTags);
  }
</script>

<svelte:head>
  <title>Soul Pupils</title>
</svelte:head>

<div class="home-page">
  <div class="banner">
    <div class="container">
      <h1 class="logo-font">Soul Pupils</h1>
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
        {#if isAuthenticated}
          <button
            class="btn btn-lg btn-primary btn-block"
            on:click={toggleModal}
            type="button"
          >
            Create Publication
          </button>
        {/if}
        <Searchbar
          {searchTerm}
          {searchSelectedTags}
          href={(t) => `/?search=${t}`}
        />

        <!-- Contenedor de búsqueda y tags disponibles -->
        <div class="tag-search-container">
          <div>
            <h5>Available Tags</h5>
            <!-- Input para buscar tags -->
            <input
              type="text"
              placeholder="Search tags..."
              bind:value={tagFilter}
              class="search-input"
            />
          </div>

          <!-- Mostrar solo si hay tags filtrados -->
          {#if filteredTags.length > 0}
            <div class="tags-section-scrollable">
              <!-- Contenedor de tags -->
              <div class="tag-container">
                {#each filteredTags as tag}
                {#if searchSelectedTags.includes(tag.name)}
                  <span
                    class="tag-pill {searchSelectedTags.includes(tag.name)
                      ? 'selected'
                      : ''} {tag.tag_type}"
                    on:click={() => toggleSearchTags(tag.name)}
                  >
                    {tag.name}
                  </span>
                {/if}
                {/each}
                {#each filteredTags as tag}
                {#if !searchSelectedTags.includes(tag.name)}
                  <span
                    class="tag-pill {searchSelectedTags.includes(tag.name)
                      ? 'selected'
                      : ''} {tag.tag_type}"
                    on:click={() => toggleSearchTags(tag.name)}
                  >
                    {tag.name}
                  </span>
                {/if}
                {/each}
              </div>
            </div>
          {/if}
        </div>

        <!-- Modal for Creating Publication -->
        <!-- Modal for Creating Publication -->
        {#if showModal}
          <div class="modal" role="dialog">
            <div class="modal-content">
              <span
                class="close"
                on:click={toggleModal}
                role="button"
                tabindex="0"
                aria-label="Close"
                aria-hidden="true"
                aria-controls="modal">&times;</span
              >
              <h2>Create New Publication</h2>
              <form method="POST" on:submit={createPublication}>
                <div>
                  <label for="title">Title</label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    class="form-control"
                    required
                  />
                </div>
                <div>
                  <label for="content">Content</label>
                  <MarkdownEditor
                    {carta}
                    textarea={{ name: "content", required: true }}
                  />
                </div>

                <!-- New container for the tag search section -->
                <div class="tag-search-container">
                  <!-- Input de búsqueda de tags con estilo mejorado -->
                  <div>
                    <input
                      type="text"
                      id="tagFilter"
                      bind:value={tagFilter}
                      placeholder="Search tags..."
                      class="search-input"
                    />
                  </div>

                  <!-- Contenedor de Tags Disponibles (oculto si no hay tags disponibles) -->
                  {#if filteredTags.length > 0}
                    <div class="tags-section-scrollable">
                      <h5>Available Tags</h5>
                      <div class="tag-container">
                        {#each filteredTags as tag}
                          <span
                            class="tag-pill {selectedTags.includes(
                              tag.name
                            )
                              ? 'selected'
                              : ''} {tag.tag_type}"
                            on:click={() => toggleTag(tag)}
                          >
                            {tag.name}
                          </span>
                        {/each}
                      </div>
                    </div>
                  {/if}

                  <!-- Contenedor de Tags Seleccionados (oculto si no hay tags seleccionados) -->
                  {#if selectedTags.length > 0}
                    <div class="tags-section-scrollable">
                      <h5>Selected Tags</h5>
                      <div class="tag-container">
                        {#each selectedTags as tag}
                          <span
                            class="tag-pill {selectedTags.includes(
                              tag.name
                            )
                              ? 'selected'
                              : ''} {tag.tag_type}"
                            on:click={() => toggleTag(tag)}
                          >
                            {tag.name}
                          </span>
                        {/each}
                      </div>
                    </div>
                  {/if}
                </div>

                <div class="form-group">
                  <button class="btn btn-primary" type="submit">Submit</button>
                  <button
                    class="btn btn-secondary"
                    type="button"
                    on:click={toggleModal}>Cancel</button
                  >
                </div>
              </form>
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Toast Component (handles toast display automatically via toastStore) -->
  <Toast />
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
  .search-input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s;
  }

  .search-input:focus {
    border-color: #4caf50;
    outline: none;
  }

  /* Contenedor de tags disponibles y seleccionados */
  .tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
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

  .tag-pill:hover {
    background-color: #c7c7c7;
    transform: scale(1.05);
  }

  /* Estilo para los tags seleccionados */
  .tag-pill.selected {
    background-color: #4caf50 !important;
    color: #fff;
    font-weight: bold;
  }

  .tag-pill.selected:hover {
    background-color: #388e3c;
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

  button {
    margin: 10px 0;
  }
  .btn-block {
    width: 100%;
    margin-bottom: 20px;
  }

  .tag-search-container {
    margin-top: 15px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f4f4f4;
  }

  .search-input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s;
  }

  .search-input:focus {
    border-color: #4caf50;
    outline: none;
  }

  .selected-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .tags-section-scrollable {
    margin-top: 10px;
    max-height: 200px; /* Ajusta la altura según sea necesario */
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  :global(.carta-wrapper) {
    height: 400px;
    overflow: auto;
  }

  :global(.carta-container) {
    height: 400px;
    overflow: hidden;
  }

  :global(.carta-font-code) {
    font-family: "...", monospace;
    font-size: 1.1rem;
  }

  :global(.carta-input, .carta-renderer) {
    height: 400px !important;
  }

  :global(.carta-theme__default .carta-container > *) {
    margin: 0;
    padding: 10px;
  }

  /* Estilos para los tags según el tipo */
</style>
