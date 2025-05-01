<template>
    <div>
        <q-banner inline-actions rounded class="bg-red text-white q-mb-md" v-if="!jobLoading && job && !job?.state">
            <q-icon name="warning" size="xs" /> This job is paused.
        </q-banner>
        <q-card style="min-height: 145px;">
            <q-inner-loading showing v-if="jobLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>
            <template v-else-if="job && !jobLoading">
                <q-item class="q-pb-none">
                    <q-item-section avatar class="q-pr-xs">
                        <q-avatar>
                            <q-icon name="cloud" size="23px" color="orange" v-if="job?.favicon_url === null" />
                            <q-img height="25px" width="25px" spinner-color="black" spinner-size="1rem" fit="fill" v-else
                                :src="job?.favicon_url">
                                <template v-slot:error>
                                    <q-icon name="cloud" size="23px" color="orange" />
                                </template>
                            </q-img>
                        </q-avatar>
                    </q-item-section>
                    <q-item-section>
                        <div class="text-h6 q-pt-xs">{{ job?.title }}
                            <q-icon name="fiber_manual_record" size="0.7rem" :color="job?.healthy ? 'green' : 'red'"
                                v-if="job?.state" />
                        </div>
                    </q-item-section>
                    <q-card-section class="flex flex-center q-pa-0 q-ma-0">
                        <div class="q-gutter-xs">
                            <q-btn flat round size="sm" :icon="job?.state ? 'pause' : 'play_arrow'"
                                :color="job?.state ? 'orange' : 'green'" @click="toggleJobStateDialog"
                                :disable="jobLoading" />
                            <JobAddEdit :isEdit="true" />
                            <q-btn flat round size="sm" icon="delete" color="red" @click="toggleJobDeleteDialog"
                                :disable="jobLoading" />
                        </div>
                    </q-card-section>
                </q-item>
                <q-card-section class="q-pt-none">
                    <div class="fit text-subtitle2 q-pl-sm">
                        {{ job?.url }} <q-icon class="cursor-pointer" name="content_copy" color="grey"
                            @click="copy2Clipboard(job?.url)" />
                    </div>
                </q-card-section>
                <q-card-section class="q-pt-md">
                    <div class="q-pl-sm q-gutter-md">
                        <span><q-icon name="update" color="blue" class="q-pr-xs" />
                            <q-tooltip>Job Interval</q-tooltip>
                            {{ job?.interval }} Min.</span>
                        <span><q-icon name="checklist" color="green" class="q-pr-xs" />
                            <q-tooltip>Job Success Status Codes</q-tooltip>
                            {{ job?.success_status.join(", ")
                            }}</span>
                        <span><q-icon name="shield" :color="job?.verify_ssl ? 'green' : 'red'" class="">
                                <q-tooltip>{{ job?.verify_ssl ? 'Verifies SSL' : 'Does not verify SSL' }}</q-tooltip>
                            </q-icon> </span>
                        <span><q-icon name="redo" :color="job?.check_redirect ? 'green' : 'red'" class="q-pr-xs">
                                <q-tooltip>
                                    {{ job?.check_redirect ? 'Checks for redirect' : 'Does not check for redirect' }}
                                </q-tooltip>
                            </q-icon></span>
                        <span><q-icon name="data_thresholding" color="brown" class="q-pr-xs" />
                            <q-tooltip>Job Failure Threshold</q-tooltip>
                            {{ job?.failure_threshold }}</span>
                    </div>
                </q-card-section>
            </template>
        </q-card>
    </div>



    <q-dialog v-model="jobStateDialog">
        <q-card class="q-px-md">
            <q-card-section>
                <div class="text-h6 text-primary">{{ job?.state ? 'Pause' : 'Resume' }} Job?</div>
            </q-card-section>

            <q-card-section class="q-py-md">
                Are you sure you want to {{ job?.state ? 'pause' : 'resume' }} job?.
            </q-card-section>

            <q-card-actions align="right" class="q-pt-md">
                <q-btn flat label="Cancel" class="text-capitalize" v-close-popup />
                <q-btn flat :label="job?.state ? 'Pause' : 'Resume'" class="text-capitalize" color="primary"
                    :loading="jobStateLoading" :disable="jobStateLoading" @click="toggleJobState" />
            </q-card-actions>
        </q-card>
    </q-dialog>

    <q-dialog v-model="jobDeleteDialog">
        <q-card class="q-px-md">
            <q-card-section>
                <div class="text-h6 text-primary">Delete Job?</div>
            </q-card-section>

            <q-card-section class="q-py-md">
                Are you sure you want to delete this job?. This is a non-reversible operation.
            </q-card-section>

            <q-card-actions align="right" class="q-pt-md">
                <q-btn flat label="Cancel" class="text-capitalize" v-close-popup />
                <q-btn flat label="Delete" class="text-capitalize" color="red" :loading="jobStateLoading"
                    :disable="jobStateLoading" @click="deleteJob" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { JobType } from '../../types';
import { useJobStore, useJobsStore } from '../../store';
import { copy2Clipboard } from "../../utils/utils"
import router from '../../router';
import JobAddEdit from './JobAddEdit.vue'

const jobStateDialog = ref<boolean>(false)
const jobDeleteDialog = ref<boolean>(false)

const props = defineProps({
    uuid: {
        type: String,
        required: true
    }
})

const job = computed((): JobType => {
    const jobStore = useJobStore()
    return jobStore.getJob as JobType
})

const jobLoading = computed((): boolean => {
    const jobStore = useJobStore()
    return jobStore.getJobLoading
})


const jobStateLoading = computed((): boolean => {
    const jobStore = useJobStore()
    return jobStore.getJobStateLoading
})

const toggleJobStateDialog = () => {
    jobStateDialog.value = !jobStateDialog.value
}

const toggleJobDeleteDialog = () => {
    jobDeleteDialog.value = !jobDeleteDialog.value
}

const toggleJobState = async () => {
    const jobsStore = useJobsStore()

    if (job?.value.state) {
        const jobStore = useJobStore()
        await jobStore.pauseJob(props.uuid)
    } else {
        const jobStore = useJobStore()
        await jobStore.resumeJob(props.uuid)
    }
    jobsStore.forceFetchJobs()
    toggleJobStateDialog()
}

const deleteJob = async () => {
    const jobStore = useJobStore()
    const status = await jobStore.deleteJob(props.uuid)
    if (status) {
        const jobsStore = useJobsStore()
        jobsStore.forceFetchJobs()
        router.push({ name: 'jobs' })
    }
}
onMounted(() => {
    const jobStore = useJobStore()
    jobStore.fetchJob(props.uuid)
})


</script>
