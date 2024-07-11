<script setup>
import {inject, onMounted, ref, watch} from "vue";
import * as bootstrap from "bootstrap"

const props = defineProps(['current_task'])
const emit = defineEmits(['statusUpdated'])
const folder = ref(false)
function changeStatus(status) {
    fetch("api/task/status", {
        method: "POST",
        headers: {
            'Content-Type': "application/json;charset=utf-8"
        },
        body: JSON.stringify({
            task_id: props.current_task.id,
            status: status
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                emit("statusUpdated", props.current_task.id)
            } else {
                document.getElementById("error_text").setAttribute("data-bs-error-text", data.error.text)
                new bootstrap.Modal('#errorModal').show(document.getElementById("error_text"))
            }
        })
}

function fetchSubTasks() {
    console.log(props)
    if (props.current_task !== null) {
        fetch(`api/task/subtasks/${props.current_task.id}`)
        .then(response => response.json())
        .then(data => data.tasks.length > 0 ? folder.value = true : folder.value = false)
    }
}

onMounted(fetchSubTasks)
watch(() => props.current_task, fetchSubTasks)

</script>

<template>
    <span v-show="false" id="error_text" data-bs-error-text=""></span>
    <template v-if="current_task !== null">
        <button class="btn btn-primary" :data-bs-task-id="current_task.id" data-bs-toggle="modal"
                data-bs-target="#createModal" v-if="current_task.status !== 'completed'">Добавить подзадачу
        </button>
        <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editModal">Редактировать</button>
        <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal" v-if="!folder">Удалить</button>
        <button class="btn btn-warning" v-if="current_task.status === 'in_progress'" @click="changeStatus('paused')">Приостановить выполнение</button>
        <button class="btn btn-success"
                v-if="current_task.status === 'in_progress' || current_task.status === 'paused'" @click="changeStatus('completed')">Отметить завершённой
        </button>
        <button class="btn btn-success" v-if="current_task.status === 'assigned'" @click="changeStatus('in_progress')">Начать выполнение</button>
        <button class="btn btn-primary" v-if="current_task.status === 'paused'" @click="changeStatus('in_progress')">Продолжить выполнение</button>
    </template>
</template>

<style scoped>

</style>