<script setup>
const props = defineProps(['current_task'])
const formatter = new Intl.DateTimeFormat('ru', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
})
const statuses = {
    assigned: "Назначена",
    in_progress: "Выполняется",
    paused: "Приостановлена",
    completed: "Завершена"
}
</script>

<template>
    <template v-if="current_task !== null">
        <h1>{{ current_task.title }}</h1>
        <p><b class="fs-4">Описание: </b>{{ current_task.description }}</p>
        <p><b class="fs-4">Исполнители: </b>{{ current_task.performers }}</p>
        <p><b class="fs-4">Создано: </b>{{ formatter.format(new Date(current_task.created_at)) }}</p>
        <p><b class="fs-4">Статус задачи: </b>{{ statuses[current_task.status] }}</p>
        <p><b class="fs-4">Плановая трудоёмкость: </b>{{ current_task.own_plan_time }} часов</p>
        <p><b class="fs-4">Плановая трудоёмкость
            подзадач: </b>{{ (current_task.plan_time - current_task.own_plan_time) }} часов</p>
        <p v-if="current_task.status === 'completed'"><b class="fs-4">Фактическое время
            выполнения: </b>{{ current_task.own_real_time }} часов</p>
        <p v-if="current_task.status === 'completed'"><b class="fs-4">Фактическое время выполнения
            подзадач: </b>{{ (current_task.real_time - current_task.own_real_time) }} часов</p>
        <p v-if="current_task.status === 'completed'"><b class="fs-4">Дата
            завершения: </b>{{ formatter.format(new Date(current_task.completed_at)) }}</p>
    </template>
    <template v-else>
        <h1>Выберите задачу</h1>
    </template>
</template>

<style scoped>

</style>