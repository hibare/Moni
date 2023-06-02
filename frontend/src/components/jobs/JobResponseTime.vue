<template>
    <q-card class="job-metric-card">
        <q-inner-loading showing v-if="jobResponseTimeLoading">
            <q-spinner-puff size="50px" color="primary" />
        </q-inner-loading>
        <q-card-section>
            <div class="text-weight-medium"><q-icon name="schedule" size="xs" class="q-mr-xs" />Avg. Response
                Time
            </div>
            <div class="q-mt-md card-title" v-if="jobResponseTimeError">Error</div>
            <div class="q-mt-md card-title" v-else>{{ jobResponseTime }}</div>
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

const jobResponseTime = computed((): string => {
    const jobStore = useJobStore()
    return jobStore.getJobResponseTime || ''
})

const jobResponseTimeLoading = computed(() => {
    const jobStore = useJobStore()
    return jobStore.getJobResponseTimeLoading
})

const jobResponseTimeError = computed((): string => {
    const jobStore = useJobStore()
    return jobStore.getJobResponseTimeError || ''
})

onMounted(() => {
    const jobStore = useJobStore()
    jobStore.fetchJobResponseTime(props.uuid)
})
</script>