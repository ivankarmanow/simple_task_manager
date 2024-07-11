<script setup>
import {inject, onMounted, ref, watch} from 'vue'

const emit = defineEmits(['taskSelected'])
const props = defineProps(['item'])
const isOpen = ref(false)
const subtasks = ref({})
const updates = inject("updates")

function toggle(task_id) {
    if (props.item.folder) {
        isOpen.value = !isOpen.value;
    }
    emit("taskSelected", task_id)
}

function fetchTask() {
    fetch(`api/task/subtasks/${props.item.id}`)
        .then(response => response.json())
        .then(data => subtasks.value = data.tasks)
}

onMounted(fetchTask)
watch(updates, fetchTask)
</script>

<template>
    <li :class="{open: isOpen&&item.folder, closed: !isOpen&&item.folder}" class="my-3 user-select-none" @click.self="toggle(item.id)">
        {{ item.title }}
        <ul v-show="isOpen" v-if="item.folder">
            <Task
                class="item"
                v-for="child in subtasks"
                :key="child.id"
                :item="child"
                :updates="updates"
                @task-selected="(task_id) => $emit('taskSelected', task_id)"
            >
            </Task>
        </ul>
    </li>
</template>

<style scoped>

</style>