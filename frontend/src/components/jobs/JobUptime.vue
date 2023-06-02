<template>
    <q-card class="job-metric-card">
        <q-inner-loading showing v-if="jobUptimeLoading">
            <q-spinner-puff size="50px" color="primary" />
        </q-inner-loading>
        <q-card-section>
            <div class="text-weight-medium"><q-icon name="monitor_heart" size="xs" class="q-mr-xs" />Uptime
            </div>
            <div class="q-mt-md card-title" v-if="jobUptimeError">Error</div>
            <div class="q-mt-md card-title" v-else>{{ jobUptime }}</div>
        </q-card-section>
    </q-card>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useJobStore } from '../../store';

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const jobUptime = computed((): string => {
    const jobStore = useJobStore()
    return jobStore.getJobUptime || ''
})

const jobUptimeLoading = computed((): boolean => {
    const jobStore = useJobStore()
    return jobStore.getJobUptimeLoading
})

const jobUptimeError = computed((): string => {
    const jobStore = useJobStore()
    return jobStore.getJobUptimeError || ''
})

onMounted(() => {
    const jobStore = useJobStore()
    jobStore.fetchJobUptime(props.uuid)
})
</script>