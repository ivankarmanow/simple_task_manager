<script setup>
import TaskList from './components/TaskList.vue'
import TaskActions from "@/components/TaskActions.vue";
import TaskData from "@/components/TaskData.vue";
import TaskCreate from "@/components/TaskCreate.vue";
import TaskEdit from "@/components/TaskEdit.vue";
import TaskDelete from "@/components/TaskDelete.vue";

import {onMounted, provide, ref, watch} from "vue"

import Error from "@/components/Error.vue";

const current_task_id = ref(0)
const current_task = ref(null)

const updates = ref(0)

provide("current_task_id", current_task_id)
provide("updates", updates)

function fetchCurrentTask(task_id) {
    current_task_id.value = task_id
    if (task_id > 0) {
        fetch(`api/task/get/${task_id}`)
            .then(response => response.json())
            .then(data => current_task.value = data)
    } else {
        current_task.value = null
    }
}

</script>

<template>
    <div class="row gap-3 p-3">
        <div class="col-3 border border-1 border-opacity-50 rounded-3 p-3 overflow-auto fixed">
            <TaskList @task-selected="fetchCurrentTask"></TaskList>
        </div>
        <div class="col border border-1 border-opacity-50 rounded-3 p-5 pt-3 fixed overflow-auto fs-5">
            <div class="d-flex flex-row gap-3 pb-4">
                <TaskActions :current_task="current_task" @status-updated="fetchCurrentTask"></TaskActions>
            </div>
            <TaskData :current_task="current_task"></TaskData>
        </div>
    </div>
    <TaskCreate @task-created="fetchCurrentTask"></TaskCreate>
    <TaskEdit @task-edited="fetchCurrentTask" :current-task="current_task"></TaskEdit>
    <TaskDelete @task-deleted="fetchCurrentTask"></TaskDelete>
    <Error></Error>
</template>

<style scoped>

</style>
