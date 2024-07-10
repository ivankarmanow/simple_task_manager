<script setup>
import {onMounted, ref} from "vue";

const error_text = ref("")
onMounted(() => {
    document.getElementById("errorModal").addEventListener("show.bs.modal", (event) => {
        error_text.value = event.relatedTarget.getAttribute("data-bs-error-text")
    })
})

</script>

<template>
    <div class="modal fade" id="errorModal" tabindex="-1" aria-labelledby="errorModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Произошла ошибка</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    {{ error_text }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>