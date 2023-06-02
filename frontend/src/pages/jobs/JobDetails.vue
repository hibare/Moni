<template>
    <q-page container class="q-pa-md q-col-gutter-md">
        <error :text="jobError" v-if="jobError"></error>

        <template v-else>
            <JobDetails :uuid="(uuid as string)" v-if="uuid !== null"></JobDetails>

            <div class="row q-col-gutter-md q-col-gutter-y-md">
                <div class="col-md-3 col-12">
                    <JobCreated />
                </div>
                <div class="col-md-3 col-12">
                    <JobUpdated />
                </div>
                <div class="col-md-3 col-12">
                    <JobUptime :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
                <div class="col-md-3 col-12">
                    <JobResponseTime :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
            </div>

            <div class="row q-col-gutter-md q-col-gutter-y-md">
                <div class="col-md-6 col-12">
                    <JobNotifiers :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
                <div class="col-md-6 col-12">
                    <JobHistory :uuid="(uuid as string)" v-if="uuid !== null" />
                </div>
            </div>
        </template>
    </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import router from '../../router';
import { useJobStore } from '../../store';
import Error from '../../components/Error.vue';
import JobDetails from '../../components/jobs/JobDetails.vue';
import JobCreated from '../../components/jobs/JobCreated.vue';
import JobUpdated from '../../components/jobs/JobUpdated.vue';
import JobUptime from '../../components/jobs/JobUptime.vue';
import JobResponseTime from '../../components/jobs/JobResponseTime.vue';
import JobNotifiers from '../../components/jobs/JobNotifiers.vue';
import JobHistory from '../../components/jobs/JobHistory.vue';

const uuid = ref<String | null>(null)

const jobError = computed((): string => {
    const jobStore = useJobStore()
    return jobStore.getJobError || ''
})

onMounted(() => {
    uuid.value = router.currentRoute.value.params.uuid as string
})


</script>
