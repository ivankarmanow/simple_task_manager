<script setup>
import Task from './Task.vue'
import {inject, onMounted, provide, ref, watch} from "vue";

defineEmits(['taskSelected'])
const tasks = ref({})
const updates = inject("updates")

function fetchTaskList() {
    fetch("http://127.0.0.1:8000/task/list")
        .then(response => response.json())
        .then(data => {
            tasks.value = data.tasks
        })
}

onMounted(fetchTaskList)
watch(updates, fetchTaskList)
</script>

<template>
    <div class="d-flex flex-row gap-3 justify-content-between">
        <button class="btn btn-primary" type="button" data-bs-toggle="modal" data-bs-target="#createModal">
            Добавить корневую задачу
        </button>
        <button class="btn btn-success" @click="updates++">Обновить список</button>
    </div>
    <div class="fs-5 mt-3">
        <ul>
            <Task
                class="item"
                v-for="task in tasks"
                :key="task.id"
                :item="task"
                :updates="updates"
                @task-selected="(task_id) => $emit('taskSelected', task_id)">
            </Task>
        </ul>
    </div>

</template>

<style scoped>

</style>
