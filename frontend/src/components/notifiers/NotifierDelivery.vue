<template>
    <q-card class="job-metric-card">
        <q-inner-loading showing v-if="notifierDeliveryLoading">
            <q-spinner-puff size="50px" color="primary" />
        </q-inner-loading>
        <q-card-section>
            <div class="text-weight-medium"><q-icon name="rocket_launch" size="xs" class="q-mr-xs" />Delivery
            </div>
            <div class="q-mt-md card-title" v-if="notifierDeliveryError">Error</div>
            <div class="q-mt-md card-title" v-else>{{ notifierDelivery }}</div>
        </q-card-section>
    </q-card>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useNotifierStore } from '../../store';

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const notifierStore = useNotifierStore()

const notifierDelivery = computed((): string => {
    return notifierStore.getNotifierDelivery || ''
})

const notifierDeliveryLoading = computed((): boolean => {
    return notifierStore.getNotifierDeliveryLoading
})

const notifierDeliveryError = computed((): string => {
    return notifierStore.getNotifierDeliveryError || ''
})

onMounted(() => {
    notifierStore.fetchNotifierDelivery(props.uuid)
})
</script>
