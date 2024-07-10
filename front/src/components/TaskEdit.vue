<script setup>
import {inject, reactive, watch} from "vue";

const emit = defineEmits(['taskEdited'])

const updates = inject('updates')

const props = defineProps(['currentTask'])

const temp_task = reactive({
    title: "",
    description: "",
    performers: "",
    own_plan_time: 0
})

watch(() => props.currentTask, () => {
    if (props.currentTask !== null) {
        temp_task.title = props.currentTask.title
        temp_task.description = props.currentTask.description
        temp_task.performers = props.currentTask.performers
        temp_task.own_plan_time = props.currentTask.own_plan_time
        temp_task.parent_id = props.currentTask.parent_id
    }
})

function editTask() {
    fetch("http://127.0.0.1:8000/task/update", {
        method: "POST",
        headers: {
            'Content-Type': "application/json;charset=utf-8"
        },
        body: JSON.stringify({
            task_id: props.currentTask.id,
            task_input: temp_task
        })
    })
        .then(response => response.json())
        .then(data => {
            emit("taskEdited", props.currentTask.id)
            console.log(props.currentTask.id)
            updates.value++
        })
}

</script>

<template>
    <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="EditModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Редактировать задачу</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="title" class="col-form-label">Название:</label>
                            <input type="text" class="form-control" id="title" required v-model="temp_task.title">
                        </div>
                        <div class="mb-3">
                            <label for="description" class="col-form-label">Описание:</label>
                            <textarea class="form-control" id="description" required
                                      v-model="temp_task.description"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="performers" class="col-form-label">Исполнители:</label>
                            <input type="text" class="form-control" id="performers" required
                                   v-model="temp_task.performers"/>
                        </div>
                        <div class="mb-3">
                            <label for="performers" class="col-form-label">Плановая трудоёмкость задачи (в
                                часах):</label>
                            <input type="number" class="form-control" id="plan_time" min="1" required
                                   v-model="temp_task.own_plan_time"/>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editTask">Обновить
                        задачу
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>