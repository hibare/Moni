<template>
    <div class="text-center absolute-center">
        <q-icon name="error" :size="props.size" color="red" />
        <div class="q-pt-md text-h6">{{ props.text }}</div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps({
    size: {
        type: String,
        default: "xl"
    },
    text: {
        type: String,
        required: true
    }
})
</script>