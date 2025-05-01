<template>
    <div class="text-center absolute-center">
        <q-spinner-puff color="deep-orange" :size="size" />
        <slot name="text"></slot>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        size: {
            type: String,
            default: "sm"
        }
    }
}
</script>
