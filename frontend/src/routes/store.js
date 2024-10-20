import { writable } from 'svelte/store';

// export const publicationStore = writable(null);
export const isLoading = writable(false);

function localStorageStore(key, initial) {
    const value = localStorage.getItem(key)
    const store = writable(value == null ? initial : value);
    store.subscribe(v => localStorage.setItem(key, JSON.stringify(v)));
    return store;
}

export const isAuthenticated = localStorageStore('token', null);