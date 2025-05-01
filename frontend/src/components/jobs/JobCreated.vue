<template>
    <q-card class="job-metric-card">
        <q-inner-loading showing v-if="jobLoading">
            <q-spinner-puff size="50px" color="primary" />
        </q-inner-loading>
        <q-card-section>
            <div class="text-weight-medium"><q-icon name="calendar_month" size="xs" class="q-mr-xs" />Created
                on</div>
            <div class="q-mt-md card-title">{{ prettyDate(job?.created) }}</div>
        </q-card-section>
    </q-card>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { JobType } from '../../types';
import { useJobStore } from '../../store';
import { prettyDate } from '../../utils/utils';

const job = computed((): JobType => {
    const jobStore = useJobStore()
    return jobStore.getJob as JobType
})

const jobLoading = computed((): boolean => {
    const jobStore = useJobStore()
    return jobStore.getJobLoading
})

</script>
