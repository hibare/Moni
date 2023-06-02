<template>
    <q-card class="job-metric-card">
        <q-inner-loading showing v-if="notifierJobsLoading">
            <q-spinner-puff size="50px" color="primary" />
        </q-inner-loading>
        <q-card-section>
            <div class="text-weight-medium"><q-icon name="memory" size="xs" class="q-mr-xs" />Jobs
            </div>
            <div class="q-mt-md card-title" v-if="notifierJobsError">Error</div>
            <div class="q-mt-md card-title" v-else>{{ notifierJobs.length }}</div>
        </q-card-section>
    </q-card>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useNotifierJobsStore } from '../../store';
import { JobType } from '../../types';

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const notifierJobStore = useNotifierJobsStore()

const notifierJobs = computed((): Array<JobType> => {
    return notifierJobStore.getJobs
})

const notifierJobsLoading = computed((): boolean => {
    return notifierJobStore.getJobsLoading
})

const notifierJobsError = computed((): string => {
    return notifierJobStore.getJobsError || ''
})

onMounted(() => {
    notifierJobStore.fetchNotifierJobs(props.uuid)
})
</script>