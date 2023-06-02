<template>
    <q-page container class="q-pb-xl q-px-md">
        <div class="q-pa-md q-gutter-md" v-if="!jobsError">
            <template v-if="jobs.length">
                <q-banner inline-actions rounded :class="[systemsOperational ? 'bg-green' : 'bg-orange', 'text-white']"
                    v-if="hasActiveJobs">
                    <q-icon :name="systemsOperational ? 'check' : 'warning'" size="xs" /> {{ systemsOperational ?
                        allSystemsOperational : someSystemsOperational }}
                </q-banner>

                <q-banner inline-actions rounded class="bg-primary text-white" v-if="hasPausedJobs">
                    <q-icon name="info" size="xs" /> {{ pausedJobs }}
                </q-banner>
            </template>

            <div class="row">
                <q-input filled dense v-model="search" label="Search..." style="width: calc(100% - 150px)"
                    :disable="!jobs.length">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>
                <q-btn round flat icon="refresh" @click="refreshJobs" :disable="jobsLoading || jobs.length === 0">
                    <q-tooltip>
                        Click to refresh
                    </q-tooltip>
                </q-btn>
                <q-btn round flat icon="tune">
                    <q-tooltip>
                        Apply filteredJobs
                    </q-tooltip>
                    <q-menu>
                        <q-list style="min-width: 100px">
                            <q-item-label header>Jobs Filter</q-item-label>
                            <q-item tag="label" v-ripple>
                                <q-item-section side top>
                                    <q-checkbox v-model="jobsFilter.healthyJobs" />
                                </q-item-section>

                                <q-item-section>
                                    <q-item-label>Healthy Jobs</q-item-label>
                                    <q-item-label caption>
                                        Show only healthy jobs.
                                    </q-item-label>
                                </q-item-section>
                            </q-item>
                            <q-item tag="label" v-ripple>
                                <q-item-section side top>
                                    <q-checkbox v-model="jobsFilter.unhealthyJobs" />
                                </q-item-section>

                                <q-item-section>
                                    <q-item-label>Unhealthy Jobs</q-item-label>
                                    <q-item-label caption>
                                        Show only unhealthy jobs.
                                    </q-item-label>
                                </q-item-section>
                            </q-item>
                            <q-item tag="label" v-ripple>
                                <q-item-section side top>
                                    <q-checkbox v-model="jobsFilter.pausedJobs" />
                                </q-item-section>

                                <q-item-section>
                                    <q-item-label>Paused Jobs</q-item-label>
                                    <q-item-label caption>
                                        Show only paused jobs.
                                    </q-item-label>
                                </q-item-section>
                            </q-item>
                            <q-separator />
                            <q-item clickable v-close-popup @click="clearFilters">
                                <q-item-section>Clear all</q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                </q-btn>
                <JobAddEdit iconSize="md" />
            </div>
            <div class="row absolute-center" v-if="!jobs.length && !jobsLoading && !jobsError">
                <div class="text-subtitle2"><q-icon name="psychology_alt" size="sm" /> No Jobs found<br />
                    Click
                    <JobAddEdit iconSize="sm" /> to add a job
                </div>
            </div>
        </div>

        <div class="q-mx-md q-mt-sm">
            <q-inner-loading :showing="jobsLoading">
                <q-spinner-puff size="50px" color="primary" />
            </q-inner-loading>

            <error :text="jobsError" v-if="jobsError"></error>

            <div class="row q-col-gutter-md q-col-gutter-y-lg" v-else>
                <div class="col-md-4 clickable-card " v-for="job in filteredJobs" @click="route2Details(job.uuid)">
                    <q-card>
                        <q-item>
                            <q-item-section avatar class="q-pr-xs">
                                <q-avatar>
                                    <q-icon name="cloud" size="23px" color="orange" v-if="job.favicon_url === null" />
                                    <q-img height="25px" width="25px" spinner-color="black" spinner-size="1rem" fit="fill"
                                        v-else :src="job.favicon_url">
                                        <template v-slot:error>
                                            <q-icon name="cloud" size="23px" color="orange" />
                                        </template>
                                    </q-img>
                                </q-avatar>
                            </q-item-section>

                            <q-item-section>
                                <q-item-label>
                                    <div class="text-h6 q-pt-sm">{{ job.title }}</div>
                                </q-item-label>
                            </q-item-section>
                            <q-card-section class="flex flex-center q-pa-none q-ma-none">
                                <q-icon name="fiber_manual_record" size="0.7rem" :color="job.healthy ? 'green' : 'red'"
                                    v-if="job.state" />
                                <q-chip v-else dense class="text-caption q-pa-sm">Paused
                                    <q-tooltip>Job is paused. Open job details to resume it.</q-tooltip>
                                </q-chip>
                            </q-card-section>
                        </q-item>
                        <q-item>
                            <q-item-section>
                                <q-item-label caption class="q-py-2">
                                    {{ job.url }}
                                </q-item-label>
                            </q-item-section>
                        </q-item>
                    </q-card>
                </div>
            </div>
        </div>

    </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useJobsStore } from '../../store';
import Error from '../../components/Error.vue';
import router from '../../router';
import JobAddEdit from '../../components/jobs/JobAddEdit.vue'
import { JobType, JobsFilterType } from '../../types';

const allSystemsOperational = 'All Systems Operational.'
const someSystemsOperational = 'Some systems are not operational.'
const pausedJobs = 'Some jobs are paused.'

const search = ref<string>('')

const jobsStore = useJobsStore()

const jobsFilter = ref<JobsFilterType>({
    healthyJobs: false,
    unhealthyJobs: false,
    pausedJobs: false
})

const clearFilters = () => {
    jobsFilter.value.healthyJobs = false
    jobsFilter.value.unhealthyJobs = false
    jobsFilter.value.pausedJobs = false
}

const filteredJobs = computed(() => {
    let filteredJobs: Array<JobType> = []
    const searchStr = search.value.toLowerCase().trim()

    // Filter based on search string
    if (!searchStr)
        filteredJobs = jobsStore.getJobs
    else
        filteredJobs = jobsStore.getJobs.filter(job => {
            return (job.title.toLowerCase().includes(searchStr) || job.url.toLowerCase().includes(searchStr))
        })

    // Filter based on filter object
    filteredJobs = filteredJobs.filter(job => {
        if (jobsFilter.value.healthyJobs || jobsFilter.value.unhealthyJobs || jobsFilter.value.pausedJobs) {
            if (jobsFilter.value.healthyJobs && job.healthy)
                return job
            else if (jobsFilter.value.unhealthyJobs && !job.healthy)
                return job
            else if (jobsFilter.value.pausedJobs && !job.state)
                return job
        } else {
            return job
        }
    })

    return filteredJobs
})

const jobs = computed(() => {
    return jobsStore.getJobs
})

const jobsLoading = computed(() => {
    return jobsStore.getJobsLoading

})

const jobsError = computed(() => {
    return jobsStore.getJobsError
})

const refreshJobs = () => {
    jobsStore.forceFetchJobs()
}

const systemsOperational = computed((): boolean => {
    const activeJobs: Array<JobType> = jobs.value.filter(obj => obj.state)

    const systemStatus: boolean = activeJobs.every(obj => obj.healthy === true);

    return systemStatus
})

const hasActiveJobs = computed((): boolean => {
    return jobs.value.some(obj => obj.state)
})

const hasPausedJobs = computed((): boolean => {
    return jobs.value.some(obj => !obj.state);
})

const route2Details = (uuid: string) => {
    router.push({ name: 'jobDetails', params: { uuid } })
}

onMounted(() => {
    jobsStore.fetchJobs()
})
</script>
