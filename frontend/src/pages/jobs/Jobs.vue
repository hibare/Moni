<template>
    <q-page container class="q-pb-xl q-px-md">
        <div class="q-pa-md q-gutter-md" v-if="!jobsError && jobs.length">
            <q-banner inline-actions rounded class="bg-green text-white">
                <q-icon name="check" size="xs" /> {{ systemOperationalBanner }}
            </q-banner>

            <div class="row">
                <q-input filled dense v-model="search" label="Search..." style="width: calc(100% - 100px)">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>
                <q-btn round flat icon="refresh" @click="refreshJobs" :disable="jobsLoading || jobs.length === 0">
                    <q-tooltip>
                        Click to refresh
                    </q-tooltip>
                </q-btn>
                <JobAddEdit iconSize="md" />
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
                            <q-card-section class="flex flex-center q-pa-0 q-ma-0">
                                <q-icon name="fiber_manual_record" size="0.7rem" :color="job.healthy ? 'green' : 'red'" />
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

const search = ref<string>('')

const jobsStore = useJobsStore()

const filteredJobs = computed(() => {
    const searchStr = search.value.toLowerCase().trim()

    if (!searchStr)
        return jobsStore.getJobs

    return jobsStore.getJobs.filter(job => {
        return (job.title.toLowerCase().includes(searchStr) || job.url.toLowerCase().includes(searchStr))
    })
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

const systemOperationalBanner = computed(() => {
    const healthyStatus = 'All Systems Operational.'
    const unhealthyStatus = 'Some systems are not operational.'

    const systemStatus: boolean = jobs.value.every(obj => obj.healthy === true);

    return systemStatus ? healthyStatus : unhealthyStatus
})

const route2Details = (uuid: string) => {
    router.push({ name: 'jobDetails', params: { uuid } })
}


onMounted(() => {
    jobsStore.fetchJobs()
})
</script>