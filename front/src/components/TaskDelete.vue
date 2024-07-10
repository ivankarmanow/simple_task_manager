<script setup>
import {inject} from "vue";

const emit = defineEmits(['taskDeleted'])
const current_task_id = inject("current_task_id")
const updates = inject("updates")

function deleteTask() {
    console.log(current_task_id.value)
    fetch("http://127.0.0.1:8000/task/delete", {
        method: "POST",
        headers: {
            'Content-Type': "application/json;charset=utf-8"
        },
        body: JSON.stringify({id: current_task_id.value})
    })
        .then(response => response.json())
        .then(data => {
            current_task_id.value = 0
            emit("taskDeleted")
            updates.value++
        })
}
</script>

<template>
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Подтверждение удаления</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    Вы точно хотите удалить задачу?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Нет</button>
                    <button type="button" class="btn btn-danger" @click="deleteTask" data-bs-dismiss="modal">Да</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>