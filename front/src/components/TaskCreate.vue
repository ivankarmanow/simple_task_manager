<script setup>
import {inject, onMounted, ref} from "vue";

const emit = defineEmits(['taskCreated'])

const title = ref("")
const description = ref("")
const performers = ref("")
const own_plan_time = ref(0)
const parent_id = ref(null)

const updates = inject("updates")
const current_task_id = inject("current_task_id")

function addTask() {
    const createObj = {
        title: title.value,
        description: description.value,
        performers: performers.value,
        own_plan_time: own_plan_time.value,
    }
    if (parent_id.value !== null) {
        createObj.parent_id = parent_id.value
    }
    fetch("http://127.0.0.1:8000/task/create", {
        method: "POST",
        headers: {
            'Content-Type': "application/json;charset=utf-8"
        },
        body: JSON.stringify(createObj)
    })
        .then(response => response.json())
        .then(data => {
            current_task_id.value = data.task_id
            emit("taskCreated", data.task_id)
            updates.value++
        })
    clearTemp()
}

function fetchParent(event) {
    const pid = event.relatedTarget.getAttribute("data-bs-task-id")
    if (pid) {
        parent_id.value = pid
    }
    console.log(parent_id.value)
}

function clearTemp() {
    title.value = ""
    description.value = ""
    performers.value = ""
    own_plan_time.value = 0
    parent_id.value = null
}

onMounted(() => {
    document.getElementById("createModal").addEventListener("show.bs.modal", fetchParent)
})

</script>

<template>
    <div class="modal fade" id="createModal" tabindex="-1" aria-labelledby="CreateModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Добавить задачу</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="title" class="col-form-label">Название:</label>
                            <input type="text" class="form-control" id="title" required v-model="title">
                        </div>
                        <div class="mb-3">
                            <label for="description" class="col-form-label">Описание:</label>
                            <textarea class="form-control" id="description" required v-model="description"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="performers" class="col-form-label">Исполнители:</label>
                            <input type="text" class="form-control" id="performers" required v-model="performers"/>
                        </div>
                        <div class="mb-3">
                            <label for="performers" class="col-form-label">Плановая трудоёмкость задачи (в
                                часах):</label>
                            <input type="number" class="form-control" id="plan_time" min="1" required
                                   v-model="own_plan_time"/>
                        </div>
                        <input type="hidden" name="parent" id="parent" v-model="parent_id">
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" @click="addTask" data-bs-dismiss="modal">Добавить
                        задачу
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>